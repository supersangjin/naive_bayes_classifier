# -*- coding: utf-8 -*-
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier
import json

f = open("text_data.txt", "r")

data = json.loads(f.read())

print(data)

subjectTrainer = Trainer(tokenizer)

for subject in data:
    if subject["grade"] != "?":
        review = subject["comment"].replace('.', '\n').split("\n")
        for li in review:
            if len(li.strip()) != 0:
                subjectTrainer.train(li, subject["grade"])

subjectClassifier = Classifier(subjectTrainer.data, tokenizer)

unknownInstance = "hello."
classification = subjectClassifier.classify(unknownInstance)

print(classification)