import pyautogui
import time

print("You have 5 seconds to click on the app window...")
time.sleep(5)

# Select the reader row 
print("Looking for John Doe row...")
row = pyautogui.locateCenterOnScreen('john_doe_row.png', confidence=0.8)
if row:
    pyautogui.click(row)
    print("Selected John Doe row.")
    time.sleep(1)
else:
    print("John Doe row not found!")
    exit()

# Click the 'Delete Reader' button
print("Looking for Delete Reader button...")
delete_btn = pyautogui.locateCenterOnScreen('delete_reader_button.png', confidence=0.8)
if delete_btn:
    pyautogui.click(delete_btn)
    print("Clicked Delete Reader button.")
    time.sleep(2)
else:
    print("Delete Reader button not found!")
    exit()

# Click the 'Yes' button in the confirmation dialog
print("Looking for Yes button...")
yes_btn = pyautogui.locateCenterOnScreen('yes_delete_reader_button.png', confidence=0.8)
if yes_btn:
    pyautogui.click(yes_btn)
    print("Clicked Yes to confirm deletion.")
    time.sleep(2)
else:
    print(" Yes button not found!")
    exit()

# Click the 'OK' button in the success dialog
print("Looking for OK button...")
ok_btn = pyautogui.locateCenterOnScreen('ok_delete_reader_button.png', confidence=0.8)
if ok_btn:
    pyautogui.click(ok_btn)
    print("Reader deletion confirmed.")
else:
    print("OK button not found!")

print("Delete Reader automation test completed.")
