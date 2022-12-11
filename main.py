#libraries
import os
from gui import *
from talk import *
from art import *

print("\n")
tprint("FRIDAY AI")
print(f"{bcolors.OKCYAN}Welcome, firing GUI. Should be ready in a moment.\n{bcolors.ENDC}")

#Auth
def auth_change(pin):
    result = hashlib.md5(pin.encode())
    auth_file = open("Authfile", "w+")
    auth_file.write(result.hexdigest())
    auth_file.close()
    return result.hexdigest()

#Get auth pin
if(os.path.exists("Authfile")):
    auth_file = open("Authfile", "r")
    gui_pincode = auth_file.read()
else:
    print("AUTH: "+bcolors.WARNING+"No authorization record found"+bcolors.ENDC)
    r = auth_change('1234')
    gui_pincode = r
    if(r):
        print("AUTH: "+bcolors.HEADER+"Auth reset(New pin: 1234). Ask Friday 'Change engine PIN'"+bcolors.ENDC)
    else:
        print("AUTH: "+bcolors.WARNING+"Failed to create a auth record"+bcolors.ENDC)
        talk("I am unable to fire GUI. Abroting...")
        quit()

talk("Hi, I am Friday. Enter your PIN code to verify and begin engine.")
gui = auth(gui_pincode)
gui.mainloop()