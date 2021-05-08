#%%
import numpy as np
import pandas as pd
import os
# nltk components
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk.corpus import subjectivity
# from nltk import tokenize
# from nltk.corpus.reader.plaintext import PlaintextCorpusReader

def analysis_txt(fp: str, analyzer):
    '''
    Scale up a specific analysis process for a entire txt file of scripts
    :param fp: str filepath of the cleaned script line file
    :param analyzer: textual analysis function of choice
    :return: a numpy array corresponding to the analysis result by lines
    '''
    result = []
    with open(fp, 'r', encoding="utf-8") as file:
        for line in file:
            result.append(analyzer(line))
    return np.array(result)



# Here are some possible candidate for analyzers

def vader_sentiment_intensity(line: str): # WARNING: This method isn't good lol
    '''
    Simple sentiment intensity analysis function using the VADER package from NLTK
    This is only a early test run; it doesn't represent the expected performance
    NOTICE: VADER doesn't contain a test for the success rate

    Citation: Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
    Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and
    Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

    :param line:
    :return: str in ['neg', 'neu', 'pos', 'compound'] representing the most probable attitude of the line
    '''
    vader = SentimentIntensityAnalyzer()
    result = vader.polarity_scores(line)
    return max(result, key=lambda x: result[x])

#%%
def build_line_corpus(name: str):
    '''
    This function build a corpus file with only lines that is ready to be processed
    by the nltk reader functions with faster speed

    :param name: a str for the name of the csv containing the specific scripts' lines
    :return: True if the file is created successfully, False otherwise
    '''
    path = os.path.join('cleaned_scripts', f'{name}.csv')
    outpath = os.path.join('corpus', f'{name}.txt')
    df = pd.read_csv(path)
    lines = df['mod_lines'].values # an array of lines

    # write the words in the corpus
    with open(outpath, mode='a', encoding='utf-8') as out:
        for i, line in enumerate(lines):
            try:
                out.write(line+'\n')
            except:
                print('invalid line: ', i, line)
                if line == np.NaN:
                    continue

    return f'{name}.csv written into {outpath}'

