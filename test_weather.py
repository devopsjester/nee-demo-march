"""Tests for api.py and weather.py (weather CLI)."""

from unittest.mock import MagicMock, patch

import pytest
import requests
from click.testing import CliRunner

from api import (
    WMO_CONDITIONS,
    get_current_location,
    get_location_by_zipcode,
    get_weather,
)
from weather import cli


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_response(status_code=200, json_data=None, raise_connection_error=False):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data or {}
    if raise_connection_error:
        mock.side_effect = requests.exceptions.ConnectionError
    if status_code != 200:
        mock.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock)
    else:
        mock.raise_for_status.return_value = None
    return mock


# ---------------------------------------------------------------------------
# get_location_by_zipcode
# ---------------------------------------------------------------------------


class TestGetLocationByZipcode:
    VALID_RESPONSE = {
        "places": [
            {
                "place name": "Austin",
                "state": "Texas",
                "latitude": "30.2672",
                "longitude": "-97.7431",
            }
        ]
    }

    def test_valid_zipcode_returns_location(self):
        with patch(
            "api.requests.get",
            return_value=_mock_response(json_data=self.VALID_RESPONSE),
        ):
            result = get_location_by_zipcode("78701")
        assert result["city"] == "Austin"
        assert result["state"] == "Texas"
        assert result["lat"] == pytest.approx(30.2672)
        assert result["lon"] == pytest.approx(-97.7431)

    def test_invalid_zipcode_raises_value_error(self):
        with patch("api.requests.get", return_value=_mock_response(status_code=404)):
            with pytest.raises(ValueError, match="Invalid or unknown zip code"):
                get_location_by_zipcode("00000")

    def test_connection_error_raises_runtime_error(self):
        with patch(
            "api.requests.get",
            side_effect=requests.exceptions.ConnectionError,
        ):
            with pytest.raises(RuntimeError, match="Unable to connect"):
                get_location_by_zipcode("78701")

    def test_server_error_raises_http_error(self):
        with patch("api.requests.get", return_value=_mock_response(status_code=500)):
            with pytest.raises(requests.exceptions.HTTPError):
                get_location_by_zipcode("78701")


# ---------------------------------------------------------------------------
# get_current_location
# ---------------------------------------------------------------------------


class TestGetCurrentLocation:
    VALID_RESPONSE = {
        "status": "success",
        "city": "Seattle",
        "regionName": "Washington",
        "lat": 47.6062,
        "lon": -122.3321,
    }

    def test_returns_current_location(self):
        with patch(
            "api.requests.get",
            return_value=_mock_response(json_data=self.VALID_RESPONSE),
        ):
            result = get_current_location()
        assert result["city"] == "Seattle"
        assert result["state"] == "Washington"
        assert result["lat"] == pytest.approx(47.6062)
        assert result["lon"] == pytest.approx(-122.3321)

    def test_api_failure_status_raises_runtime_error(self):
        with patch(
            "api.requests.get",
            return_value=_mock_response(
                json_data={"status": "fail", "message": "private range"}
            ),
        ):
            with pytest.raises(
                RuntimeError, match="Unable to determine current location"
            ):
                get_current_location()

    def test_connection_error_raises_runtime_error(self):
        with patch(
            "api.requests.get",
            side_effect=requests.exceptions.ConnectionError,
        ):
            with pytest.raises(RuntimeError, match="Unable to connect"):
                get_current_location()


# ---------------------------------------------------------------------------
# get_weather
# ---------------------------------------------------------------------------


class TestGetWeather:
    VALID_RESPONSE = {
        "current_weather": {
            "temperature": 72.5,
            "weathercode": 0,
        }
    }

    def test_returns_temperature_and_condition(self):
        with patch(
            "api.requests.get",
            return_value=_mock_response(json_data=self.VALID_RESPONSE),
        ):
            result = get_weather(30.27, -97.74)
        assert result["temperature_f"] == 72.5
        assert result["condition"] == "clear sky"

    def test_unknown_weather_code_returns_fallback(self):
        response_data = {"current_weather": {"temperature": 50.0, "weathercode": 999}}
        with patch(
            "api.requests.get", return_value=_mock_response(json_data=response_data)
        ):
            result = get_weather(30.27, -97.74)
        assert "unknown conditions" in result["condition"]
        assert "999" in result["condition"]

    def test_all_known_wmo_codes_resolve(self):
        for code, description in WMO_CONDITIONS.items():
            response_data = {
                "current_weather": {"temperature": 60.0, "weathercode": code}
            }
            with patch(
                "api.requests.get", return_value=_mock_response(json_data=response_data)
            ):
                result = get_weather(0, 0)
            assert result["condition"] == description

    def test_connection_error_raises_runtime_error(self):
        with patch(
            "api.requests.get",
            side_effect=requests.exceptions.ConnectionError,
        ):
            with pytest.raises(RuntimeError, match="Unable to connect"):
                get_weather(30.27, -97.74)

    def test_server_error_raises_http_error(self):
        with patch("api.requests.get", return_value=_mock_response(status_code=500)):
            with pytest.raises(requests.exceptions.HTTPError):
                get_weather(30.27, -97.74)


