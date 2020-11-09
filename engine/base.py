from abc import ABC
from .settings import THRESHOLD
from .preprocessing import TextPreprocessor

class DataAdapter:
    def convert(self, preprocessed_text, *args, **kwargs):
        #  преобразовнание текста в требуемый формат
        raise NotImplementedError 

    def calc_resemblance(self, text1, text2):
        #  вычисление величины совпадения.
        raise NotImplementedError 

    def is_matched(self, text1, text2):
        #  тест на совпадение с заданной точностью (settings.py)
        result = calc_resemblance(text1, text2) >= THRESHOLD
        return result


class TextModel:
    """
    Базовый класс  моделей представления текста
    """
   
    def __init__(self, text, text_preprocessor=TextPreprocessor(), data_adapter=TextPreprocessor()):
        self._orig_text = text
        self._text_preprocessor = text_preprocessor
        self._data_adapter = data_adapter
        text = self._text_preprocessor.process(text)
        #print(type(self._text_preprocessor))
        #print(f'inside TextModel init text = {text}')
        self._stored_text = self._data_adapter.convert(text)

    @property
    def orig_text(self):
        return self._orig_text

    @property
    def stored_text(self):
        return self._stored_text


class TextCorpus:
    """
    Корпус текстов (базовый класс)
   
    """
    def __init__(self, 
                text_model=TextModel, 
                text_preprocessor=TextPreprocessor(),
                data_adapter=DataAdapter()
                ):
        self._corpus = []
        self._text_model = text_model
        self._text_preprocessor = text_preprocessor
        self._data_adapter = data_adapter

    def _check_for_coincidence(self, text):
        """
        проверка на наличие совпадений по порогу

        Args:
            text : текст в виде сплошной строки

        Returns:
             None, если нет совпадений, список кортежей (оригинальный_текст_одной_строкой, %_совпадения)
        """
        matched_texts = []
        text = self._text_preprocessor.process(text)
        data = self._data_adapter.convert(text)
        
        for item in self._corpus:
            if self._data_adapter.is_matched(data, item.stored_text):
                #resemblance = self._data_adapter.calc_resemblance(data, item.stored_text())
                #matched_texts.append((item.orig_text(), resemblance))
                matched_texts.append((item.orig_text,))
        
        if len(matched_texts):
            return matched_texts
        else:
            return None

    def _store_text(self, text):
        text_model = self._text_model(text)
        self._corpus.append(text_model)

    def add_text(self, text):
        if len(text) == 0:
            raise Exception("Can't add empty text to the corpus")
        """
        Добавить текст в корпус

        Args:
            text ([type]): текст в тектовом формате

        Returns:
            [type]: если добавил, то None, иначе кортеж с оригинальными текстами, где найдено совпадение
        """
        check_result =  self._check_for_coincidence(text)
        if check_result is None:
            self._store_text(text)
            return None
        else:
            return check_result

    

