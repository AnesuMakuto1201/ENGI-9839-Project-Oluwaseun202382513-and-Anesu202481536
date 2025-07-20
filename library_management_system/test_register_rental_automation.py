import pyautogui
import time

print("You have 5 seconds to click on the Library Management System window...")
time.sleep(5)

# Click "Rental Management" tab
print("Looking for 'Rental Management' tab...")
rental_tab = pyautogui.locateCenterOnScreen('rental_management_tab.png', confidence=0.8)
if rental_tab:
    pyautogui.click(rental_tab)
    print("Clicked 'Rental Management' tab.")
    time.sleep(1)
else:
    print("Could not find 'Rental Management' tab.")
    exit()

# Click "Register Rental" button
print("Looking for 'Register Rental' button...")
register_rental_btn = pyautogui.locateCenterOnScreen('regrental_register_button.png', confidence=0.8)
if register_rental_btn:
    pyautogui.click(register_rental_btn)
    print("Clicked 'Register Rental' button.")
    time.sleep(1)
else:
    print("Could not find 'Register Rental' button.")
    exit()

# Enter Reader ID and move to Book ISBN field
print("Looking for Reader ID input box...")
reader_id_box = pyautogui.locateCenterOnScreen('regrental_reader_id_box.png', confidence=0.8)
if reader_id_box:
    pyautogui.click(reader_id_box)
    time.sleep(0.3)
    pyautogui.write('202481536', interval=0.05)
    print("Entered Reader ID.")
    time.sleep(0.3)
    pyautogui.press('tab')  
    time.sleep(0.3)
    pyautogui.write('9 781550 819731', interval=0.05)
    print("Entered Book ISBN.")
else:
    print("Could not find Reader ID input box.")
    exit()

# Click Register button
print("Looking for 'Register' button...")
register_btn = pyautogui.locateCenterOnScreen('regrental_confirm_register_button.png', confidence=0.8)
if register_btn:
    pyautogui.click(register_btn)
    print("Clicked 'Register' to complete rental.")
else:
    print("Could not find 'Register' button.")
