import speech_recognition as sr
import time
from gpiozero import LED
import os
from wakewords import *
import csv
from pinoutcommands import *

#selection functions

def fetchcommand(argument):
    switcher = {
        "one": one,
        "two": two ,
        "three": three ,
        "four": four,
        "five": five,
        "six": six,
        "seven": seven,
        "eight": eight,
        "nine": nine,
        "ten": ten,
        "eleven": eleven,
        "twelve": twelve
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "No match")
    # Execute the function
    print(func())
# recipe select function
def recipes():
    attempts = 0 ;
    os.system("aplay ./intro.wav") #response to wakeword
    while attempts < 3 :
        #swake.off()
        listentime = 6
        for j in range(4) :
            print("Choose Coffee Product")
            cp = recognize_speech_from_mic(recognizer, microphone)
            if cp["transcription"]:
                rcommands = cp["transcription"].lower()
                break
            if not cp["success"]:
                print("Did not recognize command.")
                j += 1
            else:
                j += 1
                if attempts < 2:
                    os.system("aplay ./psa.wav")
                    print("attempts=", attempts)
                if attempts > 1:
                    os.system("aplay ./error.wav")
                    os.system("aplay ./cancelling.wav")
                    rcommands = "--no transcription--"
                    print("attempts=", attempts)
                    break
                attempts = attempts + 1
        print("You said: {}".format(cp["transcription"]))
        print("lower case: {}".format(rcommands))
        try:  #exception when no transcription is made in 3 attempts, or does not match the dictionary
            while attempts < 3:
                cutval = set(rcommands.split())     #cut STT response string up into commands
                complete = list(cutval.intersection(recipedict.keys())) #intersect the command list with the recipe commands to see if there is a match
                keyword = complete[0] #take the first priority intersection, others not priority
                print("Matched Keyword:",keyword)
                kfunc = recipedict.get(keyword, "No keyword found")  #No keyword found when there is transcription but without any matches
                print("Test:" , kfunc)
                fetchcommand(kfunc)

                if cancel in rcommands:
                    os.system("aplay ./cancelling.wav")
                    print("Cancelling")
                    attempts = 3
                    break
                if wakeword in rcommands or wakeword2 in rcommands or wakeword3 in rcommands or wakeword4 in rcommands: 
                    attempts = 0
                    os.system("aplay ./intro.wav")
                    break
                else:
                    print("recipe not recognized")
                    
                if attempts < 2 :
                    os.system("aplay ./psa.wav")
                    print("attempts =", attempts)
                    attempts = attempts + 1
                    break
                if attempts > 1 :
                    os.system("aplay ./error.wav")
                    os.system("aplay ./cancelling.wav")
                    attempts = attempts + 1
                    break

        except Exception as e:
            print(e)
            print("No selection detected")
            attempts = attempts + 1
               
        
        
    wake = False
        
def sleep_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.dynamic_energy_threshold = True
        if attempts == 1:
            recognizer.adjust_for_ambient_noise(source, duration = .5)
        recognizer.pause_threshold = 0.5
        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        
        try:
            audio = recognizer.listen(source, phrase_time_limit = listentime)
        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
            try:
                response["transcription"] = recognizer.recognize_google(audio)
            except sr.RequestError:
                # API was unreachable or unresponsive
                response["success"] = False
                response["error"] = "API unavailable"
                
            except sr.UnknownValueError:
                # speech was unintelligible
                response["error"] = "Unable to recognize speech"
            except sr.WaitTimeoutError:        
                response["error"] = "No speech recorded"
                pass
            else:
                response["error"] =  "No speech recorded"
        #Run timeout exception
        except sr.WaitTimeoutError:
            print("Timeout recording")
            pass

    return response


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.dynamic_energy_threshold = True
        # recognizer.adjust_for_ambient_noise(source, duration = .5)
        recognizer.pause_threshold = 2
        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        
        try:
            recognizer.adjust_for_ambient_noise(source, duration = .5)
            audio = recognizer.listen(source, phrase_time_limit = listentime, timeout = 6)
            print("audio recorded")
        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
            try:
                response["transcription"] = recognizer.recognize_google(audio)
                print("transcription received")
            except sr.RequestError:
                # API was unreachable or unresponsive
                response["success"] = False
                response["error"] = "API unavailable"
            except sr.UnknownValueError:
                # speech was unintelligible
                response["error"] = "Unable to recognize speech"
            except sr.WaitTimeoutError:        
                response["error"] = "No speech recorded"
                pass
            else:
                response["error"] =  "No speech recorded"
        #Run timeout exception
        except sr.WaitTimeoutError:
            print("Timeout recording")

    return response
#microphone initialization and adjustment
recipedict = {}
recognizer = sr.Recognizer()
recognizerwake = sr.Recognizer()
microphone = sr.Microphone(device_index=2)
#importing CSV file for recipes
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
with open('recipes.csv') as recipe_file:
    recipe_reader = csv.reader(recipe_file)
    line_count = 0
    for row in recipe_reader:
        if line_count == 0:
            print("Importing list")
        
        else:
            recipedict.update({row[0]:row[1]})
            print("Imported", row[0], " as a keyword for function ", row[1])
        line_count += 1
    print("Imported ", line_count," keywords.")
        
wake = False
attempts = 0
listentime = 2
#initializing the GPIO pins as outputs on the Pi, the first 8 GPIO pins on the left side are used by default
sone = LED(17)
sone.off()
stwo = LED(27)
stwo.off()
sthree = LED(22)
sthree.off()
sfour = LED(10)
sfour.off()
sfive = LED(9)
sfive.off()
ssix = LED(11)
ssix.off()
sseven = LED(5)
sseven.off()
seight = LED(6)
seight.off()
swake = LED(0)
swake.on()
sleeping = True
order = True
while True:
    listentime = 1.6
    swake.off()
    if wake == True:
        recipes()
    print("Awaiting Wake Word")
    while sleeping == True :
        ww = sleep_from_mic(recognizer, microphone)
        if ww["transcription"]:
            break
        if not ww["success"]:
            print("Unable to recognize voice")
        
            
    print("You said: {}".format(ww["transcription"]))
        
    if wakeword in ww["transcription"] or wakeword2 in ww["transcription"] or wakeword3 in ww["transcription"] or wakeword4 in ww["transcription"]: 
        wake = True
        #subprocess.call("/home/pi/dspeech/PythonVC/volume.sh", shell="True")
        #os.system("aplay ./intro.wav")
        #video("intro.wav")
        #speech="What would you LIKE?"
        #subprocess.call(['espeak', '-v', 'en-jt', '-p', '99', speech]
            
    else:
    
        print("no wake word detected")
        wake = False
        
