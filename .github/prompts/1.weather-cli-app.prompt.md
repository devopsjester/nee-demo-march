# Weather CLI App Instructions

## App Overview
Create a new Command Line Interface (CLI) application named "weather".
The application will be written in Python and use the Click CLI library.

## Commands

### 1. `where-is`
   - **Functionality:** This command will display the city and state for a given location.
   - **Arguments/Switches:**
     - `--zipcode <zipcode>`: An optional switch to specify the zip code.
   - **Behavior:**
     - If a `--zipcode` is provided, the command should determine the city and state based on that zip code.
     - If no `--zipcode` is provided, the command should attempt to determine the current location of the user and display its city and state.
   - **Output Format:**
     - If zipcode is provided: "`<zipcode>` is in `<city>`, `<state>`."
     - If current location is used: "Your current location is `<city>`, `<state>`." (or similar, if zipcode cannot be determined for current location)

### 2. `current`
   - **Functionality:** This command will display the current temperature (in imperial units - Fahrenheit) and weather conditions for a given location.
   - **Arguments/Switches:**
     - `--zipcode <zipcode>`: An optional argument to specify the zip code.
   - **Behavior:**
     - If a `--zipcode` is provided, the command should fetch and display the current weather conditions for that zip code.
     - If no `--zipcode` is provided, the command should attempt to determine the current location of the user and display its current weather conditions.
   - **Output Format:** "It is currently `<temperature>`ºF, and `<weather condition>` in `<city>`, `<state>`."

## General Requirements
- **Python Version:** Use Python 3.7 or higher.
- **CLI Framework:** Use Click.
- **Dependencies:** All necessary Python dependencies should be listed in a `requirements.txt` file.
- **Error Handling:** Implement basic error handling (e.g., for invalid zip codes, API request failures, inability to determine current location).
- **API Usage:**
    - Use free APIs that do not require registration or API keys for basic functionality.
    - If an API requires a key, provide clear instructions on how a user can obtain and configure it (though preference is for keyless APIs).
- **Modularity:** Structure the code logically, potentially separating API interaction logic from the CLI command definitions.
- **README:** Include a `README.md` file with instructions on how to install, configure (if necessary), and use the application.