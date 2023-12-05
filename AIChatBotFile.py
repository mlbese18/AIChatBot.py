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
        printUserInput(msg)

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


#GUI implimentation testing
def printUserInput (msg):
    print("UserInput: ",msg)

#Placeholder

root.mainloop()
