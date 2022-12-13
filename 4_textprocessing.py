#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Processing
CPD Annual Reports -- clearance rates data
@author: polinarozhkova
"""
import PyPDF2
import os
import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import matplotlib.pyplot as plt
import seaborn as sns


base_path = r'/Users/polinarozhkova/Desktop/GitHub/final-project-homicide-cr-and-cpd-complaints/'
path = base_path + 'sustained_complaints/'


filenames = []
for filename in os.listdir(path):
    if filename.lower().endswith(".pdf"):
        filenames.append(os.path.join(path, filename))


complaints = []
for file in filenames:
    fileReader = PyPDF2.PdfFileReader(open(file, 'rb'))
    for pnum in range(fileReader.getNumPages()):
        pg = fileReader.getPage(pnum)
        complaints.append(pg.extractText())


def preprocess_text(complaints):
    processed_text = []
    for case in complaints:
        text = (case.replace('\n', ' ').replace('Abstracts of Sustained Cases ', '')
                .replace('Created by INDEPENDENT POLICE REVIEW AUTHORITY', '')
                .replace('Page 1 of 3', '')
                .replace('Page 2 of 3', '')
                .replace('Page 3 of 3', ''))
        processed_text.append(text)
    return processed_text


def rep_polarity(processed_text):
    polarity_list = []
    for text in processed_text:
        doc = nlp(text)
        polarity = doc._.blob.polarity
        polarity_list.append(polarity)
    return polarity_list


def plot_sentiment(df):
    sns.set_style("darkgrid")
    fig, ax = plt.subplots(sharex=True, figsize=(10, 5))
    sns.histplot(data=df, x='Polarity')
    ax.legend(loc='upper left')
    ax.set_title('Language used in Sustained Police Complaint Cases 2011-2013')
    ax.set_ylabel('Count')
    return ax


nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')
processed_text = preprocess_text(complaints)
sentiment_df = pd.DataFrame((rep_polarity(processed_text)), columns=['Polarity'])
plot_sentiment(sentiment_df)
plt.savefig(os.path.join(base_path + '/plots/' + 'textprocessing_plot.png'))

# Sources:
# https://stackoverflow.com/questions/72601282/python-extract-text-from-multiple-pdf-and-paste-on-excel

