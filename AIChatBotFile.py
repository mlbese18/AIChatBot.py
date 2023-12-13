import tkinter as tk
from tkinter import filedialog
import PyPDF2
import os
import re
import nltk
import spacy
import string
from tkinter import *

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load("en_core_web_sm")

import ttkbootstrap as tb # to install do: pip install ttkbootstrap
from ttkbootstrap.scrolled import ScrolledText

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

global stop_words
global questionBank
questionBank = []
stop_words = set(stopwords.words('english'))

informationFile = "FlowerDoc2.0.txt"

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
        #printUserInput(msg)

        #generateAIResponce()
        #addNewInfo("newSentence", "newInfo", "newKeyWords")
        #clean_sentence(msg)
        #findQuestionWords(msg)
        #compareInfo("This is string one", "This is string two")
        keyMatching(large_string, capitalize_words(correct_typo(msg)))

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
    #print(sentences)
    #split the large_string into individual sentences
    if not isQuestion(userQuestion):
        if len(userQuestion.split()) >= 4:
            bot_response("Thank you for the information")
            addNewInfo(userQuestion, findQuestionWords(userQuestion), clean_sentence(userQuestion))
            return
        else:
            bot_response("Information does not meet requirements to add to database")
            bot_response("What else is on your mind?")
            return


    sentences = sentences.split("\n")
    i = 0
    currentBestScore = 0
    QSentences = []
    for sentence in sentences:
        #split the sentences into their sections (split by the "|")
        splitSentences = sentences[i].split("|")

        #compare questions
        if len(splitSentences) == 3:
            #print("Split sentences = ",splitSentences)
            currentQuestion = splitSentences[1]
            #print("currentQuestion = ", currentQuestion )
            userQuestionWords = findQuestionWords(userQuestion)
            if currentBestScore == compareInfo(currentQuestion, userQuestionWords):
                QSentences.append(sentences[i])
            elif (currentBestScore < compareInfo(currentQuestion, userQuestionWords)):
                QSentences = []
                currentBestScore = compareInfo(currentQuestion, userQuestionWords)
                QSentences.append(sentences[i])
                print("Question Score = " ,currentBestScore)
        i += 1
    j = 0
    if currentBestScore == 0:
        bot_response("This doesnt seem to be related to Sunflowers or roses")
        return
    currentBestScoreKeys = 0
    KSentences = []
    for sentence in QSentences:
        splitSentences = sentences[j].split("|")
        #compare key words
        #print("Splitsentence 2 = ",splitSentences)
        if len(splitSentences) == 3:
            currentKeys = splitSentences[2]
            userQuestionKeys = clean_sentence(userQuestion)
            if currentBestScoreKeys == compareInfo(currentKeys, userQuestionKeys):
                KSentences.append(sentences[j])
                print(currentBestScoreKeys)
            elif currentBestScoreKeys < compareInfo(currentKeys, userQuestionKeys):
                KSentences = []
                currentBestScoreKeys = compareInfo(currentKeys, userQuestionKeys)
                KSentences.append(sentences[j])
                print("Key Score = ",currentBestScoreKeys)
        j += 1
    if currentBestScoreKeys == 0:
        bot_response("This doesnt seem to be related to Sunflowers or roses")
        return
    #print("Ksentences = ",KSentences)
    #print("Current best Score: ", currentBestScore)
    k = 0
    finalResponse = ""
    for part in KSentences:
        part2 = KSentences[k].split("|")
        finalResponse = finalResponse + part2[0].strip() + ". "
        k += 1
    finalResponse = good_manner(userQuestion,finalResponse)
    collect_question(userQuestion)
    bot_response(finalResponse)
        #j = 0
        #for section in splitSentences:
            #print(splitSentences[j])
            #j += 1


    print(userQuestion)
    #get key words (cleaned) from input sentence
    #for each key word in input sentence, check if that word matches with a doc sentence, if it does, add to list and
    #for the next loop, use the list that we just created.
    #print(stuff)

