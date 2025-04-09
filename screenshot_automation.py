import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # **Restore Google login session**
    context = browser.new_context(
        storage_state=SESSION_FILE,
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=2
    )
    
    page = context.new_page()

    # **🚀 Step 1: Capture Graphs from First Looker Studio URL**
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

    # **🚀 Step 2: Capture Graphs from Second Looker Studio URL**
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

    # **🚀 Step 3: Capture "Forecasting Graph" from Third Looker Studio URL**
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

    # **🚀 Step 4: Capture "Margin Forecast" (Both nth(5) and nth(6))**
    looker_url_4 = "https://lookerstudio.google.com/u/0/reporting/e4a1b657-4b12-4006-bc7d-548acc494fb0/page/p_l7wemkecod"
    print(f"🌍 Navigating to: {looker_url_4}")
    page.goto(looker_url_4)
    time.sleep(30)

    print(f"📊 Processing: Combined Margin Forecast Graphs")
    graph_1 = page.locator("div.cdk-drag.lego-component-repeat").nth(6)
    graph_2 = page.locator("div.cdk-drag.lego-component-repeat").nth(7)
    graph_1.scroll_into_view_if_needed()
    graph_2.scroll_into_view_if_needed()
    graph_1.wait_for(state="visible", timeout=10000)
    graph_2.wait_for(state="visible", timeout=10000)

    box_1 = graph_1.bounding_box()
    box_2 = graph_2.bounding_box()

    if box_1 and box_2:
        combined_x = min(box_1["x"], box_2["x"])
        combined_y = min(box_1["y"], box_2["y"])
        combined_width = max(box_1["x"] + box_1["width"], box_2["x"] + box_2["width"]) - combined_x
        combined_height = (box_2["y"] + box_2["height"]) - combined_y

        extra_height = extra_heights.get("Margin_Forecast", 100)
        new_y = max(combined_y - extra_height, 0)
        new_height = combined_height + extra_height
        screenshot_path = os.path.join(output_folder_forecasting, "looker_studio_Margin_Forecast.png")
        page.screenshot(path=screenshot_path, clip={"x": combined_x, "y": new_y, "width": combined_width, "height": new_height})
        print(f"📸 Screenshot saved: {screenshot_path}")

    # **🚀 Step 5: Capture "Booking Made Today Going to February and March"**
    looker_url_5 = "https://lookerstudio.google.com/s/g5FlpFaFEao"
    print(f"🌍 Navigating to: {looker_url_5}")
    page.goto(looker_url_5)
    time.sleep(30)  # Ensures full page load

    print(f"📊 Processing: Booking Made Today (nth 18)")
    
    # **Target the graph using nth(18)**
    graph_element = page.locator("div.cdk-drag.lego-component-repeat").nth(14)

    # **Ensure the graph is visible**
    graph_element.scroll_into_view_if_needed()
    graph_element.wait_for(state="visible", timeout=15000)

    # **Extract graph position & dimensions**
    bounding_box = graph_element.bounding_box()
    if bounding_box:
        print(f"📏 Detected Graph Position (Booking Made Today): {bounding_box}")

        # **Adjust y and height to include the title**
        extra_height = extra_heights.get("Booking_Made_Today", 100)
        new_y = max(bounding_box["y"] - extra_height, 0)
        new_height = min(bounding_box["height"], 740)

        # **Save Screenshot in Forecasting Folder**
        screenshot_path = os.path.join(output_folder_forecasting, "looker_studio_Booking_Made_Today.png")
        page.screenshot(
            path=screenshot_path,
            clip={
                "x": bounding_box["x"],
                "y": new_y,
                "width": bounding_box["width"],
                "height": new_height
            }
        )
        print(f"📸 Screenshot saved: {screenshot_path}")

    # **🚀 Step 6: Capture "Daily_2%_growth"**
    looker_url_5 = "https://lookerstudio.google.com/reporting/79392fcb-9070-4c36-aeea-30e4cd7002a6/page/p_0dkh0kecod"
    print(f"🌍 Navigating to: {looker_url_5}")
    page.goto(looker_url_5)
    time.sleep(30)  # Ensures full page load

    print(f"📊 Processing: Booking Made Today (nth 2)")

    # **Target the graph using nth(2)**
    graph_element = page.locator("div.cdk-drag.lego-component-repeat").nth(2)

    # **Ensure the graph is visible**
    graph_element.scroll_into_view_if_needed()
    graph_element.wait_for(state="visible", timeout=10000)

    # **Extract graph position & dimensions**
    bounding_box = graph_element.bounding_box()
    if bounding_box:
        print(f"📏 Detected Graph Position (Daily_2%_growth): {bounding_box}")

        # **Adjust y and height to include only the table**
        extra_height = extra_heights.get("Daily_2%_growth", 386)  # Adjust this if needed
        new_y = max(bounding_box["y"] - extra_height, 0)  # Move upwards slightly to include the title
        new_height = max(bounding_box["height"] - extra_height, 550)  # Reduce downward height

        # **Save Screenshot in Forecasting Folder**
        screenshot_path = os.path.join(output_folder_forecasting, "Daily_2%_growth.png")
        page.screenshot(
            path=screenshot_path,
            clip={
                "x": bounding_box["x"],
                "y": new_y,
                "width": bounding_box["width"],
                "height": new_height
            }
        )
        print(f"📸 Screenshot saved: {screenshot_path}")



    # **🚀 Step 7: Capture "Daily_2%_growth"**
    # **Extra height adjustments for better visibility**
    extra_heights = {
    "Weekly_2%_Growth": 390,  
    "Monthly_2%_Growth": 150  
}


    # **🚀 Step 1: Capture "Weekly 2% Growth" Graphs Combined**
    looker_url_weekly = "https://lookerstudio.google.com/reporting/79392fcb-9070-4c36-aeea-30e4cd7002a6/page/p_0vnu3jgbad"
    print(f"🌍 Navigating to: {looker_url_weekly}")
    page.goto(looker_url_weekly)
    time.sleep(30)

    print(f"📊 Processing: Weekly 2% Growth (Combining nth 23 & nth 26)")
    graph_1 = page.locator("div.cdk-drag.lego-component-repeat").nth(23)
    graph_2 = page.locator("div.cdk-drag.lego-component-repeat").nth(26)

    graph_1.scroll_into_view_if_needed()
    graph_2.scroll_into_view_if_needed()
    graph_1.wait_for(state="visible", timeout=10000)
    graph_2.wait_for(state="visible", timeout=10000)

    box_1 = graph_1.bounding_box()
    box_2 = graph_2.bounding_box()

    if box_1 and box_2:
        combined_x = min(box_1["x"], box_2["x"])
        combined_y = min(box_1["y"], box_2["y"])
        combined_width = max(box_1["x"] + box_1["width"], box_2["x"] + box_2["width"]) - combined_x
        combined_height = (box_2["y"] + box_2["height"]) - combined_y

        # **Adjust for better visibility**
        extra_height = extra_heights.get("Weekly_2%_Growth", 300)
        new_y = max(combined_y - extra_height, 0)
        new_height = combined_height + extra_height

        # **Save Combined Screenshot**
        screenshot_path = os.path.join(output_folder_forecasting, "Weekly_2%_Growth_Combined.png")
        page.screenshot(
            path=screenshot_path,
            clip={"x": combined_x, "y": new_y, "width": combined_width, "height": new_height}
        )
        print(f"📸 Screenshot saved: {screenshot_path}")

    # **🚀 Step 2: Capture "Monthly 2% Growth" Graph**
    looker_url_monthly = "https://lookerstudio.google.com/reporting/79392fcb-9070-4c36-aeea-30e4cd7002a6/page/p_71t2ke6tod"
    print(f"🌍 Navigating to: {looker_url_monthly}")
    page.goto(looker_url_monthly)
    time.sleep(30)

    print(f"📊 Processing: Monthly 2% Growth (nth 5)")
    graph_element = page.locator("div.cdk-drag.lego-component-repeat").nth(4)
    graph_element.scroll_into_view_if_needed()
    graph_element.wait_for(state="visible", timeout=10000)

    bounding_box = graph_element.bounding_box()
    if bounding_box:
        extra_height = extra_heights.get("Monthly_2%_Growth", 150)
        new_y = max(bounding_box["y"] - extra_height, 0)
        new_height = bounding_box["height"] + extra_height

        screenshot_path = os.path.join(output_folder_forecasting, "Monthly_2%_Growth.png")
        page.screenshot(
            path=screenshot_path,
            clip={"x": bounding_box["x"], "y": new_y, "width": bounding_box["width"], "height": new_height}
        )
        print(f"📸 Screenshot saved: {screenshot_path}")

    browser.close()
    
    