import streamlit as st
import time
from playwright.sync_api import sync_playwright

st.title("📸 Webpage Screenshot Tool")

if st.button("Capture Screenshot"):
    with st.spinner("Taking screenshot..."):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    storage_state="google_login.json",
                    viewport={"width": 1920, "height": 1080},
                    device_scale_factor=2
                )
                page = context.new_page()
                page.goto("https://lookerstudio.google.com/s/h5ygQdM1cz8")
                time.sleep(5)
                screenshot_path = "screenshot.png"
                page.screenshot(path=screenshot_path)
                browser.close()

            st.success("Screenshot taken!")
            st.image(screenshot_path)
        except Exception as e:
            st.error(f"An error occurred: {e}")
