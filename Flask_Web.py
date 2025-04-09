from flask import Flask, render_template, jsonify
import threading
import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# **Path to saved Google login session**
SESSION_FILE = "google_login.json"

# **Get Current Hour to Create a Folder**
current_hour = datetime.now().strftime("%Y-%m-%d_%H")  # Format: YYYY-MM-DD_HH

# **Define output folders**
output_folder_300M = f"screens_automate/screenshots/300M/{current_hour}"  # 300M Folder
output_folder_forecasting = f"screens_automate/screenshots/Forecasting/{current_hour}"  # Forecasting Folder
os.makedirs(output_folder_300M, exist_ok=True)  # Ensure 300M folder exists
os.makedirs(output_folder_forecasting, exist_ok=True)  # Ensure Forecasting folder exists

# **Define custom extra heights for each graph**
extra_heights = {
    "North_America_Without_Vegas": 0,
    "LATAM": 0,
    "EMEA": 0,
    "APAC": 0,
    "Farming": 120,
    "Potential_TTV_Share": 120,
    "Mark_Up_and_Revenue": 75,
    "Forecasted Vs Target": 0,  # Adjusted extra height for nth(29)
    "Margin_Forecast": 150  # Extra height for combined graphs
}

def run_screenshot_script():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # **Restore Google login session**
            context = browser.new_context(
                storage_state=SESSION_FILE,
                viewport={"width": 1920, "height": 1080},
                device_scale_factor=2
            )
            
            page = context.new_page()

            # **Step 1: Capture Graphs from First Looker Studio URL**
            looker_url_1 = "https://lookerstudio.google.com/s/h5ygQdM1cz8"
            print(f"🌍 Navigating to: {looker_url_1}")
            page.goto(looker_url_1)
            time.sleep(40)  # Ensures full page load

            graphs_1 = {
                "North_America_Without_Vegas": 2,
                "LATAM": 3,
                "EMEA": 4,
                "APAC": 5
            }

            for region, index in graphs_1.items():
                print(f"📊 Processing: {region}")
                graph_element = page.locator("div.cdk-drag.lego-component-repeat").nth(index)
                graph_element.scroll_into_view_if_needed()
                graph_element.wait_for(state="visible", timeout=10000)
                bounding_box = graph_element.bounding_box()

                if bounding_box:
                    extra_height = extra_heights.get(region, 100)
                    new_y = max(bounding_box["y"] - extra_height, 0)
                    new_height = bounding_box["height"] + extra_height
                    screenshot_path = os.path.join(output_folder_300M, f"looker_studio_{region}.png")
                    page.screenshot(path=screenshot_path, clip={"x": bounding_box["x"], "y": new_y, "width": bounding_box["width"], "height": new_height})
                    print(f"📸 Screenshot saved: {screenshot_path}")

            # **Step 2: Capture Graphs from Second Looker Studio URL**
            looker_url_2 = "https://lookerstudio.google.com/s/pBxYu1fCH_s"
            print(f"🌍 Navigating to: {looker_url_2}")
            page.goto(looker_url_2)
            time.sleep(30)  # Ensures full page load

            graphs_2 = {
                "Farming": 0,
                "Potential_TTV_Share": 6,
                "Mark_Up_and_Revenue": 25
            }

            for name, index in graphs_2.items():
                print(f"📊 Processing: {name}")
                graph_element = page.locator("div.cdk-drag.lego-component-repeat").nth(index)
                graph_element.scroll_into_view_if_needed()
                graph_element.wait_for(state="visible", timeout=10000)
                bounding_box = graph_element.bounding_box()

                if bounding_box:
                    extra_height = extra_heights.get(name, 250)
                    new_y = max(bounding_box["y"] - extra_height, 0)
                    new_height = bounding_box["height"] + extra_height
                    screenshot_path = os.path.join(output_folder_300M, f"looker_studio_{name}.png")
                    page.screenshot(path=screenshot_path, clip={"x": bounding_box["x"], "y": new_y, "width": bounding_box["width"], "height": new_height})
                    print(f"📸 Screenshot saved: {screenshot_path}")

            # **Step 3: Capture "Forecasting Graph" from Third Looker Studio URL**
            looker_url_3 = "https://lookerstudio.google.com/s/un-Qn7koFhY"
            print(f"🌍 Navigating to: {looker_url_3}")
            page.goto(looker_url_3)
            time.sleep(30)

            print(f"📊 Processing: Forecasting Graph (nth 29)")
            graph_element = page.locator("div.cdk-drag.lego-component-repeat").nth(28)
            graph_element.scroll_into_view_if_needed()
            graph_element.wait_for(state="visible", timeout=10000)
            bounding_box = graph_element.bounding_box()

            if bounding_box:
                extra_height = extra_heights.get("Forecasted Vs Target", 100)
                new_y = max(bounding_box["y"] - extra_height, 0)
                new_height = bounding_box["height"] + extra_height
                screenshot_path = os.path.join(output_folder_forecasting, "Forecasted Vs Target.png")
                page.screenshot(path=screenshot_path, clip={"x": bounding_box["x"], "y": new_y, "width": bounding_box["width"], "height": new_height})
                print(f"📸 Screenshot saved: {screenshot_path}")

            browser.close()

    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    # Run the screenshot script in a separate thread
    thread = threading.Thread(target=run_screenshot_script)
    thread.start()
    return render_template('index.html', message="The script is running, please wait...")

if __name__ == '__main__':
    app.run(debug=True)
