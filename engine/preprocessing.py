import re
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.regexp import  WhitespaceTokenizer
from nltk.corpus import stopwords

# Предобработка текста. Для описанной задачи подходит сравнение на уровне предложений. 
# Для большей части операций обработки использую инструменты nltk + re

def clear_digits(text):
    return re.sub(r"\d+", "", text)


def clear_emails(text):
    return re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", '', text)


def clear_url(text):
    return re.sub(
        r"(?i)\b((?:(http(s)?)?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
        "", text)


# чистим "левые" символы, кроме !?.; - которые могут означать конец предложения.
def clear_symb(text):
    return re.sub(r"[~`@«»#$%^&*()_+=\-:№\"\[\]\\/|',\n]", '', text)


# чистим !?.;.
def clear_endings(text):
    return re.sub(r"[!?.;]", '', text)


def preprocess_text(text):
    """
    предобработка, токенизация по предложениям, удаление дублей.

    Args:
        text ([type]): [description]
    """

    #text = text.lower()

    # убираем числа, email, гиперрсылки

    #text = text.encode('utf-8')

    text = clear_emails(text)
    text = clear_url(text)
    text = clear_digits(text)
    text = clear_symb(text)

    # выделяем предложения
    sentence_tokenizer = PunktSentenceTokenizer()
    text = sentence_tokenizer.tokenize(text)

    cleaned_text = []
    stop_words = set(stopwords.words('russian'))

    # разбиваем по словам, чистим от оставшейся пунктуации и stopwords
    tokenizer = WhitespaceTokenizer()
    stemmer = SnowballStemmer('russian')

    for sentence in text:
        punct_cleaned_sent = clear_endings(sentence)  # служ. символы конца предложения
        tokenized_sent = tokenizer.tokenize(punct_cleaned_sent)  # раскидали по словам, только для отчистки
        stpw_clean_sentence = [word for word in tokenized_sent if not word in stop_words]
        stemmed_sentence = [stemmer.stem(word) for word in stpw_clean_sentence]  # проеборазуем в ед. число или корень слова
        clean_sentence = ' '.join(stemmed_sentence)  # собрали обратно в предложение-сторку для хэшировнаия

        cleaned_text.append(clean_sentence)

    return cleaned_text