import pyautogui
import time
import sys

# Helper function to locate image and print status
def locate_image(image_name, label):
    print(f"🔍 Looking for {label}...")
    location = pyautogui.locateCenterOnScreen(image_name, confidence=0.8)
    if location:
        print(f"Found {label}.")
    else:
        print(f"Could not find {label}.")
    return location


print("You have 5 seconds to click on the Library Management System window...")
time.sleep(5)

# Click "Rental Management" tab
rental_tab = locate_image('rental_management_tab.png', "'Rental Management' tab")
if not rental_tab:
    sys.exit()
pyautogui.click(rental_tab)
time.sleep(1)

# Click "Register Return" button
return_btn = locate_image('regrental_register_return_button.png', "'Register Return' button")
if not return_btn:
    sys.exit()
pyautogui.click(return_btn)
time.sleep(1)

# Enter Rental ID
reader_box = locate_image('regrental_reader_id_box.png', "Rental ID input box")
if not reader_box:
    sys.exit()
pyautogui.click(reader_box)
time.sleep(0.3)
pyautogui.write('R0004', interval=0.05)
print("Entered Reader ID.")
time.sleep(0.3)


# Click OK button to confirm
ok_btn = locate_image('ok_registerreturn_button.png', "'OK' button (Register Return)")
if not ok_btn:
    sys.exit()
pyautogui.click(ok_btn)
print("Clicked OK to complete return process.")