def clean_sentence(sentence):
    emailsNoStop = []
    #for email in sentence:
    words = sentence.split()
    newSentence = ""
    i = 0
    #print(words)
    for word in words:
        #print(words[i])
        if word.lower() in stop_words:
            #print("word = ",word)
            #print("Delete word: ", words[i])
            #words.pop(i)
            #print("next Word: ", words[i])
            i += 1
        else:
            newSentence = newSentence + words[i] + " "
            #words.pop(i)
            i += 1                               #check

    newSentence = re.sub(r"[^a-zA-z0-9 ]", "", newSentence.lower())
    #print("old sentence",sentence)
    #print("New sentence = ",newSentence)

     # add key extra key words based on content
    color = ["hue", "colour", "brightness", "light", "tone", "yellow", "red", "blue", "purple", "black", "green","white", "gray", "pink", "orange", "pigment"]
    feature = ["look", "prickle", "head", "stem", "phenomenon", "mature", "seed", "econom", "petal", "behavior", "pattern", "structure", "character", "type", "variet", "breed", "fruit", "categor", "habit", "propert"]
    human_use = ["oil","medicinal", "cook", "product", "food", "industry", "subject", "purpose", "capture", "test", "feed", "appl"]
    good = ["help", "aid", "improv", "role", "add", "enhance", "ideal", "effects", "inspire", "benefit", "rich", "importan", "contribute", "ability"]
    grow = ["cultivate", "zone", "environment", "require", "temperature", "condition", "moisture", "soil"]
    culture = ["cultural", "symbol","metaphor", "art", "literature", "theme", "belief", "represent", "folk", "myth", "associate", "language"]
    history = ["fossil", "native", "acient", "introduce"]
    for c in color:
        if c in newSentence:
            newSentence = newSentence + "color "
            break
    # find if content relate to feature
    for f in feature:
        if f in newSentence:
            newSentence = newSentence + "feature "
            break
    # find if content relate to human use
    for u in human_use:
        if u in newSentence:
            newSentence = newSentence + "human use "
            break
    # find if content relate to benifit
    for g in good:
        if g in newSentence:
            newSentence = newSentence + "good "
            break
    # find if content relate to grow
    for gr in grow:
        if gr in newSentence:
            newSentence = newSentence + "grow "
            break
    # find if content relate to culture
    for cul in culture:
        if cul in newSentence:
            newSentence = newSentence + "culture "
            break
    # find if content relate to color
    for h in history:
        if h in newSentence:
            newSentence = newSentence + "history "
            #print("111")
            break

    #print("Added New sentence = ",newSentence)
    return newSentence

#Add the question words
def findQuestionWords(sen):
    questionWords = []
    temp = ""
    senlowercase = sen.lower().replace("\\r\\n", "" ).split()
    # where(any capital words after to/of/in/on/at/from):
    where_regex = re.compile(r'to [\w+ ]*[A-Z][a-z]+|of [\w+ ]*[A-Z][a-z]+|in [\w+ ]*[A-Z][a-z]+|on [\w+ ]*[A-Z][a-z]+|at [\w+ ]*[A-Z][a-z]+|from [\w+ ]*[A-Z][a-z]+')
    if where_regex.search(sen):
        temp = temp + "where "

    # when/how long (day/year/centry...)
    timelist = ["day", "year", "date", "era", "future", "hour", "second", "season", "month", "moment", "while", "am", "pm", "week", "centur", "summer", "winter", "fall", "autumn", "spring", "morning", "noon", "evening", "night",
                "january", "February", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "period", "during", "bloom", "when"]
    for w in timelist:
        if w in senlowercase and "when how long" not in temp:
            temp = temp + "when how long "

    # why (causal words + infinitive verb)
    causal = ["cause", "due", "for", "contribute to", "enhance", "since", "incase", "according", "result", "in order to", "as", "so", "reason", "therefore", "consequen", "thus", "then"]
    for w in causal:
        if w in senlowercase and "why" not in temp:
            temp = temp + "why "
    to_and_verb = re.findall(r'to \w+',sen)
    to_and_verb = to_and_verb[0] if to_and_verb else ""
    text = nltk.word_tokenize(to_and_verb)
    tag = nltk.pos_tag(text)
    for x in tag:
        if x[1] == "VB" and "why" not in temp:
            temp = temp + "why "

    # what (be)
    whatlist = ["be", "is", "are", "was", "were", "has", "have", "can", "could", "should", "will", "would", "known for"]
    for w in whatlist:
        if w in senlowercase and "what" not in temp:
            temp = temp + "what "

    # how (verb)
    texthow = nltk.word_tokenize(sen)
    taghow = nltk.pos_tag(texthow)
    for x in taghow:
        if (x[1] == "VB" or x[1] == "VBD" or x[1] == "VBG" or x[1] == "VBN" or x[1] == "VBP" or x[1] == "VBZ") and "how" not in temp:
            temp = temp + "how "

    # a default question word

    if temp == "":
        temp = "what how"
        #temp = "NONE"
    questionWords.append(temp)

    #print("Question words: ", questionWords )
    questionWordString = ""
    for word in questionWords:
        questionWordString = questionWordString + word
    #print(questionWordString)


    return(questionWordString)

def compareInfo(string1, string2):
    stringScore = 0
    for word1 in string1.split():
        #print(word1)
        for word2 in string2.split():
            if word1 == word2:
                #print("Word for score = " , word1)
                stringScore += 1

    #print("String Score = ", stringScore)
    return stringScore




#put the info back into the file
global newData
newData = "new data"
def addNewInfo(newSentence, infoType, keywords):
    with open(informationFile, 'a') as file:
            file.write(capitalize_words(correct_typo(newSentence)) + " | " + infoType + " | " + keywords +"\n")

