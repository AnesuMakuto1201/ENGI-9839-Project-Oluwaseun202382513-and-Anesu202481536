import pyautogui
import time

print("You have 5 seconds to click the Library Management System window...")
time.sleep(5)

# Locating and clicking the Logout button
print("Looking for 'Logout' button...")
logout_button = pyautogui.locateCenterOnScreen('lms_logout_button.png', confidence=0.8)
if logout_button:
    pyautogui.click(logout_button)
    print("Logout button clicked.")
else:
    print("Could not find Logout button.")
