# -*- coding: utf-8 -*-
from konlpy.tag import Twitter
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier
import json

twitter = Twitter()

f = open("data.txt", "r")

data = json.loads(f.read())

gradeTrainer = Trainer(tokenizer)
loadTrainer = Trainer(tokenizer)
lectureTrainer = Trainer(tokenizer)

print("Training grade ...")
for subject in data:
    if subject["grade"] != "?":
        review = subject["comment"].replace('.', '\n').split("\n")
        for li in review:
            if len(li.strip()) != 0:
                gradeTrainer.train(li, subject["grade"])

print("Training load ...")
for subject in data:
    if subject["load"] != "?":
        review = subject["comment"].replace('.', '\n').split("\n")
        for li in review:
            if len(li.strip()) != 0:
                loadTrainer.train(li, subject["load"])

print("Training lecture ...")
for subject in data:
    if subject["lecture"] != "?":
        review = subject["comment"].replace('.', '\n').split("\n")
        for li in review:
            if len(li.strip()) != 0:
                lectureTrainer.train(li, subject["lecture"])


gradeClassifier = Classifier(gradeTrainer.data, tokenizer)
loadClassifier = Classifier(loadTrainer.data, tokenizer)
lectureClassifier = Classifier(lectureTrainer.data, tokenizer)

input = u""
classify_input = []

for element in twitter.pos(input):
    if element[1] == 'Noun':
        classify_input.append(element[0])
    elif element[1] == 'Verb':
        classify_input.append(element[0])
    elif element[1] == 'Adjective':
        classify_input.append(element[0])
    elif element[1] == 'Adverb':
        classify_input.append(element[0])
    elif element[1] == 'Exclamation':
        classify_input.append(element[0])
    elif element[1] == 'Alpha':
        classify_input.append(element[0])
    elif element[1] == 'KoreanParticle':
        classify_input.append(element[0])

text = " ".join(classify_input)

print(text)

gradeClassification = gradeClassifier.classify(text)
loadClassification = loadClassifier.classify(text)
lectureClassification = lectureClassifier.classify(text)

print("\n________________________________________GRADE________________________________________\n")
print(gradeClassification)
print("\n________________________________________LOAD_________________________________________\n")
print(loadClassification)
print("\n________________________________________LECTURE______________________________________\n")
print(lectureClassification)