import os
import os.path
import csv
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import nltk
import string
import spacy
import re
from nltk.corpus import stopwords
from txt_to_csv_third import Comment, get_dataset 


nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_ru')
nltk.download('punkt')

def GetDataset():
    path = os.path.abspath("../application_programming_first_lab_and_dataset/dataset")
    return path

def GetDataframe(dataset_path: str) -> pd.DataFrame:

    dataset = get_dataset(dataset_path)

    texts = list()

    marks = list()

    for comment in dataset:
        texts.append(comment.comment)
        marks.append(comment.mark)

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
        #text = text.replace("\n", " ")
        #text = text.replace(",", "").replace(
        #    ".", "").replace("?", "").replace("!", "").replace("'", "")
        #text = text.lower()

        words = text.split()

        for i in range(0,len(words)):
            words[i] = words[i].strip()
            words[i] = re.sub(r'[@#$%^&*()<>?.,/|\\`~]', '',words[i])
            words[i] = words[i].lower()
            print(words)
        words.sort()
        count_words.append(len(words))
    return count_words

if __name__ == '__main__':

    print("-"*999)

    columns = ['mark', 'text_of_comment', 'num_of_words']

    dataset_path = GetDataset()
    dataframe = GetDataframe(dataset_path)
    num_of_words = CountWords(dataframe, 'text_of_comment')

    dataframe[columns[2]] = pd.Series(num_of_words)

    dataframe[columns[2]] = pd.Series(count_word)
    print(dataframe)

    stat = statistical_information(dataframe, columns[2])
    print(stat)

    filtered_reviews_df = filtered_dataframe_word(
        dataframe, columns[2], 100)
    print(filtered_reviews_df)

    #reviews_good_df = filtered_dataframe_class(
    #    dataframe, column_name[0], 'good')
    #reviews_bad_df = filtered_dataframe_class(
    #    dataframe, column_name[0], 'bad')

    print(reviews_bad_df)
    print(reviews_good_df)

    stat_good = statistical_information(reviews_good_df, column_name[2])
    print('\nДля положительных отзывов:\n')
    print('Минимальное кол-во слов:', stat_good['min'])
    print('Максимальное кол-во слов:', stat_good['max'])
    print('Среднее кол-во слов:', stat_good['mean'])

    stat_bad = statistical_information(reviews_bad_df, column_name[2])
    print('\nДля отрицательных отзывов:\n')
    print('Минимальное кол-во слов:', stat_bad['min'])
    print('Максимальное кол-во слов:', stat_bad['max'])
    print('Среднее кол-во слов:', stat_bad['mean'])

    #histogram(reviews_df, 'good', column_name[1])

    print("-"*999)
