from tokenize import String
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# nltk.download('punkt')


def stemming_word(word):
    porter_stemmer = PorterStemmer()
    stemmed_words = porter_stemmer.stem(word)  # antony -> antoni
    return stemmed_words


def stemming_text(text):
    words = str(text).strip().split()
    porter_stemmer = PorterStemmer()
    words = [porter_stemmer.stem(word) for word in words]
    answer_text = ""
    for word in words:
        answer_text += word + " "
    return answer_text.strip()


def stemming_list(text_list):
    for i, word in enumerate(text_list):
        text_list[i] = stemming_text(word)  # antony -> antoni
    return text_list


def delete_stop_words(matrix):
    my_stopwords = stopwords.words("english")
    my_list = ["in", "to", "where"]
    new_matrix = list()
    my_stopwords = [el for el in my_stopwords if el not in my_list]
    for term in matrix:
        if term not in my_stopwords and term != " ":
            new_matrix.append(term)
    new_text = ""
    for i, term in enumerate(new_matrix):
        new_text += term
        if i != len(new_matrix) - 1:
            new_text += " "
    return new_text


def stemming(text):
    words = word_tokenize(text)  # ["Ahmed", "Mohamed"]
    porter_stemmer = PorterStemmer()
    stemmed_words = [porter_stemmer.stem(word) for word in words]
    return stemmed_words


def tokenization_and_stemming(words):
    return stemming(delete_stop_words(words))
