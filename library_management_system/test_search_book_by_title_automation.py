import pyautogui
import time
import sys

def locate_and_click(image_file, description, confidence=0.8, retries=5, delay=1):
    print(f"Looking for '{description}'...")
    for attempt in range(retries):
        try:
            location = pyautogui.locateCenterOnScreen(image_file, confidence=confidence)
            if location:
                pyautogui.moveTo(location)
                pyautogui.click()
                print(f"Clicked '{description}'.")
                time.sleep(delay)
                return location
            else:
                print(f"  Attempt {attempt + 1} failed... retrying.")
                time.sleep(delay)
        except pyautogui.ImageNotFoundException:
            print(f"Image not found: {image_file}")
            time.sleep(delay)
    print(f"Failed to locate '{description}' after {retries} attempts.")
    return None

print("You have 5 seconds to click on the Library Management System window...")
time.sleep(5)

# Click "Search Books" tab
if not locate_and_click('search_books_tab.png', "Search Books tab"):
    sys.exit()

# Click "Title" radio button
if not locate_and_click('search_by_title_radio.png', "Title radio button"):
    sys.exit()

# Click search input box
search_box = locate_and_click('search_input_box.png', "Search input box")
if not search_box:
    sys.exit()

# Type book title
pyautogui.write("The Gull workshop and other stories", interval=0.05)
print("Entered book title.")
time.sleep(0.5)

# Click Search button
if not locate_and_click('search_book_button.png', "Search button"):
    sys.exit()

print("Search Book by Title test completed successfully.")
