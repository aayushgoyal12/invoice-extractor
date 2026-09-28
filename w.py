import time
import urllib.parse
import webbrowser
import pyautogui

# Saare numbers ki list (already with 91)
numbers = [
    "918860632015",
    "919810012029",
    "918860736513",
    "919810510280",
    "917303755564",
    "917701879108",
    "911244058233",  # Gurgaon Landline
    "918708901473",
    "918448337764",
    "918510091748",
    "919899095574",
]

message = (
    "Hi sir, main DU se graduate hoon aur abhi CA Inter ki prep kar raha hoon. "
    "Saath hi, tax data processing ke liye ek Python automation tool par kaam kar raha hoon.\n\n"
    "Yeh tool text-based GST PDFs ko direct clean Excel register mein convert karta hai aur missing fields flag kar deta hai.\n\n"
    "Main abhi iska ek small pilot run kar raha hoon. Agar aapke yahan invoicing ya data entry mein manual effort lagta hai, toh kya main 10 invoices ka ek free sample Excel output bhej sakta hoon review ke liye?"
)

encoded_message = urllib.parse.quote(message)

print("=== FULLY AUTOMATED WHATSAPP OUTREACH STARTED ===")
print("Script apne aap chat kholegi, load hone ka wait karegi, aur Enter press karegi!")
print("⚠️ Dhyan rakhna: Jab tak script chale, mouse ya keyboard ko touch mat karna.\n")

# Initial safety pause
time.sleep(3)

for index, phone_number in enumerate(numbers):
    whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"

    print(f"[{index+1}/{len(numbers)}] Opening chat for +{phone_number}...")
    webbrowser.open(whatsapp_url)
    
    # WhatsApp Web load hone ke liye ample time (18 seconds)
    print("WhatsApp load hone ka wait ho raha hai...")
    time.sleep(18)

    # Automatically press Enter to send the message
    print("Sending message...")
    pyautogui.press('enter')
    
    # Message send hone ke liye chhota wait
    time.sleep(3)
    
    # Tab close karne ke liye shortcut 
    # (Note: Agar Windows use kar raha hai toh 'command' ki jagah 'ctrl' kar dena -> pyautogui.hotkey('ctrl', 'w'))
    pyautogui.hotkey('command', 'w')
    
    print(f"Message sent & tab closed for +{phone_number}!\n")
    
    # Agla number khulne se pehle gap taaki browser crash na ho
    time.sleep(4)

print("🎉 Saare messages successfully automated tareeqe se send ho gaye hain!")