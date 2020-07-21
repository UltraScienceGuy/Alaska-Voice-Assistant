import speech_recognition as sr
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
from selenium import webdriver
from pynput.keyboard import Key, Controller, Listener
import requests
import nltk
from nltk.stem import WordNetLemmatizer

keyboard = Controller()

num = 1

#So I added a machine learning chatbot feature...

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model

model = load_model('chatbot_model.h5')
import json
import random

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for tg in list_of_intents:
        if (tg['tag'] == tag):
            responses = random.choice(tg['responses'])
            break
    return responses


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

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
    assistant_speaks("Alright! What website would you like to search?")
    website_search = get_audio().lower()
    driver.get("https://amazon.com")
    search_bar = driver.find_element_by_name("field-keywords")
    assistant_speaks("What would you like to search for?")
    search_term = get_audio()
    search_bar.send_keys(search_term)
    enter()

def chat():
    assistant_speaks("What would you like to ask me?")
    msg = get_audio().lower()

    if msg != '':
        res = chatbot_response(msg)
        assistant_speaks(f'{res}')

# Driver Code

def driver_code():
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
            elif "chat" in str(text):
                chat()
            elif "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
                assistant_speaks("Ok bye, " + name + '.')
                break


num = 1

while num ==1:
    rObject = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak...")
        audio = rObject.listen(source, phrase_time_limit=10000000000)
        print("Stop")
        text = rObject.recognize_google(audio, language='en-US')
        print("You : ", text)

        if text == "Alaska":
            driver_code()
