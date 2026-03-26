# Weather Data MCP Server Implementation

## Overview
Create a Model Context Protocol (MCP) server that provides weather data tools and resources. This server will act as a centralized weather data provider that can be consumed by multiple applications, including the existing weather CLI app.

## Requirements

### Core MCP Server Setup
- Implement using Python and the `mcp` library
- Follow MCP protocol specifications for server implementation
- Use only free APIs that don't require registration or tokens
- Provide proper error handling and logging

### Weather Data Sources
**Primary API: Open-Meteo (openmeteo.com)**
- Free, no registration required
- Provides current weather and forecasts
- Supports geocoding for location lookup
- RESTful JSON API

**Backup API: wttr.in**
- Simple weather API
- No registration required
- Multiple output formats available

### MCP Tools to Implement

1. **get_current_weather**
   - Parameters: `location` (string - city, zipcode, or coordinates)
   - Returns: Current temperature, conditions, humidity, wind speed
   - Error handling for invalid locations

2. **get_weather_forecast** 
   - Parameters: `location` (string), `days` (integer, 1-7)
   - Returns: Multi-day forecast with high/low temps, conditions
   - Default to 3 days if not specified

3. **get_location_info**
   - Parameters: `query` (string - zipcode, city name, coordinates)
   - Returns: Resolved location name, coordinates, timezone
   - Use geocoding to standardize location data

4. **get_weather_alerts**
   - Parameters: `location` (string)
   - Returns: Any active weather warnings or alerts
   - Return empty list if no alerts available

5. **get_weather_history**
   - Parameters: `location` (string), `date` (string YYYY-MM-DD)
   - Returns: Historical weather data for specific date
   - Limited to past 30 days due to API constraints

### MCP Resources to Provide

1. **weather_stations**
   - List of nearby weather stations for a location
   - Include station ID, name, distance

2. **climate_data**
   - Monthly climate averages for locations
   - Temperature ranges, precipitation averages

3. **weather_codes**
   - Mapping of weather condition codes to descriptions
   - Support for multiple weather APIs

### Server Configuration
- Listen on configurable host/port (default: localhost:8000)
- Support both stdio and TCP transport methods
- Include comprehensive logging with different log levels
- Configuration file support for API endpoints and settings

### Error Handling
- Graceful handling of API rate limits
- Fallback between different weather APIs
- Proper error messages for invalid locations
- Timeout handling for API requests

### Data Validation
- Validate location inputs (coordinates, zipcodes, city names)
- Sanitize and normalize location strings
- Validate date ranges for historical data
- Check forecast day limits

### Response Format
- Consistent JSON structure across all tools
- Include metadata (source API, timestamp, location coordinates)
- Human-readable weather descriptions
- Appropriate units (Celsius/Fahrenheit, km/h or mph for wind)

## Integration with Existing CLI
The weather CLI app should be modified to:
- Connect to the MCP server as a client
- Use MCP tools instead of direct API calls
- Demonstrate the benefit of centralized weather data access
- Show how multiple applications can share the same weather backend

## File Structure
```
mcp-weather-server/
├── requirements.txt
├── server.py (main MCP server implementation)
├── weather_apis.py (API client classes)
├── location_utils.py (geocoding and location helpers)
├── config.py (server configuration)
├── README.md
└── examples/
    ├── client_example.py
    └── cli_integration.py
```

## Dependencies (requirements.txt)
- mcp (Model Context Protocol library)
- httpx (async HTTP client)
- pydantic (data validation)
- python-dotenv (configuration)
- loguru (enhanced logging)

## Testing Requirements
- Unit tests for all weather API functions
- Integration tests for MCP server functionality
- Mock API responses for reliable testing
- Test error conditions and edge cases

## Documentation
- Comprehensive README with setup instructions
- API documentation for all MCP tools
- Examples of client usage
- Configuration options explained

## Demo Script
Create a demonstration that shows:
1. Starting the MCP server
2. Connecting from the CLI app
3. Making weather requests through MCP
4. Showing the same data being accessed by a second client
5. Demonstrating server resilience (API failover)

This MCP server will showcase how the Model Context Protocol can centralize weather data access, making it available to multiple applications while maintaining a clean, standardized interface.
