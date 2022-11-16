"""Script file to for initial text analysis pre-processing"""
from nltk import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from data_access import load_from_db, save_to_db

sentence_tokenizer = PunktSentenceTokenizer()


def train_sentence_tokenizer() -> None:
    """Train sentence tokenizer on all article text"""
    global sentence_tokenizer

    training_text = ""

    article_list = load_from_db(db_key_string='filtered_articles')

    for article in article_list:
        training_text += article['maincontent']

    sentence_tokenizer = sentence_tokenizer.train(training_text)

    return None


def tokenize_articles() -> None:
    """Creates lists of word and sentence tokens for each article"""
    article_list = load_from_db(db_key_string='filtered_articles')

    for article in article_list:
        article['sentences'] = sentence_tokenizer.tokenize(article['maincontent'])
        article['words'] = word_tokenize(article['maincontent'])

    # Save the updated list for later use
    save_to_db(db_key_string='filtered_articles',
               data_to_save=article_list)

    return None


def strip_stopwords() -> None:
    """Strips stopwords from the article tokens"""
    article_list = load_from_db(db_key_string='filtered_articles')
    stop_words = set(stopwords.words('english'))

    for article in article_list:
        # Strip stopwords from word tokens
        article['words'] = [word for word in article['words'] if word not in stop_words]

        # Strip stopwords from sentence tokens
        article['sentences'] = [remove_sentence_stopwords(sentence) for sentence in article['sentences']]

    # Save the updated list for later use
    save_to_db(db_key_string='filtered_articles',
               data_to_save=article_list)

    return None


def remove_sentence_stopwords(input_sentence: str) -> str:
    """Take a sentence, remove stopwords, and return a sentence"""
    stop_words = set(stopwords.words('english'))

    word_list = word_tokenize(input_sentence)
    word_list = [word for word in word_list if word not in stop_words]
    returned_sentence = " ".join(word_list)

    return returned_sentence


def remove_numeric_tokens():
    article_list = load_from_db(db_key_string='filtered_articles')
    numchars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    for article in article_list:
        for numchar in numchars:
            article['words'] = [word for word in article['words'] if numchar not in word]

    # Save the updated list for later use
    save_to_db(db_key_string='filtered_articles',
               data_to_save=article_list)

    return None


def stem_sentence(input_sentence: str) -> str:
    """Take a sentence, stem words, and return a sentence"""
    ps = PorterStemmer()

    word_list = word_tokenize(input_sentence)
    word_list = [ps.stem(word) for word in word_list]
    returned_sentence = " ".join(word_list)

    return returned_sentence


def stem_article_words() -> None:
    """Stem words included in article word and sentence lists"""
    article_list = load_from_db(db_key_string='filtered_articles')
    ps = PorterStemmer()

    for article in article_list:
        # Stem word tokens
        article['words'] = [
            {
                'original_word': word,
                'stemmed_word': ps.stem(word)
            }
            for word in article['words']
        ]

        # Stem sentence tokens
        article['sentences'] = [
            {
                'original_sentence': sentence,
                'stemmed_sentence': ps.stem(sentence)
            }
            for sentence in article['sentences']
        ]

    # Save the updated list for later use
    save_to_db(db_key_string='filtered_articles',
               data_to_save=article_list)

    return None

