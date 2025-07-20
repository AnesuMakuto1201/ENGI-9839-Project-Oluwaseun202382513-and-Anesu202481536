import pyautogui
import time

# Time to select the library management system application window
print("You have 5 seconds to click on the app...")
time.sleep(5)

#Login
pyautogui.write('admin')
pyautogui.press('tab')
pyautogui.write('password123')
pyautogui.press('enter')
time.sleep(3)

# Click Book Management tab
print("Looking for Book Management tab...")
tab = pyautogui.locateCenterOnScreen('book_management_tab.png', confidence=0.8)
if tab:
    pyautogui.click(tab)
    print("Book Management tab clicked.")
else:
    print("Book Management tab not found.")
    exit()

time.sleep(2)

# Click Add Book button
print("Looking for Add Book button...")
add_btn = pyautogui.locateCenterOnScreen('add_book_button.png', confidence=0.8)
if add_btn:
    pyautogui.click(add_btn)
    print("Add Book button clicked.")
else:
    print("Add Book button not found.")
    exit()

time.sleep(2)

# Fill the book ISBN, Title,Author,Copies
print("Filling in book details...")
pyautogui.write('9789876553233')  
pyautogui.press('tab')
pyautogui.write('Automate everything ')  
pyautogui.press('tab')
pyautogui.write('Anesu Vickie')  
pyautogui.press('tab')
pyautogui.write('2')  

time.sleep(1)

# Click Save button
print("Looking for Save button...")
save_btn = pyautogui.locateCenterOnScreen('save_book_button.png', confidence=0.8)
if save_btn:
    pyautogui.click(save_btn)
    print("Save button clicked.")
else:
    print("Save button not found.")
    exit()

time.sleep(2)

# Confirm success
print("Looking for OK success message...")
ok_btn = pyautogui.locateCenterOnScreen('ok_add_book_button.png', confidence=0.8)
if ok_btn:
    pyautogui.click(ok_btn)
    print("Book added successfully confirmed.")
else:
    print("OK confirmation not found.")

print("Add Book automation test completed.")
