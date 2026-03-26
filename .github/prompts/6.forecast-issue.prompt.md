# GitHub Issue: Implement 'forecast' Command

## Issue Title
Feature: Add `forecast` command to display multi-day weather forecast

## Issue Description

### Background
The current weather CLI application provides functionality to get the current location (`where-is`) and the current weather conditions (`current`). A valuable addition would be to allow users to see the weather forecast for the upcoming days.

### Feature Request
Implement a new command called `forecast` that displays a multi-day weather forecast (e.g., for the next 3 or 5 days) for a specified location.

### Justification
- **User Value:** Provides users with more comprehensive weather information, allowing them to plan ahead.
- **Completeness:** Complements the existing `current` weather command, making the app a more rounded weather tool.
- **Common Functionality:** Weather forecasts are a standard feature in most weather applications.

## Suggested Command Structure
```
weather forecast [--zipcode <zipcode>] [--days <number_of_days>]
```
- `--zipcode <zipcode>`: Optional. If provided, fetch forecast for this zipcode. If omitted, use current location.
- `--days <number_of_days>`: Optional. Number of days for the forecast (e.g., 1 to 7). Default to 3 or 5 days if not specified.

## Expected Output Format
The output should be clear and easy to read. For each day in the forecast, display:
- Date (e.g., "Tomorrow", "YYYY-MM-DD", or day of the week)
- High temperature (in Fahrenheit)
- Low temperature (in Fahrenheit)
- Weather condition (e.g., "Sunny", "Partly Cloudy", "Rain")

**Example Output (for a 3-day forecast):**
```
Forecast for <City>, <State>:

Tuesday, June 11:
  High: 75ºF, Low: 60ºF
  Conditions: Sunny

Wednesday, June 12:
  High: 72ºF, Low: 58ºF
  Conditions: Partly Cloudy

Thursday, June 13:
  High: 68ºF, Low: 55ºF
  Conditions: Chance of Rain
```
*(Adjust date formatting and details based on API capabilities and desired clarity)*

## Acceptance Criteria
1.  A new command `weather forecast` is available.
2.  The command accepts an optional `--zipcode` argument.
    - If `--zipcode` is provided, the forecast for that zipcode is displayed.
    - If `--zipcode` is not provided, the forecast for the user's current location is displayed.
3.  The command accepts an optional `--days` argument to specify the number of forecast days (e.g., 1-7).
    - If `--days` is not provided, a default number of days (e.g., 3 or 5) is used.
4.  Output displays the date, high temperature (ºF), low temperature (ºF), and weather condition for each forecast day.
5.  Appropriate error handling is implemented:
    - Invalid zipcode format.
    - Zipcode not found by the API.
    - Failure to determine current location (if no zipcode provided).
    - API request failures for forecast data.
    - Invalid value for `--days` (e.g., non-numeric, out of acceptable range).
6.  The chosen weather API for forecast data must be free and not require registration or an API key, aligning with existing project constraints.
7.  The `requirements.txt` file is updated with any new dependencies.
8.  Inline documentation (docstrings) is added for new functions/methods.
9.  The `README.md` is updated to include documentation for the new `forecast` command, including usage examples.
10. Automated tests (`pytest`) are written for the `forecast` command, covering various scenarios (valid/invalid zipcode, current location, different `--days` values, API mocking).

## Technical Considerations
- **API Selection:** A crucial step will be to find a suitable free, keyless API that provides multi-day forecast data. This API should ideally return:
    - Daily high/low temperatures.
    - A textual description of weather conditions.
    - Data parseable by date.
- **Current Location:** Leverage existing mechanisms for determining current location if no zipcode is provided.
- **Modularity:** Implement the forecast fetching logic in the `services/weather_api.py` module or a similar appropriate location.
- **Output Formatting:** Ensure the output is well-formatted and readable in a terminal.

## Tasks
- Research and select a suitable free, keyless weather API for forecast data.
- Implement the `forecast` command logic in `commands/forecast.py` (or a new file).
- Integrate API calls into `services/weather_api.py`.
- Add error handling and user feedback.
- Write unit tests for the new command.
- Update `README.md` with usage instructions.
- Update `requirements.txt` if necessary.