# just chech the beginning of the sentence for the question words
# split the string, use the first value in the list of words to check for question words
# if not a question, add the info to the file (include the infotype (question words) and keyWords)
def isQuestion(sentence):
    list = sentence.split()
    checkWord = list[0].lower()
    questionWordList = ["what", "where", "when", "why", "how", "who", "is", "could"]
    isQuestion = False
    for check in questionWordList:
        if checkWord == check:
            isQuestion = True
    return isQuestion

def good_manner(input, re):
    inputText = input.lower()
    response = re
    if "please" in inputText:
        response = "Thanks for asking. " + response
    if "thanks" in inputText:
        response = "Your welcome, here what I found. " + response
    if "good morning" in inputText:
        response = "Good morning. " + response
    if "good evening" in inputText:
        response = "Good evening. " + response
    if "good afternoon" in inputText:
        response = "Good afternoon. " + response
    if "good night" in inputText:
        response = "Good night. " + response
    if "hi" in inputText or "hello" in inputText:
        response = "Hello. " + response
    return response

def correct_typo(input):
    inputText = input.lower()
    response = "Did you mean "
    flower = ["floowers", "flooer", "frower", "fiewer", "floww", "flooe", "flooor", "flouer", "follwer", "flowerey", "flor", "flowin", "fewwer", "flowerly", "lowwer", "loewer", "slowey", "fowar",
              "flowly", "flowes"]
    for i in flower:
        if i in inputText:
            if response != "Did you mean ":
                response = response + ", "
            response = response + "\"flower\" for \"" + i +"\""
            inputText = inputText.replace(i, "flower")
    sun = ["suasn", "sund", "suran", "sugns", "saund", "sgn", "sunn", "swun", "suana", "sundy", "sut", "spune", "kun", "sauan", "scna", "soutn", "sytun", "suh", "sunce"]
    for i in sun:
        if i in inputText:
            if response != "Did you mean ":
                response = response + ", "
            response = response + "\"sun\" for \"" + i +"\""
            inputText = inputText.replace(i, "sun")
    sunflower = ["sinflower", "sunflowes", "saflower", "sunflour", "sunfower", "lyrflower", "sponflower", "sunbloker", "aunflower", "zunflower", "xunflower", "dunflower",
                  "eunflower", "wunflower", "synflower", "shnflower", "sjnflower", "s8nflower", "s7nflower", "subflower"]
    for i in sunflower:
        if i in inputText:
            if response != "Did you mean ":
                response = response + ", "
            response = response + "\"sunflower\" for \"" + i +"\""
            inputText = inputText.replace(i, "sunflower")
    rose = ["roseta", "riase", "risqe", "rosett", "remose", "rosess", "proce", "risde", "rasie", "rhose", "broze", "forse", "prosse", "rese", "rouste", "gose", "rlse", "risj", "ciose"]
    for i in rose:
        if i in inputText:
            if response != "Did you mean ":
                response = response + ", "
            response = response + "\"rose\" for \"" + i +"\""
            inputText = inputText.replace(i, "rose")
    color = ["colol", "coord", "couslor", "conour", "colver", "colle", "colose", "coloed", "scholor", "colpor", "rollor", "cornor", "coclor", "collon", "culor", "coutor", "colom", "colar", "coolor", "colora"]
    for i in color:
        if i in inputText:
            if response != "Did you mean ":
                response = response + ", "
            response = response + "\"color\" for \"" + i +"\""
            inputText = inputText.replace(i, "color")
    human = ["wiman", "humand", "himans", "ohman", "humanty", "whiman", "humit", "hunman", "humnan", "hunam", "humant", "hgan", "wumen", "humain", "huamn", "humasn", "whoman", "hummm", "kuman", "juman"]
    for i in human:
        if i in inputText:
            if response != "Did you mean ":
                response = response + ", "
            response = response + "\"human\" for \"" + i +"\""
            inputText = inputText.replace(i, "human")

    response = response + "? if so then here is what I found. "
    if response != "Did you mean ? if so then here is what I found. ":
        bot_response(response)
    return inputText

def capitalize_words(input):
    text = input
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.label_)
        text = text.replace(ent.text, string.capwords(ent.text))
    return text



def collect_question(input):
    response = ""
    questionBank.append(input)
    print("Question bank ",questionBank)
    match = 0
    #with open(question_file,'r') as file:
    if len(questionBank) >= 1:
        for question in questionBank:
            if input in question:
                match = match + 1
        if match == 2:
            response = "You already asked this question, but here is the answer anyway "
            bot_response(response)
        if match == 3:
            response = "You have asked this question twice, but it seems you still want the answer. "
            bot_response(response)
        if match > 3:
            response = "You have asked this question " + str(match-1) + " times, but here is you answer. "
            bot_response(response)

    return

root.mainloop()
