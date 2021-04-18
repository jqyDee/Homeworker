import logging
import schedule
import os
import os.path
import json
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import *
from os import path
from getpass import getpass

"""
This Program is writing in the Chats at the start of every lesson (10b).
Python 3 and pip is needed.

Before first execution, execute these 2 commands to be able to run the script:
+ pip install selenium 
+ pip install schedule
"""


class HomeworkerBot:
    def __init__(self):
        # Time
        now = time.strftime("%d-%m-%Y-%H-%M")

        # Logging
        self.check_log_dir()
        logging.basicConfig(filename="./logs/main" + now + ".log",
                            format=' [ %(asctime)s ] [ %(levelname)s ] %(message)s',
                            encoding="utf-8", level=logging.DEBUG)

        # Web Driver
        options = Options()
        options.add_argument('')  # delete/add the Argument('--headless'), to hide/show the browser
        self.driver = webdriver.Firefox(executable_path=r"./src/geckodriver.exe", options=options,
                                        service_log_path="./logs/geckodriver" + now + ".log")
        self.driver.get("https://homeworker.li/auth")

    @staticmethod
    def check_log_dir():
        """
        Checks if the Directory to store the .log files exist
        """

        currentdir = os.getcwd()
        finaldir = os.path.join(currentdir, r'logs')
        if not path.exists(finaldir):
            os.makedirs(finaldir)

    def login(self):
        """
        Logs in with the Login Data stored in LoginInfo.json. It also checks if the
        JSON file is there in if its empty

        + added Fix that Program doesnt crash when homeworker.li is currently unrecheable
        """

        # Checks the Json File of Data
        try:
            with open("./user/data/LoginInfo.json", "r") as f:
                logindata = json.load(f)
                username = logindata["username"]
                pw = logindata["pw"]
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            username = str(input("E-Mail: "))
            pw = str(getpass("Passwort: "))
            jsondict = {"username": username, "pw": pw}
            with open("./user/data/LoginInfo.json", "w") as f:
                json.dump(jsondict, f)

        print("Logging in!")
        time.sleep(5)

        # While and Try loop to prevent crash when homeworker.li is unreachable
        while True:
            try:
                self.driver.refresh()

                try:
                    # Accept Cookies
                    self.driver.find_element_by_xpath("/html/body/div[4]/div/div[6]/span[2]").click()
                except NoSuchElementException:
                    pass

                time.sleep(5)

                # Type Username
                self.driver.find_element_by_xpath("//input[@type='email']").send_keys(username, Keys.RETURN)
                time.sleep(5)

                # Type Password
                self.driver.find_element_by_xpath("//input[@type='password']").send_keys(pw, Keys.RETURN)
                time.sleep(5)

                try:
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    print("Alert accepted")
                    time.sleep(5)
                except NoAlertPresentException:
                    pass

                self.driver.refresh()
                time.sleep(5)

                if self.driver.current_url == "https://homeworker.li/dashboard":
                    logging.info("Succesfully Logged in!")
                    print("Logged in!")
                    os.system("cls")
                    break
            except Exception as e:
                if self.driver.current_url == "https://homeworker.li/dashboard":
                    try:
                        alert = self.driver.switch_to.alert
                        alert.accept()
                        print("Alert accepted")
                        time.sleep(5)
                    except NoAlertPresentException:
                        pass

                    self.driver.refresh()
                    time.sleep(5)

                    logging.info("Succesfully Logged in!")
                    print("Logged in!")
                    os.system("cls")
                    break
                print("Error", e)
                time.sleep(30)
                continue

    def write_to_chat(self, chatfach, msg="Morgen"):
        """
        Function to write the Message in a certain chat.
        """

        run = 0
        while run < 5:
            try:
                print("Start Writing MSG to Chat: " + chatfach + "!")
                self.driver.refresh()
                time.sleep(5)

                # Go to Chat
                self.driver.find_element_by_xpath("/html/body/div[25]/div/nav/a[3]").click()
                time.sleep(5)

                # Go in certain Chat
                self.driver.find_element_by_xpath("//*[contains(text(), '" + chatfach + "')]").click()
                time.sleep(5)

                # Send Message in Chat
                self.driver.find_element_by_xpath("//*[@id='new-text-message']").send_keys(msg, Keys.RETURN)

                chatname = self.driver.find_element_by_xpath("//*[@id='chat-name']").text
                timenow = time.strftime("%H:%M")
                time.sleep(5)
                print("Message: '" + msg + "' send to Chat: '" + str(chatname) + "' at: '" + timenow + "'")
                logging.info("Message: '" + msg + "' send to Chat: '" + str(chatname) + "' at: '" + timenow + "'")
                break
            except Exception as e:
                run += 1
                print("Error writing message(run: " + str(run) + "): ", e)
                time.sleep(30)
                continue

    def start(self):
        """
        Function which is running all the time, to start the write_in_chat Function
        at the right timestamps
        """

        self.login()

        # Montag - Done
        schedule.every().monday.at("08:33").do(lambda: self.write_to_chat("10b Französisch Granet"))  # Franze
        schedule.every().monday.at("09:13").do(lambda: self.write_to_chat("10b Deutsch Gerlach"))  # Deutsch
        schedule.every().monday.at("10:07").do(lambda: self.write_to_chat("Chemie 10b"))  # Chemie
        schedule.every().monday.at("11:43").do(lambda: self.write_to_chat(
                                                            "10b_Sozialkunde/Geschichte_Mayer"))  # Geschichte/Sozi

        # Dienstag - Done
        schedule.every().tuesday.at("08:03").do(lambda: self.write_to_chat("10b Mathe scf"))  # Mathe
        schedule.every().tuesday.at("09:47").do(lambda: self.write_to_chat("10b Bio Mössinger"))  # Biologie
        schedule.every().tuesday.at("11:33").do(lambda: self.write_to_chat("10b Englisch Janker",
                                                                           "Morning"))  # Englisch

        # Mittwoch - Done
        schedule.every().wednesday.at("08:33").do(lambda: self.write_to_chat("10b wr und geo"))  # Wirtschaft und Recht
        schedule.every().wednesday.at("10:07").do(lambda: self.write_to_chat("10b Deutsch Gerlach"))  # Deutsch
        schedule.every().wednesday.at("11:43").do(lambda: self.write_to_chat("10b_Informatik_Ziegenaus"))  # Informatik

        # Donnerstag - Done
        schedule.every().thursday.at("08:03").do(lambda: self.write_to_chat("10b Französisch Granet"))  # Franze
        schedule.every().thursday.at("09:47").do(lambda: self.write_to_chat("Kunst 10b"))  # Kunst
        schedule.every().thursday.at("10:33").do(lambda: self.write_to_chat("10b Musik Schäfer"))  # Musik
        schedule.every().thursday.at("11:33").do(lambda: self.write_to_chat("10b Physik"))  # Physik Übung
        schedule.every().thursday.at("12:17").do(lambda: self.write_to_chat("Chemie 10b"))  # Chemie Übung

        # Freitag - Done
        schedule.every().friday.at("08:33").do(lambda: self.write_to_chat("10b Physik"))  # Physik
        schedule.every().friday.at("10:07").do(lambda: self.write_to_chat("10b Englisch Janker", "Morning"))  # Englisch
        schedule.every().friday.at("10:47").do(lambda: self.write_to_chat("10b Mathe scf"))  # Mathe
        schedule.every().friday.at("11:43").do(lambda: self.write_to_chat("10b wr und geo"))  # Geographie

        # Test
        # schedule.every().sunday.at("22:38").do(lambda: self.write_to_chat("Kunst 10b"))  # Test
        # schedule.every().wednesday.at("12:51").do(lambda: self.write_to_chat("10b Englisch Janker"))  # Test

        # Run Schedule
        logging.info("Schedule Running!")
        print("Schedule Running!")
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    app = HomeworkerBot()
    app.start()
