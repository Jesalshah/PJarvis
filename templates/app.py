import numpy as np
from flask import Flask, request, jsonify, render_template
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import sys
import os

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[1].id)

@app.route('/')
def home():
    return render_template('index.html')
    if (request.method=='POST'):  	
    	hour = int(datetime.datetime.now().hour)
    	if hour>=0 and hour<12:
           engine.say("Good Morning!")
    	elif hour>=12 and hour<18:
           engine.say("Good Afternoon!")
    	else:
           engine.say("Good evening!")       
    
@app.route('/',methods=['GET', 'POST'])
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

@app.route('/',methods=['GET', 'POST'])
def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.

    except Exception as e:
        # print(e)    
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query

   
@app.route('/predict',methods=['GET', 'POST'])
def predict():
    while True:

    	query = takeCommand().lower() #Converting user query into lower case

        # Logic for executing tasks based on query
    	if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
        	speak('Searching Wikipedia...')
        	query = query.replace("wikipedia", "")
        	results = wikipedia.summary(query, sentences=2) 
        	speak("According to Wikipedia")
        	print(results)
        	speak(results)
        
    	elif 'open youtube' in query:
            	webbrowser.open("youtube.com")   
            
    	elif 'open google' in query:
            	webbrowser.open("google.com")
            
    	elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))
            
    	elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            
    	elif "stop" in query:
            speak("ok bye, have a good day")
            sys.exit()  
  
    predict()

if __name__ == "__main__":
    app.run(debug=True)