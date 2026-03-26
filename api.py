import requests

# WMO Weather Interpretation Codes (open-meteo)
WMO_CONDITIONS = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "icy fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "light snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "light rain showers",
    81: "moderate rain showers",
    82: "heavy rain showers",
    85: "light snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with hail",
    99: "thunderstorm with heavy hail",
}


def get_location_by_zipcode(zipcode):
    """Return city, state, lat, lon for a US zip code via zippopotam.us."""
    url = f"https://api.zippopotam.us/us/{zipcode}"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Unable to connect to the location service. Check your internet connection."
        )
    if response.status_code == 404:
        raise ValueError(f"Invalid or unknown zip code: {zipcode}")
    response.raise_for_status()
    data = response.json()
    place = data["places"][0]
    return {
        "city": place["place name"],
        "state": place["state"],
        "lat": float(place["latitude"]),
        "lon": float(place["longitude"]),
    }


def get_current_location():
    """Return city, state, lat, lon for the current IP address via ip-api.com."""
    url = "http://ip-api.com/json/"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Unable to connect to the location service. Check your internet connection."
        )
    response.raise_for_status()
    data = response.json()
    if data.get("status") != "success":
        raise RuntimeError(
            f"Unable to determine current location: {data.get('message', 'unknown error')}"
        )
    return {
        "city": data["city"],
        "state": data["regionName"],
        "lat": data["lat"],
        "lon": data["lon"],
    }


def get_weather(lat, lon):
    """Return current temperature (°F) and condition string via open-meteo.com."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "temperature_unit": "fahrenheit",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Unable to connect to the weather service. Check your internet connection."
        )
    response.raise_for_status()
    data = response.json()
    current = data["current_weather"]
    temp = current["temperature"]
    code = int(current["weathercode"])
    condition = WMO_CONDITIONS.get(code, f"unknown conditions (code {code})")
    return {
        "temperature_f": temp,
        "condition": condition,
    }


# US AQI category thresholds
AQI_CATEGORIES = [
    (50, "Good"),
    (100, "Moderate"),
    (150, "Unhealthy for Sensitive Groups"),
    (200, "Unhealthy"),
    (300, "Very Unhealthy"),
    (500, "Hazardous"),
]


def get_aqi_category(aqi_value):
    """Return the AQI category label for a given US AQI value."""
    for threshold, category in AQI_CATEGORIES:
        if aqi_value <= threshold:
            return category
    return "Hazardous"


def get_air_quality(lat, lon):
    """Return current US AQI and category via open-meteo.com air quality API."""
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Unable to connect to the air quality service. Check your internet connection."
        )
    response.raise_for_status()
    data = response.json()
    aqi_value = data["current"]["us_aqi"]
    if aqi_value is None:
        raise RuntimeError("Air quality data is not available for this location.")
    return {
        "aqi": aqi_value,
        "category": get_aqi_category(aqi_value),
    }
