#Think compares a list of srtings to a sample and returns the best matching member
#Think expects the 1th index of the list objects to be the target string(Question)
import difflib
import speech_recognition as sr
from talk import *

listener_error = 0

def sub_listen():
    global listener_error
    if(listener_error):
        print("Engine: Write your reply please...")
        return str(input()).lower()
    r = sr.Recognizer()
    while(1):
            try:
                with sr.Microphone() as source2:
                    r.adjust_for_ambient_noise(source2, duration=0.2)
                    audio2 = r.listen(source2)
                    Text = r.recognize_google(audio2)
                    Text = Text.lower()
                    print("Command: "+bcolors.OKBLUE+Text+bcolors.ENDC)
                    return Text
            except sr.RequestError as e:
                listener_error = 1
                print("NEURAL RESPONSE: Please write reply, can not listen due to an error with listener")
                print("Engine: Write your reply please...")
                return str(input()).lower()
            except sr.UnknownValueError:
                return 0

def compare(sample, testing):
    #Currently just compare the strings and send a value 0 to 1
    result =  difflib.SequenceMatcher(a=sample.lower(), b=testing.lower())
    return result.ratio()

def think(sample, list):
    y = 0
    target = [0, 0, 0, 0, 0]
    for i in list:
        x = compare(sample, i[1])
        if(x >= y):
            target = [i[0], i[1], i[2], sample, list]
            y = x
    return target

def think_except(sample, id, list):
    y = 0
    target = [0, 0, 0, 0, 0]
    for i in list:
        if(id == i[0]):
            list.remove(i)
            continue
        else:
            x = compare(sample, i[1])
            if(x >= y):
                target = [i[0], i[1], i[2], sample, list]
                y = x
    return target

def nural_ask(neural_response):
    print("NEURAL RESPONSE: Did you mean "+bcolors.OKCYAN+bcolors.BOLD+neural_response[1]+bcolors.ENDC+bcolors.ENDC+"?")
    talk("Did you mean "+neural_response[1]+"?")
    #Ask and expect a positive response
    response = sub_listen()
    if(response and 
    (response.find("yes") > -1
        or response.find("yep") > -1
        or response.find("affirmative") > -1
        or response.find("yah") > -1
        or response.find("yeah") > -1)):
        return neural_response[2]
    else:
        #If positive return the value, if no ask if wanna continue
        print("NEURAL RESPONSE: "+bcolors.OKCYAN+"Do you wish to continue in this topic?"+bcolors.ENDC)
        talk("Do you wish to continue in this topic?")
        #If positive return the think except value, if no abort
        response = sub_listen()
        if(response and 
        (response.find("yes") > -1
            or response.find("yep") > -1
            or response.find("affirmative") > -1
            or response.find("yah") > -1
            or response.find("yeah") > -1)):
            sub_response = think_except(neural_response[3], neural_response[0], neural_response[4])
            if(len(sub_response) == 5):
                #Recall self
                return nural_ask(sub_response)
            else:
                return 0
        else:
            print("Engine: "+bcolors.OKGREEN+"Sub-command dismissed"+bcolors.ENDC)
            return "Dismiss"
            
def nural_think(question, result):
    neural_response = think(question, result)
    if(len(neural_response) == 5):
        r = nural_ask(neural_response)
        if(r == "Dismiss"):
            return "Dismiss"
        else:
            return r
    else:
        return 0