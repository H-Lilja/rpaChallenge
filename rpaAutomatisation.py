from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

with open("config.json") as f:
    config = json.load(f)
#First get the driver and go to the wanted website
driver = webdriver.Chrome(options=Options)
driver.get(config["url"])

#Download the file, TODO ADD XPATH
downloadableFile = driver.find_element(By.XPATH, "")
downloadableFile.click()

def inputInfo(email, firstName, lastName, address, phone, company, role):
    #TODO ADD XPATh
    #After all the info is in the form, press submit
    submitButton = driver.find_element(By.XPATH, "")
    submitButton.click()

for row in dict:
    
    inputInfo()

# Show the succes as info pop up TODO Add XPATH
succesMessage = driver.find_element(By.XPATH, "")
print(succesMessage.text) 
# Optional: close browser
# driver.quit()