from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import json
import time

# Determine environment for the download directory (Docker or local)
def getEnvironmentDownloadDir():
    if os.environ.get("RUNNING_IN_DOCKER") == "1":
        return "/app"
    else:
        homeDir = os.path.expanduser("~")
        return os.path.join(homeDir, "Downloads")

# Set up and return a headless Chrome driver
def getDriver(downloadDir):
    chromeOptions = Options()
    chromeOptions.add_argument("--headless=new")
    # Window size needs only to set for headless mode
    chromeOptions.add_argument("--window-size=1920x1080")
    chromeOptions.add_experimental_option("prefs", {
        "download.default_directory": downloadDir,
        "download.prompt_for_download": False,
    })
    return webdriver.Chrome(options=chromeOptions)

#Funtion to input the user data
def inputInfo(driver,email, firstName, lastName, address, phone, company, role):
    # Create a mapping of field names to their corresponding input values
    fields = {

        'labelEmail': email,
        'labelFirstName': firstName,
        'labelLastName': lastName,
        'labelAddress': address,
        'labelPhone': phone,
        'labelCompanyName': company,
        'labelRole': role,
    }

    # Loop through the fields, input the wanted text eg. name or phone number
    for fieldName, value in fields.items():
        inputElement = driver.find_element(By.XPATH, f"//input[@ng-reflect-name='{fieldName}']")
        # Check if the input form is empty
        valueTest = str(inputElement.get_attribute("value"))
        if valueTest:
            f"The input is not empty, unexpected behaviour"
        # If the field is empty, continue
        inputElement.send_keys(str(value))
        # Verify the value is set correctly
        valueTest = str(inputElement.get_attribute("value"))
        value = str(value).strip()
        assert valueTest == value,  f"Input failed, expected: {value}, found: {valueTest}"

    # Submit the form
    submitButton = driver.find_element(By.XPATH, "//input[@type='submit']")
    submitButton.click()

def main():
    #Get the correct download directory
    downloadDir = getEnvironmentDownloadDir()
    
    #Get the configuration from the config file
    with open("config.json") as f:
        config = json.load(f)

    # Start browser and navigate to the wanted url
    driver = getDriver(downloadDir)
    driver.get(config["url"])

    #Click the start button to start the timer
    startButton= driver.find_element(By.XPATH, "//Button[contains(text(), 'Start')]")
    startButton.click()

    #Download the challenge excel file
    downloadableFile = driver.find_element(By.XPATH, "//*[contains(text(), 'Download')]")
    downloadableFile.click()

    #Get the name of the .xlsx file from config. This can be done directly, because the name is the same always.
    excelFilename = config["filename"]
    downloadPath = os.path.join(downloadDir, excelFilename)

    # Retry checking file for up to 20 seconds. This is done, because file has not always done loading when trying to be read.
    timeout = 20
    interval = 1  
    start_time = time.time()
    # Loop until the filepath exists. If the time is over 20 seconds, it times out and gives error
    while not os.path.exists(downloadPath):
        if time.time() - start_time > timeout:
            raise FileNotFoundError(f"File '{excelFilename}' not found after {timeout} seconds.")
        time.sleep(interval)

    #Read the downloaded file using pandas and remove it after
    df = pd.read_excel(downloadPath)
    os.remove(downloadPath) 

    # Convert excel file to dictionary
    groupedDict= df.to_dict(orient='records')

    # Loop through each row in the excel and input the info to the website. Pass also the driver to the function.
    for row in groupedDict:
        inputInfo(driver,row['Email'],row['First Name'],row['Last Name '],row['Address'],row['Phone Number'],row['Company Name'],row['Role in Company'])

    # Show the succes as print texts
    succesMessage = driver.find_element(By.XPATH, "//*[contains(text(), 'rate')]")
    print(succesMessage.text)

    #close browser
    driver.quit()

if __name__ == "__main__":
    main()