from nltk import PunktSentenceTokenizer
from nltk.tokenize import word_tokenize

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
