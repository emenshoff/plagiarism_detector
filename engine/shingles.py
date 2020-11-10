import random
import hashlib
from .preprocessing import TextPlainPreprocessor
from .base import TextModel, TextCorpus, DataAdapter

from .settings import SHINGLES_METHOD_THRESHOLD

SHINGLE_LEN = 10  # полагаю, можно ускорить и снизить расходы на память, если поиграться со значением "окна"
SHINGLE_PADDING = 2 # отступ окна перекрытия при генерации шингла


class ShingleDataAdapter(DataAdapter):
    """
    логика и операции с шинглами
    
    Returns:
        [type]: [description]
    """

    def convert(self, text, hash_fn=hashlib.md5):
        # генерация шинглов с настраиваемым сдвигом, на входе токенизированный текст (список строк)
        shingles = []
        #text = text.encode('utf-8')
        txt_len = len(text)
        if txt_len > SHINGLE_LEN + SHINGLE_PADDING:
            for x in range(0, len(text) - SHINGLE_LEN + SHINGLE_PADDING, SHINGLE_PADDING):
                shingle_text = ' '.join(text[x : x + SHINGLE_LEN ]) #  текст шингла
                shingle_hashed = hash_fn(shingle_text.encode('utf-8')).digest() #  хэш шингла               
                shingles.append(shingle_hashed)
        else:
            shingle_text = ' '.join(text)
            shingle_hashed = hash_fn(shingle_text.encode('utf-8')).digest()         
            shingles.append(shingle_hashed)
 
        return shingles

    def calc_resemblance(self, text1, text2): # сравниваю множества 
        #  На входе предполагаются шинглы
        text1_set = set(text1)
        text2_set = set(text2)
        overlap = text1_set & text2_set

        conicedence = 2.0 * len(overlap) / (len(text1_set) + len(text2_set))

        return conicedence
        
    def is_matched(self, text1, text2):
        #  плагиат или нет. возвращает tuple, первый индекс - диагноз, по второму - оригинальный текст
        result = self.calc_resemblance(text1, text2) >= SHINGLES_METHOD_THRESHOLD
        return result
        

class ShingledText(TextModel):
    
    def __init__(self, text):        
        super().__init__(text, 
                        text_preprocessor=TextPlainPreprocessor(), 
                        data_adapter=ShingleDataAdapter()
                        )
    

class ShingledTextCorpus (TextCorpus):
    
    def __init__(self):
        super().__init__(
                        text_model=ShingledText, 
                        text_preprocessor=TextPlainPreprocessor(),
                        data_adapter=ShingleDataAdapter()
                        )
         
    
