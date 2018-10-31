# -*- coding: utf-8 -*-
# This is a Chatbot Project
"""
Created on Mon Oct 22 22:54:01 2018

@author: Mahbub - A - Rob
"""

# Import libraries
import numpy as np
import re
import time


# Read Data
lines = open("movie_lines.txt", encoding = "utf-8", errors = "ignore").read().split("\n")
conversations = open("movie_conversations.txt", encoding = "utf-8", errors = "ignore").read().split("\n")

# Clean Data and 
# Create a dictionary and map with the ID
id_mapping_line = {}
for line in lines:
    _line = line.split(" +++$+++ ")
    # print(_line)
    # Make sure we have five elements
    if len(_line) == 5:
        # store line id and line text only
        # id_mapping_line[_line[0]] contains only id
        # _line[4] contains line text
        id_mapping_line[_line[0]] = _line[4]
        
# Clean conversations data
# Create a list of conversations ids        
conversations_ids = []
# skip last empty row: use jupyter notebook for better data exploration visualization
# split(" +++$+++ ")[-1][1:-1].replace("'", "") 
# [-1] means last index
# [1:-1] remove leading and trailing square brackets
# use replace function to replace singel quote
# replace space
# only keep the comma
for conversation in conversations[:-1]:
    _conversation = conversation.split(" +++$+++ ")[-1][1:-1].replace("'", "").replace(" ", "")
    # append the clean conversation ids 
    # befor appending remove the comma
    conversations_ids.append(_conversation.split(","))
    

# Split questions and answers
questions = []    
answers = []
for conversation in conversations_ids: # take a single conversation
    for i in range(len(conversation) -  1): # split question and answer and store
        questions.append(id_mapping_line[conversation[i]])
        answers.append(id_mapping_line[conversation[i+1]])
        

# Function for cleaning text 
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"they're", "they are", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text) # replace 'll
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text) 
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"-+%$#@^\";:<>{}=.?,/*", "", text) # replace symbols
    return text


# Clean questions
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))


# Clean answers
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))
    

# Create a word counter dictionary to track number of occurances of words
word_occurance_dict = {}
for question in clean_questions: # take a single question
    for word in question.split(): # take a single word
        if word not in word_occurance_dict:
            word_occurance_dict[word] = 1 # we could do it in other way
        else:
            word_occurance_dict[word] += 1

for answer in clean_answers: # take a single question
    for word in answer.split(): # take a single word
        if word not in word_occurance_dict:
            word_occurance_dict[word] = 1 # we could do it in other way
        else:
            word_occurance_dict[word] += 1

# Create 2 dictionaries to observe the unique words occurances in both 
# questions and answers word occurance dictionaries
threshold = 20
question_unique_words_dict = {}
word_count = 0
for word, count in word_occurance_dict.items():
    if count >= threshold:
        question_unique_words_dict[word] = word_count # create key and value at the same time
        word_count += 1
    
answer_unique_words_dict = {}
word_count = 0
for word, count in word_occurance_dict.items():
    if count >= threshold:
        answer_unique_words_dict[word] = word_count # create key and value at the same time
        word_count += 1
    
# Token
tokens = ["<PAD>", "<EOS>", "<OUT>", "<SOS>"]
for token in tokens:
    question_unique_words_dict[token] = len(question_unique_words_dict) + 1

for token in tokens:
    answer_unique_words_dict[token] = len(answer_unique_words_dict) + 1
    
# Create the inverse dictionary
answer_reverse_unique_words_dic = {w_i: w for w, w_i in answer_unique_words_dict.items()}


# Add end of string token to the end of every answer
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'

# Translate all questions and answers into integers
# and replace all the words that were filtered by <OUT>    
questions_to_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in question_unique_words_dict:
            ints.append(question_unique_words_dict["<OUT>"])
        else:
            ints.append(question_unique_words_dict[word])
    questions_to_int.append(ints)
    
answers_to_int = []
for answer in clean_answers:
    ints = []
    for word in question.split():
        if word not in answer_unique_words_dict:
            ints.append(answer_unique_words_dict["<OUT>"])
        else:
            ints.append(answer_unique_words_dict[word])
    answers_to_int.append(ints)
            

# Sort clean questions and answers        
sorted_clean_questions = []    
sorted_clean_answers = []
for length in range(1, 25 + 1):
    for i in enumerate(questions_to_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_to_int[i[0]])
            sorted_clean_answers.append(answers_to_int[i[0]])


