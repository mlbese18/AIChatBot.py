import tkinter as tk
from tkinter import filedialog
import PyPDF2
import os
import re
import nltk
from tkinter import *

import ttkbootstrap as tb # to install do: pip install ttkbootstrap
from ttkbootstrap.scrolled import ScrolledText

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

informationFile = "FlowerDocInfo.txt"

#create the GUI
# Try other themes: superhero darky cyborg vapor lumen minty morph
root = tb.Window(themename="solar")
root.title("Simple Virtual Assistant")
root.geometry("")

def send_message(event=None):
    msg = my_message.get()
    if msg.strip() != "":
        chat_window.insert(tb.END, "You: " + msg + "\n")
        my_message.set("")
        #Run our functions here
        extract_info()
        printUserInput(msg)
        keyMatching(large_string, msg)
        generateAIResponce()
        addNewInfo("newSentence", "newInfo", "newKeyWords")

def bot_response(response):
    chat_window.insert(tb.END, "Agent: " + response + "\n")

chat_window = ScrolledText(root, width=60, height=20, wrap=WORD, autohide=True, bootstyle="info", font=('Verdana', 15))
chat_window.grid(row=0, column=0, columnspan=2, padx=15, pady=15)

my_message = tb.StringVar()
entry_field = tb.Entry(root, textvariable=my_message, width= 48, bootstyle="info", font=('Verdana', 15))
entry_field.grid(row=1, column=0)
entry_field.bind("<Return>", send_message)

send_button = tb.Button(root, text="Send", command=send_message, width=6, bootstyle="outline")
send_button.grid(row=1, column=1)

topic = 'Titanic movie'
initial_response = "Hi, I am your virtual assistant, ask me anything about " + topic

root.after(500, bot_response(initial_response))


#input the 3k word file
def extract_info():
   global file_path
   file_path = informationFile
   if file_path:
        try:
            fileMade = True
            if not os.path.exists(file_path):
                fileMade = False
                with open(informationFile, 'w'): pass


            with open(file_path, 'r') as file:
                global large_string
                large_string = ""
                for line in file:
                    line.strip()
                    large_string = large_string + line

        except Exception as e:
            print("Fail")

#find lines that have the same key words as the input sentence
def keyMatching(sentences, userQuestion):
    print(sentences)
    #split the large_string into individual sentences
    sentences = sentences.split("\n")
    i = 0
    for sentence in sentences:
        #split the sentences into their sections (split by the "|")
        splitSentences = sentences[i].split("|")
        j = 0
        for section in splitSentences:
            print(splitSentences[j])
            j += 1

        i += 1
    print(userQuestion)
    #get key words (cleaned) from input sentence
    #for each key word in input sentence, check if that word matches with a doc sentence, if it does, add to list and
    #for the next loop, use the list that we just created.
    #print(stuff)

#put the info back into the file
global newData
newData = "new data"
def addNewInfo(newSentence, infoType, keywords):
    with open(informationFile, 'a') as file:
            file.write(newSentence + " | " + infoType + " | " + keywords +"\n")


#GUI implimentation testing
def printUserInput (msg):
    print("UserInput: ",msg)
    print(large_string)

def generateAIResponce ():
    bot_response(large_string)
    print("placeholder")

#Placeholder

root.mainloop()
