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

#input the 3k word file

global userInput
userInput = ''
#Ask for user input question

while userInput != "EXIT":
    print("placeholder")
    #Placeholder
