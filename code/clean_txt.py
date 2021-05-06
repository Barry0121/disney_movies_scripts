import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def clean_lines(astring):
    '''
    Stem words and removing stop words

    :param astring: raw string with stop words and un-stemmed words
    :return: lowered, without stop word, stemmed version of astring
    '''
    # https://stackoverflow.com/questions/24517722/how-to-stop-nltk-stemmer-from-removing-the-trailing-e
    # https://www.nltk.org/howto/stem.html
    line = re.sub('[^a-zA-Z]', ' ',astring) # check letter are valid
    line = line.lower()
    line = line.split()
    # stem words or turn all tenses to present tense
    ps = PorterStemmer()
    # remove stopwords & add not to it
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    line = [ps.stem(word) for word in line if not word in set(all_stopwords)]
    line = ' '.join(line)
    return line

def clean_txt(fp, scene_delimiter, start=0, end=None):
    """
    Read in txt file from path and extract characters, dialogue, and stage setup

    :param fp: string location of the txt file
    :param scene_delimiter: a 2 elements tuple of character symbol containing the stage setup instruction
    :param start: default={0}, start of the character dialogue
    :param end: default={None}, end of the character dialogue
    :return: a dataframe containing the character, dialogue, and stage setup information
    """
    chars = []
    words = []
    # scene_setup = []
    left = scene_delimiter[0]
    right = scene_delimiter[1]
    scene = False
    new_char = True
    line_nums = []
    with open(fp, 'r', encoding='utf-8') as infile:
        for num_l, line in enumerate(infile):
            if (num_l < start) or ((num_l > end) and (end != None)):
                continue
            num_l += 1
            s = line
            if not new_char:
                if ':' in line and '               ' not in line:
                    pass
                else:
                    words[-1] += line
            if ':' in line:
                if '               ' in line:
                    words[-1] += line
                    continue
                line_nums += [num_l]
                words += [line.split(':')[1]]
                chars += [line.split(':')[0]]

                new_char = False

    chars_words = np.array(list(zip(chars, words,line_nums)))
    # 2) put lines into a df & store it
    draft = pd.DataFrame(chars_words,columns = ['chars','lines','line_num'])
    # 3) add scene setup column & remove it from current line
    draft['scene_setup'] = draft.lines.apply(get_scene_setup,args=(left,right))
    draft['mod_lines'] = draft.lines.apply(remove_scene_setup,args=(left,right))
    return draft

def get_scene_setup(string,left,right):
    '''
    helper for clean_txt()
    get scence setup
    '''
    s = string
    # left = scene_delimiter[0]
    # right = scene_delimiter[1]
    scene_setup = s[s.find(left):s.find(right)+1]
    return scene_setup

def remove_scene_setup(string,left,right):
    '''
    helper for clean_txt()
    remove scence setup
    '''
    s = string
    # left = scene_delimiter[0]
    # right = scene_delimiter[1]
    s = string.replace('\n',' ')
    scene_setup = s[s.find(left):s.find(right)+1]
    if scene_setup == '':
        pass
    else:
        s = string.replace(scene_setup,' ')
    return s

