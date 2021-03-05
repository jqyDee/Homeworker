# Import
import logging
import schedule
import time
import os
import json
import os.path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from os import path


class HomeworkerBot:

    def __init__(self):
        # Time
        self.now = time.strftime("%d-%m-%Y-%H-%M")

        # Logging
        self.logging()

        # Web Driver
        options = Options()
        options.add_argument('')
        self.driver = webdriver.Firefox(executable_path=r"./geckodriver.exe", options=options,
                                   log_path="./logs/geckodriver" + self.now
                                            + ".log")
        self.driver.get("https://homeworker.li/auth")

        # Code
        self.runSchedule()

    # Functions
    def logging(self):
        currentDir = os.getcwd()
        finalDir = os.path.join(currentDir, r'logs')
        if not path.exists(finalDir):
            os.makedirs(finalDir)

        logging.basicConfig(filename="./logs/main" + self.now + ".log",
                            format=' [ %(asctime)s ] [ %(levelname)s ] %(message)s',
                            encoding="utf-8", level=logging.DEBUG)

    def login(self):
        os.system("cls")

        try:
            with open("LoginInfo.json", "r") as f:
                LoginData = json.load(f)
                username = LoginData["username"]
                pw = LoginData["pw"]
                f.close()
            print(username + " ; " + pw)
        except:
            username = str(input("E-Mail: "))
            pw = str(input("Passwort: "))
            jsonDict = {"username": username, "pw": pw}
            print(username + " ; " + pw)
            with open("LoginInfo.json", "w") as f:
                json.dump(jsonDict, f)
                f.close()

        print("Logging in!")
        time.sleep(5)

        # Accept Cookies
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[6]/span[2]").click()

        time.sleep(5)

        # Type Username
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/form/div/input").send_keys(username, Keys.RETURN)

        time.sleep(5)

        # Type Password
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/form/div/input").send_keys(pw, Keys.RETURN)

        logging.info("Succesfully Logged in!")
        print("Logged in!")

        time.sleep(10)

        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass

        time.sleep(10)
        self.driver.refresh()
        time.sleep(5)
        os.system("cls")

    def writeInChat(self, ChatFach, msg="Morgen"):
        print("Start Writing MSG to Chat: " + ChatFach + "!")
        self.driver.refresh()
        time.sleep(10)

        # Go to Chat
        self.driver.find_element_by_xpath("/html/body/div[25]/div[3]/nav/a[3]").click()

        time.sleep(5)

        # Go in Last Written Chat
        self.driver.find_element_by_xpath("//*[contains(text(), '" + ChatFach + "')]").click()

        time.sleep(5)

        # Send Message in Chat
        self.driver.find_element_by_xpath("//*[@id='new-text-message']").send_keys(msg, Keys.RETURN)

        chatName = self.driver.find_element_by_xpath("//*[@id='chat-name']").text
        timeNow = time.strftime("%H:%M")
        print("Message: '" + msg + "' send to Chat: '" + str(chatName) + "' at: '" + timeNow + "'")
        logging.info("Message: '" + msg + "' send to Chat: '" + str(chatName) + "' at: '" + timeNow + "'")
        time.sleep(5)
        self.driver.back()

    def runSchedule(self):
        self.login()

        # Montag - Done
        schedule.every().monday.at("08:03").do(lambda: self.writeInChat("10b Französisch Granet"))  # Franze
        schedule.every().monday.at("08:47").do(lambda: self.writeInChat("10B Deutsch Pfeiffer"))  # Deutsch
        schedule.every().monday.at("09:47").do(lambda: self.writeInChat("Chemie 10b"))  # Chemie
        schedule.every().monday.at("11:33").do(
            lambda: self.writeInChat("10b_Sozialkunde/Geschichte_Mayer"))  # Geschichte/Sozi

        # Dienstag - Done
        schedule.every().tuesday.at("08:03").do(lambda: self.writeInChat("10b Mathe scf"))  # Mathe
        schedule.every().tuesday.at("09:47").do(lambda: self.writeInChat("10b Bio Mössinger"))  # Biologie
        schedule.every().tuesday.at("11:33").do(lambda: self.writeInChat("10b Englisch Janker", "Morning"))  # Englisch

        # Mittwoch - Done
        schedule.every().wednesday.at("08:03").do(lambda: self.writeInChat("10b wr und geo"))  # Wirtschaft und Recht
        schedule.every().wednesday.at("09:47").do(lambda: self.writeInChat("10B Deutsch Pfeiffer"))  # Deutsch
        schedule.every().wednesday.at("11:33").do(lambda: self.writeInChat("10b_Informatik_Ziegenaus"))  # Informatik

        # Donnerstag - Done
        schedule.every().thursday.at("08:03").do(lambda: self.writeInChat("10b Französisch Granet"))  # Franze
        schedule.every().thursday.at("09:47").do(lambda: self.writeInChat("Kunst 10b"))  # Kunst
        schedule.every().thursday.at("10:33").do(lambda: self.writeInChat("10b Musik Schäfer"))  # Musik
        schedule.every().thursday.at("11:33").do(lambda: self.writeInChat("10b Physik"))  # Physik Übung
        schedule.every().thursday.at("12:17").do(lambda: self.writeInChat("Chemie 10b"))  # Chemie Übung

        # Freitag - Done
        schedule.every().friday.at("08:03").do(lambda: self.writeInChat("10b Physik"))  # Physik
        schedule.every().friday.at("09:47").do(lambda: self.writeInChat("10b Mathe scf"))  # Mathe
        schedule.every().friday.at("10:33").do(lambda: self.writeInChat("10b Englisch Janker", "Morning"))  # Englisch
        schedule.every().friday.at("11:33").do(lambda: self.writeInChat("10b wr und geo"))  # Geographie

        # Run
        logging.info("Schedule Running!")
        print("Schedule Running!")
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__== "__main__":
    HomeworkerBot()