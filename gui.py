import os
from tkinter import *
from brain import *
from talk import talk
import speech_recognition as sr
import hashlib

window = 0
btn = 0
try_count = 0
lbl_input_stream = 0
window_listen_notavailable = 0
window_command = 0

def brain_actions(response):
    if(response == "ENGINE_CHANGE_PIN"):
        pin_changer()
        return
    elif(response == 0):
        return

def pre_process(input):
    print("Command: "+bcolors.OKBLUE+input+bcolors.ENDC)
    response = brain(input, window)
    brain_actions(response)
    launch_text_input_window()

def launch_text_input_window():
    global window_command
    global window
    main_window = window
    if(window_command > 0):
        return
    dialogue = "Command Window"
    window = Tk()
    window.title("Friday AI")
    window.geometry("185x120")
    window.resizable(height= "false", width= "false")
    window.eval('tk::PlaceWindow . center')
    lbl = Label(window, text= dialogue, font=("Arial bold", "15"), fg= "red")
    lbl.grid(column=0, row=0)
    lbl = Label(window, text= 'Command here', font=("Sans", "11"))
    lbl.grid(column=0, row=1)
    txt = Entry(window, width=15)
    txt.grid(column=0, row=2)
    txt.focus()
    def a():
        global window_command
        t = txt.get()
        if(window_command == 1):
            main_window.destroy()
        window_command+= 1
        pre_process(t.lower())
    btn = Button(window, text="Run", bg="white", fg="red", command= a)
    btn.grid(column=0, row=3)
    window_command+= 1
    window.mainloop()

def launch_action_center(differ_call = 0):
    global window_listen_notavailable
    global window
    global lbl_input_stream
    global btn
    if(differ_call == 0):
        #Action center
        window = dashboard()
        dialogue = "FRIDAY FEEDBACK CENTER"

        #Elements
        lbl = Label(window, text= dialogue, font=("Arial bold", "25"), fg= "red")
        lbl.grid(column=0, row=0)

        lbl_input_stream = Label(window, text = "Please proceed to start the engine.", font=("Arial bold", "12"), fg= "green")
        lbl_input_stream.grid(column=0, row=1)
    def process(input):
        print("Command: "+bcolors.OKBLUE+input+bcolors.ENDC)
        lbl_input_stream.configure(text=input)
        response = brain(input, window)
        brain_actions(response)
        lbl_input_stream.configure(text= response, fg= "blue")
        #Recall listen
        listen(1)
    
    def listen(flag = 0, flag_restart = 0):
        global btn
        global window
        global window_listen_notavailable
        if(flag_restart == 1):
            print("Engine: "+bcolors.HEADER+"Restarted"+bcolors.ENDC)
        lbl_input_stream.configure(text= "Trying to listen...")
        #This will try to listen if network available
        r = sr.Recognizer()	
        while(1):
            try:
                with sr.Microphone() as source2:
                    r.adjust_for_ambient_noise(source2, duration=0.2)
                    audio2 = r.listen(source2)
                    Text = r.recognize_google(audio2)
                    Text = Text.lower()
                    process(Text)
            except sr.RequestError as e:
                error = "Listener error. Could not request results; {0}".format(e)
                talk("Boss, "+error)
                print("Engine: "+bcolors.WARNING+"Aborted("+error+")"+bcolors.ENDC)
                talk("I can't listen to you without internet, please write your commands through the command window.")
                print("Engine: "+bcolors.WARNING+"Switched to type input mode"+bcolors.ENDC)
                window_listen_notavailable = 1
                launch_text_input_window()
                break
            except sr.UnknownValueError:
                listen(1)
            break

    if(differ_call == 1):
        listen(1, 1)
        return
        
    btn = Button(window, text="Start Engine", bg="white", fg="red", command= listen)
    btn.grid(column=0, row=2)

    window.mainloop()

def auth(gui_pincode, title = 'Friday AI - Authorization'):
    global try_count
    dialogue = "Welcome to Friday AI"
    window = Tk()
    window.title(title)
    window.geometry("206x120")
    window.resizable(height= "false", width= "false")
    window.eval('tk::PlaceWindow . center')
    lbl = Label(window, text= dialogue, font=("Arial bold", "15"), fg= "red")
    lbl.grid(column=0, row=0)
    lbl = Label(window, text= 'Enter your PIN', font=("Sans", "11"))
    lbl.grid(column=0, row=1)
    txt = Entry(window, width=10)
    txt.grid(column=0, row=2)
    txt.focus()
    def auth_test():
        global try_count
        t = txt.get()
        t = hashlib.md5(t.encode())
        t = t.hexdigest()
        if(t == gui_pincode):
            talk("Successfully verified. Welcome Boss!")
            window.destroy()
            launch_action_center()
        else:
            if(try_count < 3):
                try_count+=1
                talk("Try again")
            else:
                talk("I can see you are entering wrong PIN code. Make sure you have access permission.")
                try_count = 0
    btn = Button(window, text="Verify", bg="white", fg="red", command= auth_test)
    btn.grid(column=0, row=3)
    return window

def dashboard(title = 'Friday AI - Visual feedback'):
    window = Tk()
    window.title(title)
    window.geometry("464x150")
    window.resizable(height= "false", width= "false")
    return window

def pin_changer():
    dialogue = "Change Engine PIN"
    window = Tk()
    window.title("Friday")
    window.geometry("190x170")
    window.resizable(height= "false", width= "false")
    window.eval('tk::PlaceWindow . center')
    lbl = Label(window, text= dialogue, font=("Arial bold", "15"), fg= "red")
    lbl.grid(column=0, row=0)
    lbl = Label(window, text= 'Old PIN code', font=("Sans", "11"))
    lbl.grid(column=0, row=1)
    txt1 = Entry(window, width=10)
    txt1.grid(column=0, row=2)
    txt1.focus()
    lbl = Label(window, text= 'New PIN code', font=("Sans", "11"))
    lbl.grid(column=0, row=3)
    txt2 = Entry(window, width=10)
    txt2.grid(column=0, row=4)
    def change():
        new = txt2.get()
        old = txt1.get()
        if(new == old):
            talk("Same PIN not allowed!")
            return
        old = hashlib.md5(old.encode())
        old = old.hexdigest()
        if(len(new) < 4):
            talk("PIN must be between 4 to 8 characters!")
            return
        if(os.path.exists("Authfile")):
            auth_file = open("Authfile", "r")
            old_origin = auth_file.read()
            if(old_origin == old):
                    result = hashlib.md5(new.encode())
                    auth_file = open("Authfile", "w+")
                    auth_file.write(result.hexdigest())
                    auth_file.close()
                    print("AUTH: "+bcolors.WARNING+"Engine PIN changed"+bcolors.ENDC)
                    talk("PIN changed successfully boss.")
                    window.destroy()
                    launch_action_center(1)
            else:
                talk("Invalid old PIN.")
    btn = Button(window, text="Continue", bg="white", fg="red", command= change)
    btn.grid(column=0, row=5)
    return window