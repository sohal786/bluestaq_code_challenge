# Assessment Submission

This repository contains solutions for two assessment problems: a JavaScript project and a Python elevator simulation.

## Section 1: The Poet: JavaScript Project (app folder)

### Expanded Functionality and Features:
#### Features:
- Real-time search suggestions or auto-suggest search
- Saving user search history
- Having an option to store favorite poems and authors
- Improvements in UI and output Divs

#### Code Improvements:
- Retry mechanism for API call (trying to send requests to the server multiple times if the initial one doesn't work)
- Currently logging errors to the console but can optionally log to a remote logging service for better debugging
- Do another fetch call to an alternative database to improve user experience in case the primary API fails
- Showing better UI when an HTTP error occurs

### How to Run
**Using VS Code Live Server**:
- Open the project in VS Code and make sure all files (`index.html`, `script.js`, `errorHandler.js`, and `style.css`) are in the same folder.
- Right-click `index.html` and select "Open with Live Server".

**Using a Browser**:
- Locate the `index.html` file and double-click on it to open it in your default browser.

### Dependencies
- No dependencies required to install

## Section 2: Elevator Simulation 

### Assumptions:
- Single elevator is simulated (In real life, there could be a multiple elevator system, which would involve a more complex algorithm considering different heuristics for each user request.)
- No real-time request processing (i.e., all requests are queued and then processed so no user can add a request while the elevator is in motion; in real life, an elevator can be requested while in motion so that it knows the current floor of the user who requested)
- No consideration for weight or the number of people in the elevator (this simulation does not account for overall weight and the number of people that can be on the elevator at once)

### Features That Could Possibly Be Implemented:
- Multiple elevator system
- An exit button that shuts down the elevator when someone has an emergency (so the elevator would stop at the nearest floor level)
- Having a base floor like the Ground floor or Lobby to increase efficiency (so the elevator would come to this floor when idle as the majority of requests come from here)

### Improvements in Current Code:
- Add robust unit tests for `call_elevator` and `process_requests` functions (I currently used log statements to check their functionality, but unit tests would ensure they work when we change some logic in these functions. Example: we can add a test to check if requests are added properly for each queue.)
- Make the animation stop at each target floor of requests (Currently, the animation just shows the elevator movement to visualize the logic, but it will be better in terms of UI if it stops at each floor to imitate a real-life elevator)

### How to Run:
- Make sure to have Python installed on your system and your environment set up
- Install `matplotlib` using pip or brew:
  ```bash
  pip install matplotlib

- Navigate to the directory that contains elevator.py file and run this command
   ```bash
 python elevator.py    
