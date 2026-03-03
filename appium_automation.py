import time
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import shutil

PACKAGE = "nl.remeha.servicetoolapp_android_dedietrich"
LIST_ID = f"{PACKAGE}:id/listView1"

opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "Android"
opts.app_package = PACKAGE
opts.no_reset = True

def init_driver():
    driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
    driver.terminate_app(PACKAGE)
    driver.activate_app(PACKAGE)
    return driver

# ---------------- UTILS ----------------

def wait_device_data_ready(wait):
    btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, f"{PACKAGE}:id/dataButton")
        )
    )
    btn.click()
    time.sleep(2)

def click_tab(name, driver):
    driver.find_element(
        AppiumBy.XPATH,
        f"//android.widget.Button[@text='{name}']"
    ).click()
    time.sleep(1.5)

def scroll_to_top(driver):
    try:
        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().resourceId("{LIST_ID}")).scrollToBeginning(20)'
        )
        time.sleep(1.5)
    except Exception:
        pass

def scroll_down(driver):
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiScrollable(new UiSelector().resourceId("{LIST_ID}")).scrollForward()'
    )
    time.sleep(1.2)

def handle_deprecation_warning(driver):
    try:
        print("⏳ Sprawdzam deprecation warning...")
        continue_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//android.widget.Button[contains(@text,'CONTINUE')]")
            )
        )
        continue_btn.click()
        print("👉 Deprecation warning kliknięty")
    except TimeoutException:
        print("ℹ️ Brak deprecation warning – pomijam")


# ---------------- CORE PARSER ----------------

def collect_visible_rows(collected, driver):
    rows = driver.find_elements(
        AppiumBy.XPATH,
        f"//android.widget.ListView[@resource-id='{LIST_ID}']/android.widget.LinearLayout"
    )

    print(f"🔎 Widoczne wiersze: {len(rows)}")

    for row in rows:
        try:
            code = row.find_element(
                AppiumBy.ID, f"{PACKAGE}:id/configurationId"
            ).text.strip()

            name = row.find_element(
                AppiumBy.ID, f"{PACKAGE}:id/name"
            ).text.strip()

            value = row.find_element(
                AppiumBy.ID, f"{PACKAGE}:id/value"
            ).text.strip()

            key = f"{code} ({name})"
            if key not in collected:
                collected[key] = value

        except Exception:
            continue

def collect_tab(collected, driver):
    scroll_to_top(driver)
    last_count = -1

    for _ in range(30):
        collect_visible_rows(collected, driver)

        if len(collected) == last_count:
            break

        last_count = len(collected)
        scroll_down(driver)

# ---------------- MAIN ----------------
def main():
    data = {}
    driver = init_driver()
    wait = WebDriverWait(driver, 30)
    handle_deprecation_warning(driver)
    print("⏳ Czekam aż DEVICE DATA będzie klikalne...")
    wait_device_data_ready(wait)
    print("👉 DEVICE DATA otwarte")

    for tab in ["TEMP.", "OTHER", "0/1"]:
        print(f"👉 Zakładka {tab}")
        click_tab(tab, driver)
        collect_tab(data, driver)

    # ---------------- SAVE ----------------

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    filename = f"sample_data_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for k, v in sorted(data.items()):
            f.write(f"{k};{v}\n")

    print(f"✅ Zapisano {len(data)} rekordów do {filename}")
    shutil.copy(filename, "/data/heatpump_data_latest.txt")
    driver.terminate_app(PACKAGE)

if __name__ == "__main__":
    main()

