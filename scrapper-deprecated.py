import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login():
    email_field = driver.find_element(By.ID, "sign-in-form--email")
    email_field.send_keys("demo_estee2@cosmosid.com")

    password_field = driver.find_element(By.ID, "sign-in-form--password")
    password_field.send_keys("xyzfg321")

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()


def extract_urls(trs):

    urls = []
    for tr in trs:
        td = tr.find_elements(By.TAG_NAME, "td")
        a = td[1].find_element(By.TAG_NAME, "a")
        url = a.get_attribute("href")
        urls.append(url)
    return urls


def download_files(driver, urls):
    for url in urls:
        driver.get(url)

        result_dropdown_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='analysis-select' or @id='analysis select-lable']")
            )
        )
        time.sleep(3)
        result_dropdown_box.click()
        dropdown_options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//li[@data-value]"))
        )

        total_options = len(dropdown_options)
        for i in range(0, total_options - 1):
            print(i)
            dropdown_options[i].click()
            if dropdown_options[i].text == "Bacteria":
                process_bacteria_data(driver)

            try:
                export_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(text(), 'Export current results')]",
                        )
                    )
                )
                export_button.click()
            except Exception as e:
                print("No export button")  # empty table
                pass

            time.sleep(1)

            result_dropdown_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@id='analysis-select' or @id='analysis select-lable']",
                    )
                )
            )
            time.sleep(1)
            result_dropdown_box.click()

            dropdown_options = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[@data-value]"))
            )
            time.sleep(1)


def process_bacteria_data(driver):
    taxonomy_switcher = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Taxonomy switcher')]")
        )
    )
    taxonomy_switcher.click()

    dropdown_boxs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "artifact-options-select"))
    )
    dropdown_box = dropdown_boxs[-1]
    time.sleep(2)
    dropdown_box.click()
    bacteria_dropdown_options = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[@data-value]"))
    )
    bacteria_total_options = len(bacteria_dropdown_options)
    for j in range(0, bacteria_total_options):
        bacteria_dropdown_options[j].click()
        time.sleep(1)
        try:
            export_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(text(), 'Export current results')]",
                    )
                )
            )
            export_button.click()
            if j < bacteria_total_options - 1:
                dropdown_box.click()
                time.sleep(1)
                bacteria_dropdown_options = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//li[@data-value]"))
                )
        except Exception as e:
            print("No export button")  # empty table
            pass


if __name__ == "__main__":

    download_dir = os.path.abspath("./files")

    chrome_options = Options()
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://app.cosmosid.com/search")
    close_button = driver.find_element(By.XPATH, "//button[@aria-label='close']")
    close_button.click()

    login()

    for _ in range(4):
        driver.execute_script("window.open('https://app.cosmosid.com/search')")

    # Get all window handles
    window_handles = driver.window_handles
    for i in range(0, len(window_handles)):
        driver.switch_to.window(window_handles[i])
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.ID, "intro-tour--functional-2-tour--close-button")
                )
            )
            close_button.click()
        except Exception as e:
            print(f"Could not close button on tab {i}: {e}")
            pass

        tbody = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )
        trs = tbody.find_elements(By.TAG_NAME, "tr")
        no_of_rows = len(trs)
        tds = trs[no_of_rows - (i + 1)].find_elements(By.TAG_NAME, "td")
        a = tds[1].find_element(By.TAG_NAME, "a")
        name = tds[1].text
        a.click()
        tbody = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )
        time.sleep(2)
        trs = tbody.find_elements(By.TAG_NAME, "tr")
        urls = extract_urls(trs)
        download_files(driver, urls)
