import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Load sensitive data from environment variables
config = {
    "first_name": os.getenv("FIRST_NAME"),
    "last_name": os.getenv("LAST_NAME"),
    "address": os.getenv("ADDRESS"),
    "city": os.getenv("CITY"),
    "zip_code": os.getenv("ZIP_CODE"),
    "phone": os.getenv("PHONE"),
    "state": os.getenv("STATE"),
    "state_index": os.getenv("STATE_INDEX", "16"),  # Default to index 16 if not provided
}

# Set up Chrome options
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')  # Disable GPU acceleration
options.add_argument('--headless')  # Run headless (no GUI)

# Initialize the WebDriver without specifying the driver path (GitHub Actions handles it)
driver = webdriver.Chrome(options=options)

try:
    # Open the Signup Genius URL
    url = "https://www.signupgenius.com/go/10C0949ABA623A0F9C52-54171446-automationtest#/"
    driver.get(url)
    print("Navigated to:", driver.current_url)

    # Locate and click the "Sign Up" button
    try:
        sign_up_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-signup')]"))
        )
        sign_up_button.click()
        print("Sign Up button clicked.")
    except:
        print("Sign Up button not found or not clickable. Exiting the program.")
        driver.quit()
        exit()

    # Locate and click the "Save & Continue" button if present
    try:
        save_continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save & Continue')]"))
        )
        save_continue_button.click()
        print("'Save & Continue' button clicked. Proceeding to form.")
    except:
        print("'Save & Continue' button not found. Proceeding to form.")

    # Wait for the form to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//form"))
    )
    print("Form loaded. Filling out available fields...")

    # Dynamically check and fill fields
    name_filled = False

    # Check for 'name' field first
    try:
        name_field = driver.find_element(By.XPATH, "//input[@id='name']")
        name_field.send_keys(f"{config['first_name']} {config['last_name']}")
        print(f"Name entered: {config['first_name']} {config['last_name']}")
        name_filled = True
        time.sleep(1)
    except:
        print("Combined Name field not found. Checking for separate fields.")

    # If 'name' field is not found, try separate first and last name fields
    if not name_filled:
        try:
            first_name_field = driver.find_element(By.XPATH, "//input[@id='firstname']")
            first_name_field.send_keys(config['first_name'])
            print(f"First Name entered: {config['first_name']}")
            time.sleep(1)
        except:
            print("First Name field not found.")

        try:
            last_name_field = driver.find_element(By.XPATH, "//input[@id='lastname']")
            last_name_field.send_keys(config['last_name'])
            print(f"Last Name entered: {config['last_name']}")
            time.sleep(1)
        except:
            print("Last Name field not found.")

    # Other fields
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

    # Select State/Province Dropdown
    try:
        state_dropdown = driver.find_element(By.XPATH, "//span[contains(@class, 'filter-option pull-left') and text()='Select State/Province']")
        state_dropdown.click()  # Open the dropdown
        time.sleep(1)

        # Select the configured state from the dropdown
        state_option = driver.find_element(By.XPATH, f"//li[@data-original-index='{config['state_index']}']")
        state_option.click()
        print(f"State selected: {config['state']}")
        time.sleep(1)
    except:
        print("State/Province dropdown not found.")

    # Locate and click the "Sign Up Now" button
    try:
        sign_up_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "btnSignUp"))
        )
        sign_up_now_button.click()
        print("'Sign Up Now' button clicked successfully.")
    except:
        print("'Sign Up Now' button not found.")

except Exception as e:
    print("Unexpected error occurred:", e)

finally:
    driver.quit()