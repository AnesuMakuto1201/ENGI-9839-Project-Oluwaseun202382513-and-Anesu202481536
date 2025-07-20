import pyautogui
import time

# Open and focus the library management system interface
print("You have 5 seconds to click on the login window...")
time.sleep(5)

# Enter login username and moving to password field
pyautogui.write('admin')
pyautogui.press('tab')  

# Input  password and press Enter to login
pyautogui.write('password123')


pyautogui.press('enter')

print("Login automation test completed.")
