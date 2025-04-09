from playwright.sync_api import sync_playwright
import time

# Path to save login session
session_file = "google_login.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Open Chrome with UI
    context = browser.new_context()

    # Open a new page
    page = context.new_page()
    
    # Go to Google login page
    page.goto("https://accounts.google.com/")

    # Wait for manual login
    input("Log in manually and press Enter here...")

    # Save session (cookies & storage)
    context.storage_state(path=session_file)

    print("Login session saved successfully!")

    # Close browser
    browser.close()
