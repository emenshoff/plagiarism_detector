import re
from abc import ABC
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
    return re.sub(r"[~`@«»#$%^&*()_—+=\-:№\"\[\]\\/|',\n]", '', text)


# чистим символы конца строки  !?.;.
def clear_endings(text):
    return re.sub(r"[!?.;]", '', text)


class TextPreprocessor(ABC):
    #  базовый класс, на будущее (если понадобятся другие методы предобработки)
    _processing_pipeline = None #  пока не заморачиваюсь, тоже закладка на будущее

    def process(self, data):
        raise NotImplementedError 


class TextPlainPreprocessor(TextPreprocessor):
    def process(self, text, plain_text=False):
        """
        предобработка, токенизация по словам,  удаление дублей.
        выдает сплошной (plain) текст, для метода шиндлов или список токенов текста

        Args:
            text ([type]): [description]
        """
        #text = text.encode('utf-8')

        # убираем числа, email, гиперрсылки
        
        text = clear_emails(text)
        text = clear_url(text)
        text = clear_digits(text)
        text = clear_symb(text)

    
        # разбиваем по словам, чистим от оставшейся пунктуации и stopwords

        stop_words = set(stopwords.words('russian'))
        tokenizer = WhitespaceTokenizer()
        stemmer = SnowballStemmer('russian')

        punct_cleaned_text = clear_endings(text)  # служ. символы конца предложения
        tokenized_text = tokenizer.tokenize(punct_cleaned_text)  # раскидали по словам, только для отчистки
        stpw_clean_text = [word for word in tokenized_text if not word in stop_words]
        stemmed_text = [stemmer.stem(word) for word in stpw_clean_text]  # проеборазуем в ед. число или корень слова
        clean_text = None
        if plain_text:
            clean_text = ' '.join(stemmed_text)  # собрали обратно в предложение-сторку для хэшировнаия
        else:
            clean_text = stemmed_text #  иначе возвращаем список токенов
 
        return clean_text


class TextSentencePreprocessor(TextPreprocessor):
        def process(self, text):
            """
            предобработка, токенизация по предложениям, удаление дублей.
            выдает список предложений (для векторного метода, на будущее)
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