# ---------------------------------------------------------------------------
# CLI: where-is command
# ---------------------------------------------------------------------------


class TestWhereIsCommand:
    ZIPCODE_DATA = {
        "places": [
            {
                "place name": "Portland",
                "state": "Oregon",
                "latitude": "45.5051",
                "longitude": "-122.675",
            }
        ]
    }
    CURRENT_LOC_DATA = {
        "status": "success",
        "city": "Denver",
        "regionName": "Colorado",
        "lat": 39.7392,
        "lon": -104.9903,
    }

    def test_where_is_with_zipcode(self):
        runner = CliRunner()
        with patch(
            "api.requests.get", return_value=_mock_response(json_data=self.ZIPCODE_DATA)
        ):
            result = runner.invoke(cli, ["where-is", "--zipcode", "97201"])
        assert result.exit_code == 0
        assert "Portland" in result.output
        assert "Oregon" in result.output

    def test_where_is_without_zipcode_uses_current_location(self):
        runner = CliRunner()
        with patch(
            "api.requests.get",
            return_value=_mock_response(json_data=self.CURRENT_LOC_DATA),
        ):
            result = runner.invoke(cli, ["where-is"])
        assert result.exit_code == 0
        assert "Denver" in result.output
        assert "Colorado" in result.output

    def test_where_is_invalid_zipcode_exits_nonzero(self):
        runner = CliRunner()
        with patch("api.requests.get", return_value=_mock_response(status_code=404)):
            result = runner.invoke(cli, ["where-is", "--zipcode", "00000"])
        assert result.exit_code != 0

    def test_where_is_connection_error_exits_nonzero(self):
        runner = CliRunner()
        with patch("api.requests.get", side_effect=requests.exceptions.ConnectionError):
            result = runner.invoke(cli, ["where-is", "--zipcode", "97201"])
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# CLI: current command
# ---------------------------------------------------------------------------


class TestCurrentCommand:
    ZIPCODE_DATA = {
        "places": [
            {
                "place name": "Chicago",
                "state": "Illinois",
                "latitude": "41.8781",
                "longitude": "-87.6298",
            }
        ]
    }
    CURRENT_LOC_DATA = {
        "status": "success",
        "city": "Miami",
        "regionName": "Florida",
        "lat": 25.7617,
        "lon": -80.1918,
    }
    WEATHER_DATA = {
        "current_weather": {
            "temperature": 68.0,
            "weathercode": 2,
        }
    }

    def test_current_with_zipcode(self):
        runner = CliRunner()
        responses = [
            _mock_response(json_data=self.ZIPCODE_DATA),
            _mock_response(json_data=self.WEATHER_DATA),
        ]
        with patch("api.requests.get", side_effect=responses):
            result = runner.invoke(cli, ["current", "--zipcode", "60601"])
        assert result.exit_code == 0
        assert "68.0" in result.output
        assert "partly cloudy" in result.output
        assert "Chicago" in result.output

    def test_current_without_zipcode_uses_current_location(self):
        runner = CliRunner()
        responses = [
            _mock_response(json_data=self.CURRENT_LOC_DATA),
            _mock_response(json_data=self.WEATHER_DATA),
        ]
        with patch("api.requests.get", side_effect=responses):
            result = runner.invoke(cli, ["current"])
        assert result.exit_code == 0
        assert "Miami" in result.output
        assert "68.0" in result.output

    def test_current_invalid_zipcode_exits_nonzero(self):
        runner = CliRunner()
        with patch("api.requests.get", return_value=_mock_response(status_code=404)):
            result = runner.invoke(cli, ["current", "--zipcode", "00000"])
        assert result.exit_code != 0

    def test_current_weather_api_failure_exits_nonzero(self):
        runner = CliRunner()
        responses = [
            _mock_response(json_data=self.ZIPCODE_DATA),
            _mock_response(status_code=500),
        ]
        with patch("api.requests.get", side_effect=responses):
            result = runner.invoke(cli, ["current", "--zipcode", "60601"])
        assert result.exit_code != 0

    def test_current_connection_error_exits_nonzero(self):
        runner = CliRunner()
        with patch("api.requests.get", side_effect=requests.exceptions.ConnectionError):
            result = runner.invoke(cli, ["current"])
        assert result.exit_code != 0
