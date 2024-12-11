import random
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.audio_handler import speech_to_text  # type: ignore

USER_AGENT_LIST = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
]


def get_receipt_url(key: str) -> str:
    def delay() -> None:
        """
        Delay between 3 and 5 seconds
        """
        time.sleep(random.randint(3, 5))

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument(f"user-agent={random.choice(USER_AGENT_LIST)}")
    driver = webdriver.Chrome(options=driver_options)
    driver_wait = WebDriverWait(driver, 10)

    delay()
    driver.get("https://nfce.sefaz.pe.gov.br/nfce-web/entradaConsNfce")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    delay()
    driver.find_element(
        By.XPATH, "/html/body/form/div/div/div/div[2]/div/input"
    ).send_keys(key)
    delay()
    frames = driver.find_elements(By.XPATH, "//iframe")
    driver.switch_to.frame(frames[0])
    delay()
    driver.find_element(By.XPATH, "//*[@id='recaptcha-anchor']").click()

    driver.switch_to.default_content()
    frames = driver.find_element(By.XPATH, "/html/body/div/div[4]").find_elements(
        By.TAG_NAME, "iframe"
    )
    driver.switch_to.frame(frames[0])
    delay()
    driver_wait.until(
        EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
    ).click()
    driver_wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div/button"))
    ).click()
    audio_src = str(driver.find_element(By.ID, "audio-source").get_attribute("src"))
    audio_text = speech_to_text(audio_src)
    delay()

    audio_response = driver.find_element(By.ID, "audio-response")
    audio_response.send_keys(audio_text.lower())
    audio_response.send_keys(Keys.ENTER)
    delay()

    driver.switch_to.default_content()
    driver.find_element(
        By.XPATH, "/html/body/form/div/div/div/div[2]/div[3]/button"
    ).click()
    delay()
    url = str(
        driver.find_element(
            By.XPATH, "html/body/div/div/div/div/div/a[2]"
        ).get_attribute("href")
    )
    driver.quit()
    return url


def get_receipt_xml(url: str) -> BeautifulSoup:
    response = requests.get(url, timeout=None)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "xml")
    return soup


__all__ = ["get_receipt_url", "get_receipt_xml"]
