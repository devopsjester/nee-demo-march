import pytest
from unittest.mock import patch
from click.testing import CliRunner
from weather import cli


LOC_ZIPCODE = {
    "city": "Beverly Hills",
    "state": "California",
    "lat": 34.09,
    "lon": -118.41,
}
LOC_CURRENT = {
    "city": "Austin",
    "state": "Texas",
    "lat": 30.27,
    "lon": -97.74,
}
WEATHER_DATA = {"temperature_f": 72.5, "condition": "partly cloudy"}
AIR_DATA = {"aqi": 42, "category": "Good"}


@pytest.fixture
def runner():
    return CliRunner()


# ---------------------------------------------------------------------------
# where-is command
# ---------------------------------------------------------------------------

class TestWhereIsCommand:
    def test_with_zipcode(self, runner):
        with patch("weather.get_location_by_zipcode", return_value=LOC_ZIPCODE):
            result = runner.invoke(cli, ["where-is", "--zipcode", "90210"])
        assert result.exit_code == 0
        assert "Beverly Hills" in result.output
        assert "California" in result.output

    def test_without_zipcode_uses_current_location(self, runner):
        with patch("weather.get_current_location", return_value=LOC_CURRENT):
            result = runner.invoke(cli, ["where-is"])
        assert result.exit_code == 0
        assert "Austin" in result.output
        assert "Texas" in result.output

    def test_invalid_zipcode_exits_with_error(self, runner):
        with patch("weather.get_location_by_zipcode", side_effect=ValueError("Invalid or unknown zip code: 00000")):
            result = runner.invoke(cli, ["where-is", "--zipcode", "00000"])
        assert result.exit_code == 1

    def test_connection_error_exits_with_error(self, runner):
        with patch("weather.get_location_by_zipcode", side_effect=RuntimeError("Unable to connect")):
            result = runner.invoke(cli, ["where-is", "--zipcode", "90210"])
        assert result.exit_code == 1


# ---------------------------------------------------------------------------
# current command
# ---------------------------------------------------------------------------

class TestCurrentCommand:
    def test_with_zipcode(self, runner):
        with patch("weather.get_location_by_zipcode", return_value=LOC_ZIPCODE), \
             patch("weather.get_weather", return_value=WEATHER_DATA):
            result = runner.invoke(cli, ["current", "--zipcode", "90210"])
        assert result.exit_code == 0
        assert "72.5" in result.output
        assert "partly cloudy" in result.output
        assert "Beverly Hills" in result.output
        assert "California" in result.output

    def test_without_zipcode_uses_current_location(self, runner):
        with patch("weather.get_current_location", return_value=LOC_CURRENT), \
             patch("weather.get_weather", return_value=WEATHER_DATA):
            result = runner.invoke(cli, ["current"])
        assert result.exit_code == 0
        assert "72.5" in result.output
        assert "Austin" in result.output

    def test_invalid_zipcode_exits_with_error(self, runner):
        with patch("weather.get_location_by_zipcode", side_effect=ValueError("Invalid or unknown zip code")):
            result = runner.invoke(cli, ["current", "--zipcode", "00000"])
        assert result.exit_code == 1

    def test_weather_service_error_exits_with_error(self, runner):
        with patch("weather.get_location_by_zipcode", return_value=LOC_ZIPCODE), \
             patch("weather.get_weather", side_effect=RuntimeError("Unable to connect to the weather service")):
            result = runner.invoke(cli, ["current", "--zipcode", "90210"])
        assert result.exit_code == 1


# ---------------------------------------------------------------------------
# aqi command
# ---------------------------------------------------------------------------

class TestAqiCommand:
    def test_with_zipcode(self, runner):
        with patch("weather.get_location_by_zipcode", return_value=LOC_ZIPCODE), \
             patch("weather.get_air_quality", return_value=AIR_DATA):
            result = runner.invoke(cli, ["aqi", "--zipcode", "90210"])
        assert result.exit_code == 0
        assert "Beverly Hills" in result.output
        assert "California" in result.output
        assert "42" in result.output
        assert "Good" in result.output

    def test_without_zipcode_uses_current_location(self, runner):
        with patch("weather.get_current_location", return_value=LOC_CURRENT), \
             patch("weather.get_air_quality", return_value=AIR_DATA):
            result = runner.invoke(cli, ["aqi"])
        assert result.exit_code == 0
        assert "Austin" in result.output
        assert "Texas" in result.output
        assert "42" in result.output
        assert "Good" in result.output

    def test_invalid_zipcode_exits_with_error(self, runner):
        with patch("weather.get_location_by_zipcode", side_effect=ValueError("Invalid or unknown zip code")):
            result = runner.invoke(cli, ["aqi", "--zipcode", "00000"])
        assert result.exit_code == 1

    def test_air_quality_service_error_exits_with_error(self, runner):
        with patch("weather.get_location_by_zipcode", return_value=LOC_ZIPCODE), \
             patch("weather.get_air_quality", side_effect=RuntimeError("Unable to connect to the air quality service")):
            result = runner.invoke(cli, ["aqi", "--zipcode", "90210"])
        assert result.exit_code == 1

    def test_aqi_output_format(self, runner):
        air = {"aqi": 175, "category": "Unhealthy"}
        with patch("weather.get_current_location", return_value=LOC_CURRENT), \
             patch("weather.get_air_quality", return_value=air):
            result = runner.invoke(cli, ["aqi"])
        assert result.exit_code == 0
        assert "175" in result.output
        assert "Unhealthy" in result.output
