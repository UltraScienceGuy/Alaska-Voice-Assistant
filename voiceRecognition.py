import speech_recognition as sr
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
from selenium import webdriver
from pynput.keyboard import Key, Controller, Listener
import requests
keyboard = Controller()

num = 1

executable_letters = ["t"]
def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("Alaska : ", output)

    toSpeak = gTTS(text=output, lang='en', slow=False)
    # saving the audio file given by google text to speech
    file = str(num) + ".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Speak...")

        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit=5)
    print("Stop.")  # limit 5 secs

    try:

        text = rObject.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text

    except:

        assistant_speaks("Could not understand your audio, Please try again !")
        return 0

def enter():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def newtab():
    with keyboard.pressed(Key.ctrl):
        keyboard.press("t")
        keyboard.release("t")

def search():
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    driver.get('http://www.google.com')
    assistant_speaks("What would you like to search the web for?")
    search_phrase = get_audio()
    assistant_speaks("Ok. Searching the web for " + search_phrase + ".")
    keyboard.type(search_phrase)
    enter()
    get_results = driver.find_element_by_id("search")
    print(get_results.text)
    #assistant_speaks("Which link would you like to click on?")


def search_website():
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    driver.get('http://www.google.com')
    newtab()
    assistant_speaks("Alright! What website would you like to search?")
    website_search = get_audio().lower()
    if website_search == "youtube":
        keyboard.type("https://www.youtube.com")
    elif website_search == "amazon":
        keyboard.type("https://www.amazon.com")
    assistant_speaks("What is the phrase you would like to enter?")
    search_term = get_audio()
    keyboard.type(search_term)
    enter()

# Driver Code
if __name__ == "__main__":
    while (1):

        assistant_speaks("What can I do for you?")
        text = get_audio().lower()

        if text == 0:
            continue

        if "search" in str(text):
            search()
        elif "website" in str(text):
            search_website()
        elif "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
            assistant_speaks("Ok bye, " + name + '.')
            break
