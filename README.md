# weather — Weather CLI App

A command-line tool to look up your location and current weather conditions. Built with Python and [Click](https://click.palletsprojects.com/).

## APIs Used

All APIs are free and require no registration or API keys:

| Purpose                  | API                                        |
| ------------------------ | ------------------------------------------ |
| Location from IP address | [ip-api.com](http://ip-api.com)            |
| City/state from zip code | [zippopotam.us](https://api.zippopotam.us) |
| Weather data             | [open-meteo.com](https://open-meteo.com)   |
| Air quality data         | [open-meteo.com](https://open-meteo.com)   |

## Installation

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Usage

All commands are run via `python3 weather.py`.

### `where-is`

Displays the city and state for a given location.

```bash
# Use current location (detected from your IP address)
python3 weather.py where-is

# Look up a specific US zip code
python3 weather.py where-is --zipcode 90210
```

**Example output:**

```
90210 is in Beverly Hills, California.
Your current location is Austin, Texas.
```

### `current`

Displays the current temperature (°F) and weather conditions.

```bash
# Use current location
python3 weather.py current

# Look up a specific US zip code
python3 weather.py current --zipcode 10001
```

**Example output:**

```
It is currently 72.5ºF, and partly cloudy in New York, New York.
```

### `aqi`

Displays the current air quality index (US AQI) and category.

```bash
# Use current location
python3 weather.py aqi

# Look up a specific US zip code
python3 weather.py aqi --zipcode 90210
```

**Example output:**

```
The air quality in Beverly Hills, California is 42 (Good).
```

## Project Structure

```
weather.py      # CLI entry point (Click commands)
api.py          # API interaction logic
requirements.txt
```
