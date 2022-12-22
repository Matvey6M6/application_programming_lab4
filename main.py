from txt_to_csv_third import Comment, get_dataset 

from matplotlib import pyplot as plt

from collections import Counter

from pymystem3 import Mystem #лемматизируем
import pymorphy2 #АНАЛиз на часть речи

import pandas as pd
import os
import re

def GetDatasetPath():
    '''Возвращает путь до датасета
    '''
    path = os.path.abspath("../application_programming_first_lab_and_dataset/dataset")
    return path

def GetDataframe(dataset_path: str) -> pd.DataFrame:
    '''Генерирует датафрейм
    '''
    
    dataset = get_dataset(dataset_path)
    
    texts = list()
    
    marks = list()
    
    for comment in dataset:
        texts.append(str(comment.comment))
        marks.append(str(comment.mark))
    
    dataframe = pd.DataFrame({"mark": marks, "text_of_comment":texts})
    return dataframe

def CheckNan(df: pd.DataFrame, column_name: str) -> bool:
    """проверка на пустоту в dataframe"""
    return df[column_name].isnull().values.any()

def StatInfo(df: pd.DataFrame, column_name: str) -> pd.Series:
    """возвращает статистическую информацию о столбце"""
    return df[column_name].describe()

def CountWords(df: pd.DataFrame, column: str) -> list:
    """возвращает список с кол-вом слов в каждом отзыве"""
    count_words = []
    for i in range(0, len(df.index)):
        text = df.iloc[i]
        text = text[column]
        words = text.split()
        count_words.append(len(words))
    return count_words

def ClearWords(words:str) -> str:
    '''Возвращает список чистых слов
    '''
    words_res = list()
    for i in range(0,len(words)):
        words[i] = words[i].strip()
        words[i] = words[i].lower()
        if words[i] != ' ': 
            words_res.append(re.sub("[^абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ \n]", "", words[i]))
    
    return words_res

def pos(word, morth=pymorphy2.MorphAnalyzer()):
    "Return a likely part of speech for the *word*."""
    return morth.parse(word)[0].tag.POS
    
def Lemmatize(df: pd.DataFrame, column: str):
    ''' Лемматизирует переданный датасет
    '''
    text_nomalized = str()
    for i in range(0, len(df.index)):
        
        text = df.iloc[i]
        text = text[column]
        words = text.split()
        
        words = ClearWords(words)
        
        for i in range(0,len(words)):
            text_nomalized += words[i]
            text_nomalized += ' '
        
    m = Mystem()
    lemmas = m.lemmatize(text_nomalized)
    
    functors_pos = {'ADJF'}  # function words
    
    lemmas = [lemma for lemma in lemmas if pos(lemma) in functors_pos]
    
    print(lemmas)
    
    lemmas = ClearWords(lemmas)
    
    #lemmas_res = [lemma for lemma in lemmas if not lemma == '' ]
    
    return lemmas
    
def LemmalizeClass(df: pd.DataFrame, column: str, mark: str) -> str:
    
    new_df = FilterClass(df, "mark", mark)
    
    lemmas = Lemmatize(new_df, column)
    
    word_dict = Counter(lemmas)
    
    word_dict = dict(word_dict) 
    
    result = dict()
    
    for key, value in word_dict.items():    
        if value > 500:
            result[key] = value
    
    return result


def Top10Lemmas(lemmatized: str) -> str:
    pass

if __name__ == '__main__':
    
    print("-"*99)
    
    columns = ['mark', 'text_of_comment', 'num_of_words']
    
    dataset_path = GetDatasetPath()
    dataframe = GetDataframe(dataset_path)
    
    num_of_words = CountWords(dataframe, 'text_of_comment')
    
    dataframe[columns[2]] = pd.Series(num_of_words)
    
    dataframe[columns[2]] = pd.Series(num_of_words)
    print(dataframe)
    
    stat = dataframe[columns[2]].describe()
    print(stat)
    
    df_words_filtered = pd.DataFrame(dataframe[dataframe[columns[2]] <= 100])
    
    print(df_words_filtered)
    
    df_1 = pd.DataFrame(dataframe[dataframe[columns[0]] == '1'])
    
    print(df_1)

    stat_1 = df_1[columns[2]].describe()
    print('\nДля оценки 1:\n')
    print('Минимальное кол-во слов:', stat_1['min'])
    print('Максимальное кол-во слов:', stat_1['max'])
    print('Среднее кол-во слов:', stat_1['mean'])

    lemmatized_class = LemmalizeClass(dataframe, columns[1], '1')
    
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot()

    ax.bar(list(lemmatized_class.keys()), lemmatized_class.values(), color='g')

    plt.show()


    print("-"*99)