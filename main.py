from txt_to_csv_third import Comment, get_dataset
from matplotlib import pyplot as plt
import numpy as np
from pymystem3 import Mystem #лемматизируем
import pymorphy2 #АНАЛиз на часть речи
import pandas as pd
import os 
import string
import re


def GetDataset():
    path = os.path.abspath("../application_programming_first_lab_and_dataset/dataset")
    return path

def GetDataframe(dataset_path: str) -> pd.DataFrame:
    
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

def FilterClass(reviews_df: pd.DataFrame, column_name: str, class_name: str) -> pd.DataFrame:
    """возвращает новый отфильтрованный по метке класса dataframe"""
    result = pd.DataFrame(reviews_df[reviews_df[column_name] == class_name])
    return result

def FilterWords(reviews_df: pd.DataFrame, column_name: str, count: int) -> pd.DataFrame:
    """возвращает новый отфильтрованный по кол-вам слов dataframe"""
    result = pd.DataFrame(reviews_df[reviews_df[column_name] <= count])
    return result

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
    words_res = list()
    for i in range(0,len(words)):
        words[i] = words[i].strip()
        words[i] = words[i].lower()
        words_res.append(re.sub("[^абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]", "", words[i]))

    return words_res

def pos(word, morth=pymorphy2.MorphAnalyzer()):
    "Return a likely part of speech for the *word*."""
    return morth.parse(word)[0].tag.POS

def lemmatize(df: pd.DataFrame, column: str):
    text_nomalized = str()
    #for i in range(0, len(df.index)):
    for i in range(0, 10):

        text = df.iloc[i]
        text = text[column]
        words = text.split()

        words = ClearWords(words)

        for i in range(0,len(words)):
            text_nomalized += words[i]
            text_nomalized += ' '

    m = Mystem()
    lemmas = m.lemmatize(text_nomalized)

    functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}  # function words

    lemmas = [lemma for lemma in lemmas if pos(lemma) not in functors_pos]

    lemmas = ClearWords(lemmas)

    lemmas_res = [lemma for lemma in lemmas if not lemma == '' ]

    print(lemmas_res)

    return lemmas_res

def Top10Lemmas(lemmatized: str) -> str:


 if __name__ == '__main__':

    print("-"*99)
    
    columns = ['mark', 'text_of_comment', 'num_of_words']

    dataset_path = GetDataset()
    dataframe = GetDataframe(dataset_path)

    num_of_words = CountWords(dataframe, 'text_of_comment')

    dataframe[columns[2]] = pd.Series(num_of_words)

    dataframe[columns[2]] = pd.Series(num_of_words)
    print(dataframe)

    stat = StatInfo(dataframe, columns[2])
    print(stat)

    df_words_filtered = FilterWords(
        dataframe, columns[2], 100)

    print(df_words_filtered)

    df_1 = FilterClass(
        dataframe, columns[0], '1')

    print(df_1)

    stat_1 = StatInfo(df_1, columns[2])
    print('\nДля оценки 1:\n')
    print('Минимальное кол-во слов:', stat_1['min'])
    print('Максимальное кол-во слов:', stat_1['max'])
    print('Среднее кол-во слов:', stat_1['mean'])

    lemmatized = lemmatize(dataframe, columns[1])

    top10lemmas = Top10Lemmas(lemmatized)

    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot()

    ax.bar(list(word_dict.keys()), word_dict.values(), color='r')

    plt.show()

    print("-"*99)
