import pyautogui
import time

print("You have 5 seconds to click on the Library Management System window...")
time.sleep(5)

# Click "Search Books" tab
print("Looking for 'Search Books' tab...")
search_tab = pyautogui.locateCenterOnScreen('search_books_tab.png', confidence=0.8)
if search_tab:
    pyautogui.click(search_tab)
    print("Clicked 'Search Books' tab.")
    time.sleep(1)
else:
    print("Could not find 'Search Books' tab.")
    exit()

# Click ISBN radio button
print("Looking for 'ISBN' radio button...")
isbn_radio = pyautogui.locateCenterOnScreen('search_by_isbn_radio.png', confidence=0.8)
if isbn_radio:
    pyautogui.click(isbn_radio)
    print("Selected 'ISBN' radio button.")
    time.sleep(0.5)
else:
    print("Could not find 'ISBN' radio button.")
    exit()

# Locate and click the search input box
print("Looking for search input box...")
input_box = pyautogui.locateCenterOnScreen('search_input_box.png', confidence=0.7)
if input_box:
    pyautogui.moveTo(input_box.x, input_box.y, duration=0)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.write('9781550819731', interval=0.05)
    print("ISBN entered.")
    time.sleep(0.3)
else:
    print("Could not find search input box.")
    exit()


# Click Search button
print("Looking for Search button...")
search_button = pyautogui.locateCenterOnScreen('search_book_button.png', confidence=0.8)
if search_button:
    pyautogui.click(search_button)
    print("Search button clicked.")
else:
    print("Could not find Search button.")
