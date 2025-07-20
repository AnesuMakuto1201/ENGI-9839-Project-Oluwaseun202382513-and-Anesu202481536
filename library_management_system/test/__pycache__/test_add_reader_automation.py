import pyautogui
import time

# Step 1: Give yourself time to focus the GUI window
print("You have 5 seconds to click on the app...")
time.sleep(5)

# Step 2: Login
pyautogui.write('admin')
time.sleep(0.5)
pyautogui.press('tab')
time.sleep(0.5)
pyautogui.write('password123')
time.sleep(0.5)
pyautogui.press('enter')
time.sleep(2)

# Step 3: Click "Add Reader" button
print("Looking for Add Reader button...")
add_button = pyautogui.locateCenterOnScreen('add_reader_button.png', confidence=0.8)
if add_button:
    pyautogui.click(add_button)
    time.sleep(2)
else:
    print("❌ Add Reader button not found!")
    exit()

# Step 4: Fill the form
pyautogui.write('R100')
pyautogui.press('tab')
pyautogui.write('John Doe')
pyautogui.press('tab')
pyautogui.write('john@example.com')
pyautogui.press('tab')
pyautogui.write('1234567890')

# Step 5: Click "Save" button
print("Looking for Save button...")
save_button = pyautogui.locateCenterOnScreen('save_reader_button.png', confidence=0.8)
if save_button:
    pyautogui.click(save_button)
    print("✅ Reader added successfully.")
else:
    print("❌ Save button not found.")
