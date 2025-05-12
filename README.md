# **RPA Bot for Task Automation with Docker and Selenium**

This project solves the RPA Challenge (https://www.rpachallenge.com/) using Python and Selenium.

## Prerequisites:

Depending on how you want to run the bot, you’ll need:

- Python 3.7+ (if running locally)
- Docker (if running in a container: https://www.docker.com/get-started/)



## Setup Instructions 
### 1. Clone the Repository
   IF USING BASH:
 - git clone https://github.com/H-Lilja/rpaChallenge

```
cd rpaChallenge
```
            
   IF USING GITHUB DESKTOP:
- Download Github desktop https://github.com/apps/desktop 
- Open the app, set it up, and clone the repository.


###   2.A Running (via code editor)
- Open code in wanted code editor. Using terminal in project file, give this command to download dependencies:
```
pip install selenium pandas openpyxl
```
- Run the script either via the editor or give command:
```
python rpaAutomatisation.py
```
###   2.B Running (via docker)
- Install Docker
            Follow the instructions to install Docker for your platform from the official Docker website:
            Docker Installation Guide: https://docs.docker.com/get-started/get-docker/

- Build the Docker Image and run the container
  -To build the Docker image, run the following command in the project directory:
```
docker build -t rpa-python-script .
```
  - This will create a Docker image with the tag rpa-python-script. Then you can run it by writing: 
```
docker run rpa-python-script
```
          
## Configuration
You can modify the url and the filename in the config.json file.

## Output

After successful form submissions, the bot will display a success message from the webpage and close the browser.

## Final Thoughts
The code initiates the browser, clicks the start button, downloads the challenge.xlsx file, and reads it using pandas.

There was some uncertainty about whether the timer should start immediately upon navigating to the website or after the file is downloaded. To capture the total time, I decided to start the timer as soon as the page is accessed.

Once the file is read, it’s converted into a dictionary. The script then loops through each row of the data, inputting the information into the corresponding fields on the website. Before entering any data, the bot verifies that the input fields are empty, as expected. During the input process, the bot also checks that the correct data is entered before proceeding. These checks were implemented as safeguards to ensure the form behaves correctly.

After completing the input for one row, the bot clicks the submit button. Once all 10 rows are processed, the website displays the final time and correct percentage. This result is printed out, since in headless mode it is not visible, and in normal mode, it appears too quickly to be easily readable.

This code runs Chrome in headless mode, meaning the browser UI is not displayed. If you prefer to see the UI, simply comment out the headless option in line 21 of rpaAutomatisation.py.

Alternatively, this behavior could be controlled via a CLI flag, allowing users to choose whether to run in headless mode or not.

As the project grows in complexity, it’s recommended to modularize the code by splitting the functions into separate files. This will improve readability and make the code easier to maintain in the long term.
