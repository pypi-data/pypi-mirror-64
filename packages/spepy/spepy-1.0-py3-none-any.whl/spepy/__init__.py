import os

def speak(string):
    """Speaks the sentence"""
    file = open(r"speak.vbs","w")
    file.write('Set Speak=CreateObject("sapi.spvoice")\nSpeak.Speak "%s"'%string)
    file.close()
    os.startfile(r"speak.vbs")

try:
    file = open(r"speak.vbs","r")
    file.close()
except:
    speak("Thank you for downloading this library. I'd like to thanks Aman Raj, my Quora friend for the idea. NOTE, This library is for windows only.")
    print("Thank you for downloading this library. I'd like to thanks Aman Raj, my Quora friend for the idea.\nNOTE, This library is for windows only.")
    
