import math
import time

from PIL import ImageGrab
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui


class SlitherGame():
    boost = False

    def start_game(self, name: str, width: int, height: int):
        self.driver = webdriver.Chrome("../webdriver/chromedriver.exe")
        self.width = width
        self.height = height
        self.driver.set_window_size(width, height)
        self.driver.set_window_position(100, 100)
        self.driver.get("http://slither.io/")
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[@id=\"nick\"]").send_keys(name)
        self.driver.find_element(By.XPATH, "//*[@id=\"playh\"]/div/div/div[3]").click()

    def restart_game(self):
        try:
            self.driver.find_element(By.XPATH, "//*[@id=\"playh\"]/div/div/div[3]").click()
        except:
            pass

    def set_boost(self, boost: bool):
        self.boost = boost
        if boost:
            pyautogui.keyUp(" ")
            pyautogui.keyDown(" ")
        else:
            pyautogui.keyUp(" ")

    def get_screenshot(self):
        im = ImageGrab.grab()
        im = im.crop((110, 230, 110 + self.width, 90 + self.height))
        return im

    def is_game_running(self) -> bool:
        element = self.driver.find_element(By.XPATH, "//*[text()[contains(.,'Bestenlist')]]")
        opacity = float(element.value_of_css_property("opacity"))
        display = element.value_of_css_property("display")
        return opacity > 0 and display == "block"

    def get_score(self) -> int:
        try:
            element = self.driver.find_element(By.XPATH, "//*[text()[contains(.,'Deine Länge:')]]").find_element(
                By.XPATH, "./..").find_element(By.XPATH, "span[2]")
            return int(element.text)
        except:
            return 0

    def move_angle(self, angle: float):
        center = ((self.width / 2) + 110, (self.height / 2) + 110)
        distance = 100
        header_size = 50
        position = (math.cos(math.radians(angle - 90)) * distance + center[0],
                    math.sin(math.radians(angle - 90)) * distance + center[1] + header_size)
        pyautogui.moveTo(position[0], position[1])

    def close(self):
        self.driver.close()
