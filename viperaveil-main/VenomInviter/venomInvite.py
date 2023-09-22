import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException , TimeoutException

#User Model from Spectrum API reduced to important parts
class User(object):
    def __init__(self, nickname, displayname, online):
        self.nickname = nickname
        self.displayname = displayname
        self.online = online

def getOnlineUsers():
    uri = "https://robertsspaceindustries.com/api/spectrum/lobby/presences"
    body = {"lobby_id":  "1"}
    response = requests.post(uri, data=body)
    listToSPam = []
    if response.status_code == 200:
        #convert response to json
        onlineUsers = response.json()["data"]
        #limit to 100 users
        first100Users = onlineUsers[0:100]
        #check if user is online, not a CIG user, not a GM and speaks english
        for user in first100Users:
            isCIgUser = False
            if "CIG" in user["nickname"]:
                isCIgUser = True
            isEnglish = False
            for language in user["spoken_languages"]:
                if language == "en":
                    isEnglish = True
            #add User to list if all conditions are met
            if user["presence"]["status"] == "online" and isCIgUser == False and user["isGM"] == False and isEnglish:
                user1 = User(user["nickname"], user["displayname"],
                             user["presence"]["status"])
                listToSPam.append(user1)

    return listToSPam

# reduce the list to 100 users who are online
listOfUsersToSpam = getOnlineUsers()

#Install correct ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
#Open RSI and login
driver.get("https://robertsspaceindustries.com/orgs/VNMSQD")
#Find Account Button and click
driver.find_element(
    By.XPATH, "/html/body/div[2]/header[1]/div[1]/section/div/nav/ul[2]/li[3]/a").click()
driver.implicitly_wait(5) 
#Fill Email and Password
driver.find_element(
    By.XPATH, '//*[@id="email"]').send_keys("<USERNAME>")
driver.implicitly_wait(15)
driver.find_element(
    By.XPATH, '//*[@id="password"]').send_keys("<PASSWORD>")
driver.implicitly_wait(15)  # seconds
driver.find_element(By.XPATH, '//*//*[@id="remember"]').click()
#wait to handle 2fa
driver.implicitly_wait(15)  # seconds
driver.implicitly_wait(60)  # seconds
#click Admin
driver.find_element(
    By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/ul/li[4]/a").click()
driver.implicitly_wait(15)  # seconds
# click on recruitment
driver.find_element(
    By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div[2]/div[1]/ul/li[4]/a").click()
# click Invitations
driver.find_element(
    By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div[3]/ul/li[3]/a").click()
driver.implicitly_wait(15)  # seconds
#Loop through all users and invite them
for user in listOfUsersToSpam:
    #Print user to console
    print(user.nickname, user.displayname)
    #Fill in user name
    driver.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div[3]/section/form/fieldset[1]/div/div/div/input[1]").send_keys(f"{user.nickname}")
    driver.implicitly_wait(1) 
    # Wait for the element to be present on the page
    wait = WebDriverWait(driver, 5)
    #try click user pending popup
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="users-pending"]/div/div/div[2]/div/ul/li')))
    except TimeoutException:
        #if not found in time click to close popup
        element = driver.find_element(By.XPATH, '//*[@id="users-pending"]/div/div/div[2]')
    # Interact with the element
    try:
        driver.implicitly_wait(2) 
        element.click()
    except StaleElementReferenceException:
        # If the element is stale, wait for it to be present again and retry the operation
        try:
            element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="users-pending"]/div/div/div[2]/div/ul/li')))      
            element.click()
        except TimeoutException:
            #if not found in time click to close popup
            element = driver.find_element(By.XPATH, '//*[@id="users-pending"]/div/div/div[2]')
            element.click()
            driver.refresh()
    #click invite        
    driver.find_element(By.XPATH, '//*[@id="invites"]/fieldset[2]/div/a[1]').click()
    driver.implicitly_wait(3) 
    driver.refresh()


driver.quit()
