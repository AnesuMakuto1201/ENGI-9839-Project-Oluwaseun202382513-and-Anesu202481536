import pyautogui
import time

print("You have 5 seconds to click on the Library Management System window...")
time.sleep(5)

# Click the Rental Management tab
print("Looking for 'Rental Management' tab...")
rental_tab = pyautogui.locateCenterOnScreen('rental_management_tab.png', confidence=0.8)
if rental_tab:
    pyautogui.click(rental_tab)
    print("Clicked 'Rental Management' tab.")
    time.sleep(1)
else:
    print("Could not find 'Rental Management' tab.")
    exit()

# Click 'View Reader Rentals' button
print("Looking for 'View Reader Rentals' button...")
view_btn = pyautogui.locateCenterOnScreen('view_reader_rentals_button.png', confidence=0.8)
if view_btn:
    pyautogui.click(view_btn)
    print("Clicked 'View Reader Rentals' button.")
    time.sleep(1)
else:
    print("Could not find 'View Reader Rentals' button.")
    exit()

# Enter Reader ID
print("Looking for Reader ID input box...")
reader_input = pyautogui.locateCenterOnScreen('rental_reader_id_inputbox.png', confidence=0.8)
if reader_input:
    pyautogui.click(reader_input)
    pyautogui.write('202382513', interval=0.05)
    print("Reader ID entered.")
    time.sleep(0.5)
else:
    print("Could not find Reader ID input box.")
    exit()

# Click "OK" button
print("Looking for OK button...")
ok_button = pyautogui.locateCenterOnScreen('view_reader_rental_ok_button.png', confidence=0.8)
if ok_button:
    pyautogui.click(ok_button)
    print("Clicked OK button.")
else:
    print("Could not find OK button.")
