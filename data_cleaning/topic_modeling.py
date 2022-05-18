import pandas as pd
import numpy as np
from gensim import corpora


def read_excel_file(fileName):
    final_data_list = []
    try:
        file_data_corpus = pd.read_excel(fileName, sheet_name='bi_trigram_data')
        file_data_bow = pd.read_excel(fileName, sheet_name='bag_words_data')
        row, column = file_data_corpus.shape
        for i in range(10):
            row_data = file_data_corpus.iloc[i]
            row_data = row_data.dropna()
            row_data = row_data.tolist()
            del row_data[0]
            final_data_list.append(row_data)
        print(final_data_list)
    except FileNotFoundError as err:
        print(err)
    return file_data_corpus


def create_corpus(texts):
    id2bows = corpora.Dictionary(texts)
    corpus = [id2bows.doc2bow(text) for text in texts]

    print(id2bows)
    print(corpus)


if __name__ == '__main__':
    file_name = 'pre_processed_data.xlsx'
    data_frame = read_excel_file(file_name)
    data_to_bow = create_corpus(data_frame)
