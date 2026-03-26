# Add Automated Tests to Weather CLI App

## Objective
Implement a comprehensive suite of automated tests for the "weather" CLI application. The tests should ensure the reliability and correctness of all existing commands and their functionalities.

## Testing Framework
- Use `pytest` as the primary testing framework.
- Utilize `pytest-mock` for mocking external dependencies, particularly API calls and current location services.
- Employ Click's `CliRunner` for invoking and testing CLI commands.

## Test Structure
- Create a `tests` directory at the root of the project if it doesn't already exist.
- Inside the `tests` directory, organize test files logically. For example:
    - `test_cli.py` for general CLI structure and top-level command group tests.
    - `test_where_is.py` for tests specific to the `where-is` command.
    - `test_current.py` for tests specific to the `current` command.
- Test files should follow the `test_*.py` naming convention.

## Test Coverage Requirements

### 1. `where-is` Command
   - **Test Scenarios:**
     - Invoking `where-is --zipcode <valid_zipcode>`:
       - Verify correct output format: "`<zipcode>` is in `<city>`, `<state>`."
       - Mock the API call for geolocation and ensure it's called with the correct zipcode.
     - Invoking `where-is` (without zipcode):
       - Mock the current location service.
       - Verify correct output format: "Your current location is `<city>`, `<state>`." (or similar, based on actual implementation).
     - Invoking `where-is --zipcode <invalid_zipcode>`:
       - Mock the API to return an error or no data for the invalid zipcode.
       - Verify appropriate error message and exit code.
     - Invoking `where-is` when current location cannot be determined:
       - Mock the current location service to simulate failure.
       - Verify appropriate error message and exit code.

### 2. `current` Command
   - **Test Scenarios:**
     - Invoking `current --zipcode <valid_zipcode>`:
       - Mock the weather API call and ensure it's called with the correct zipcode.
       - Verify correct output format: "It is currently `<temperature>`ºF, and `<weather condition>` in `<city>`, `<state>`."
       - Ensure temperature is in Fahrenheit.
     - Invoking `current` (without zipcode):
       - Mock the current location service.
       - Mock the weather API call (it might need a geocoded location or a default zipcode based on current location).
       - Verify correct output format.
     - Invoking `current --zipcode <invalid_zipcode>`:
       - Mock the API to return an error or no data for the invalid zipcode.
       - Verify appropriate error message and exit code.
     - Invoking `current` when current location cannot be determined:
       - Mock the current location service to simulate failure.
       - Verify appropriate error message and exit code.
     - Invoking `current` when the weather API call fails:
       - Mock the weather API to simulate a failure (e.g., network error, API down).
       - Verify appropriate error message and exit code.

## Mocking Strategy
- **External API Calls:** All calls to external weather and geolocation APIs **must** be mocked. Tests should not make actual network requests.
- **Current Location Service:** The mechanism for determining the user's current location **must** be mocked to ensure tests are deterministic and can simulate various scenarios (e.g., location found, location not found).

## Dependencies
- Add `pytest` and `pytest-mock` to the `requirements.txt` file.
- Add `pytest` and `pytest-mock` to a `dev-requirements.txt` file for test-only dependencies.
- Ensure the command `python3 -m pip install -r dev-requirements.txt` successfully installs these dependencies.

## Running Tests
- Provide clear instructions in the `README.md` on how to run the tests (e.g., by simply running `pytest` from the project root).
- Tests should be runnable with a single command.

## General Test Practices
- Tests should be independent and not rely on the state of previous tests.
- Test names should be descriptive of the scenario they are testing.
- Use assertions to check for expected outcomes, including output, exit codes, and mocked function calls.
- Ensure tests clean up any resources they create, if applicable (though for CLI apps, this is less common).