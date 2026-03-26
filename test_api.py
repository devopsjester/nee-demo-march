import pytest
import requests
from unittest.mock import patch, MagicMock
from api import (
    get_location_by_zipcode,
    get_current_location,
    get_weather,
    get_aqi_category,
    get_air_quality,
    WMO_CONDITIONS,
)


# ---------------------------------------------------------------------------
# get_location_by_zipcode
# ---------------------------------------------------------------------------

class TestGetLocationByZipcode:
    def _make_response(self, status_code, json_data):
        mock = MagicMock()
        mock.status_code = status_code
        mock.json.return_value = json_data
        mock.raise_for_status = MagicMock()
        return mock

    def test_valid_zipcode_returns_location(self):
        payload = {
            "places": [
                {
                    "place name": "Beverly Hills",
                    "state": "California",
                    "latitude": "34.0901",
                    "longitude": "-118.4065",
                }
            ]
        }
        mock_resp = self._make_response(200, payload)
        with patch("api.requests.get", return_value=mock_resp):
            result = get_location_by_zipcode("90210")
        assert result["city"] == "Beverly Hills"
        assert result["state"] == "California"
        assert result["lat"] == pytest.approx(34.0901)
        assert result["lon"] == pytest.approx(-118.4065)

    def test_invalid_zipcode_raises_value_error(self):
        mock_resp = self._make_response(404, {})
        with patch("api.requests.get", return_value=mock_resp):
            with pytest.raises(ValueError, match="Invalid or unknown zip code"):
                get_location_by_zipcode("00000")

    def test_connection_error_raises_runtime_error(self):
        with patch("api.requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(RuntimeError, match="Unable to connect"):
                get_location_by_zipcode("90210")


# ---------------------------------------------------------------------------
# get_current_location
# ---------------------------------------------------------------------------

class TestGetCurrentLocation:
    def _make_response(self, json_data):
        mock = MagicMock()
        mock.status_code = 200
        mock.json.return_value = json_data
        mock.raise_for_status = MagicMock()
        return mock

    def test_success_returns_location(self):
        payload = {
            "status": "success",
            "city": "Austin",
            "regionName": "Texas",
            "lat": 30.2711,
            "lon": -97.7437,
        }
        with patch("api.requests.get", return_value=self._make_response(payload)):
            result = get_current_location()
        assert result["city"] == "Austin"
        assert result["state"] == "Texas"
        assert result["lat"] == pytest.approx(30.2711)
        assert result["lon"] == pytest.approx(-97.7437)

    def test_api_failure_status_raises_runtime_error(self):
        payload = {"status": "fail", "message": "reserved range"}
        with patch("api.requests.get", return_value=self._make_response(payload)):
            with pytest.raises(RuntimeError, match="Unable to determine current location"):
                get_current_location()

    def test_connection_error_raises_runtime_error(self):
        with patch("api.requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(RuntimeError, match="Unable to connect"):
                get_current_location()


# ---------------------------------------------------------------------------
# get_weather
# ---------------------------------------------------------------------------

class TestGetWeather:
    def _make_response(self, json_data):
        mock = MagicMock()
        mock.status_code = 200
        mock.json.return_value = json_data
        mock.raise_for_status = MagicMock()
        return mock

    def test_known_wmo_code_returns_condition(self):
        payload = {"current_weather": {"temperature": 72.5, "weathercode": 2}}
        with patch("api.requests.get", return_value=self._make_response(payload)):
            result = get_weather(34.09, -118.41)
        assert result["temperature_f"] == 72.5
        assert result["condition"] == "partly cloudy"

    def test_unknown_wmo_code_returns_fallback_string(self):
        payload = {"current_weather": {"temperature": 55.0, "weathercode": 999}}
        with patch("api.requests.get", return_value=self._make_response(payload)):
            result = get_weather(34.09, -118.41)
        assert result["temperature_f"] == 55.0
        assert "999" in result["condition"]

    def test_all_known_wmo_codes_are_mapped(self):
        for code, expected_condition in WMO_CONDITIONS.items():
            payload = {"current_weather": {"temperature": 60.0, "weathercode": code}}
            with patch("api.requests.get", return_value=self._make_response(payload)):
                result = get_weather(0, 0)
            assert result["condition"] == expected_condition

    def test_connection_error_raises_runtime_error(self):
        with patch("api.requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(RuntimeError, match="Unable to connect"):
                get_weather(34.09, -118.41)


# ---------------------------------------------------------------------------
# get_aqi_category
# ---------------------------------------------------------------------------

class TestGetAqiCategory:
    @pytest.mark.parametrize("value,expected", [
        (0, "Good"),
        (50, "Good"),
        (51, "Moderate"),
        (100, "Moderate"),
        (101, "Unhealthy for Sensitive Groups"),
        (150, "Unhealthy for Sensitive Groups"),
        (151, "Unhealthy"),
        (200, "Unhealthy"),
        (201, "Very Unhealthy"),
        (300, "Very Unhealthy"),
        (301, "Hazardous"),
        (500, "Hazardous"),
        (999, "Hazardous"),
    ])
    def test_aqi_category_boundaries(self, value, expected):
        assert get_aqi_category(value) == expected


# ---------------------------------------------------------------------------
# get_air_quality
# ---------------------------------------------------------------------------

class TestGetAirQuality:
    def _make_response(self, json_data):
        mock = MagicMock()
        mock.status_code = 200
        mock.json.return_value = json_data
        mock.raise_for_status = MagicMock()
        return mock

    def test_success_returns_aqi_and_category(self):
        payload = {"current": {"us_aqi": 42}}
        with patch("api.requests.get", return_value=self._make_response(payload)):
            result = get_air_quality(34.09, -118.41)
        assert result["aqi"] == 42
        assert result["category"] == "Good"

    def test_unhealthy_aqi_returns_correct_category(self):
        payload = {"current": {"us_aqi": 175}}
        with patch("api.requests.get", return_value=self._make_response(payload)):
            result = get_air_quality(34.09, -118.41)
        assert result["aqi"] == 175
        assert result["category"] == "Unhealthy"

    def test_none_aqi_raises_runtime_error(self):
        payload = {"current": {"us_aqi": None}}
        with patch("api.requests.get", return_value=self._make_response(payload)):
            with pytest.raises(RuntimeError, match="not available"):
                get_air_quality(34.09, -118.41)

    def test_connection_error_raises_runtime_error(self):
        with patch("api.requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(RuntimeError, match="Unable to connect"):
                get_air_quality(34.09, -118.41)
