import time
import os
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Automatically download and install the correct version of ChromeDriver
chromedriver_autoinstaller.install()

# Load sensitive data from environment variables
config = {
    "first_name": os.getenv("FIRST_NAME"),
    "last_name": os.getenv("LAST_NAME"),
    "address": os.getenv("ADDRESS"),
    "city": os.getenv("CITY"),
    "zip_code": os.getenv("ZIP_CODE"),
    "phone": os.getenv("PHONE"),
    "state": os.getenv("STATE"),
    "state_index": os.getenv("STATE_INDEX", "16"),
}

# Set up Chrome options
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # Overcome resource limitations
options.add_argument('--disable-gpu')  # Disable GPU for stability
options.add_argument('--window-size=1920,1080')  # Set consistent viewport size
options.add_argument('--disable-blink-features=AutomationControlled')  # Avoid detection

# Initialize WebDriver
try:
    driver = webdriver.Chrome(options=options)
    print(f"Chrome version: {driver.capabilities['browserVersion']}")

    # Open the target URL
    url = "https://www.signupgenius.com/go/10C0949ABA623A0F9C52-54171446-automationtest#/"
    print(f"Navigating to: {url}")
    driver.get(url)

    # Locate and click the "Sign Up" button
    try:
        print("Looking for the 'Sign Up' button...")
        sign_up_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-signup')]"))
        )
        sign_up_button.click()
        print("Sign Up button clicked.")
    except Exception as e:
        print(f"Error locating 'Sign Up' button: {e}")
        driver.quit()
        exit()

    # Locate and click the "Save & Continue" button if present
    try:
        print("Looking for the 'Save & Continue' button...")
        save_continue_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save & Continue')]"))
        )
        save_continue_button.click()
        print("'Save & Continue' button clicked.")
    except:
        print("'Save & Continue' button not found. Proceeding without it.")

    # Wait for the form to load
    try:
        print("Waiting for the form to load...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//form"))
        )
        print("Form loaded successfully.")
    except Exception as e:
        print(f"Error loading form: {e}")
        driver.quit()
        exit()

    # Dynamically fill fields
    name_filled = False
    try:
        name_field = driver.find_element(By.XPATH, "//input[@id='name']")
        name_field.send_keys(f"{config['first_name']} {config['last_name']}")
        print(f"Name entered: {config['first_name']} {config['last_name']}")
        name_filled = True
        time.sleep(1)
    except:
        print("Combined Name field not found. Trying separate fields.")
        try:
            driver.find_element(By.XPATH, "//input[@id='firstname']").send_keys(config['first_name'])
            driver.find_element(By.XPATH, "//input[@id='lastname']").send_keys(config['last_name'])
            print(f"Separate Name fields entered: {config['first_name']} {config['last_name']}")
        except:
            print("Separate Name fields not found.")

    # Fill other fields dynamically
    fields = [
        {"xpath": "//input[@id='5560032_id']", "value": config["address"], "name": "Address"},
        {"xpath": "//input[@id='5560034_id']", "value": config["city"], "name": "City"},
        {"xpath": "//input[@id='5560036_id']", "value": config["zip_code"], "name": "Zip Code"},
        {"xpath": "//input[@id='phone_id']", "value": config["phone"], "name": "Phone"},
    ]

    for field in fields:
        try:
            element = driver.find_element(By.XPATH, field["xpath"])
            element.send_keys(field["value"])
            print(f"{field['name']} entered: {field['value']}")
            time.sleep(1)
        except:
            print(f"{field['name']} field not found.")

    # Handle State dropdown
    try:
        state_dropdown = driver.find_element(By.XPATH, "//span[contains(@class, 'filter-option pull-left') and text()='Select State/Province']")
        state_dropdown.click()
        time.sleep(1)
        driver.find_element(By.XPATH, f"//li[@data-original-index='{config['state_index']}']").click()
        print(f"State selected: {config['state']}")
        time.sleep(1)
    except:
        print("State dropdown not found.")

    # Submit the form
    try:
        sign_up_now_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.NAME, "btnSignUp"))
        )
        sign_up_now_button.click()
        print("'Sign Up Now' button clicked successfully.")
    except Exception as e:
        print(f"Error clicking 'Sign Up Now' button: {e}")

except Exception as e:
    print(f"Unexpected error occurred: {e}")

finally:
    driver.quit()