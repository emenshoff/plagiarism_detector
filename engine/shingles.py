import random
import hashlib
from .preprocessing import preprocess_text

from .settings import THRESHOLD

SHINGLE_LEN = 5  # полагаю, можно ускорить и снизить расходы на память, если поиграться со значением "окна"
SHINGLE_PADDING = 1 # отступ окна перекрытия при генерации шингла


# def dice_coef(y_true, y_pred, smooth=1):
#     y_true_f = K.flatten(y_true)
#     y_pred_f = K.flatten(y_pred)
#     intersection = K.sum(y_true_f * y_pred_f)
#     return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


class Shingler:
    def text_to_shingles(self, text):
        # геренация шинглов с настраиваемым сдвигом
        shingles = []
        txt_len = len(text)
        if txt_len > SHINGLE_LEN + SHINGLE_PADDING:
            for x in range(len(text) - (SHINGLE_LEN + SHINGLE_PADDING - 1)):
                shingles.append(self.hash_fn(word) for word in text[x : x + SHINGLE_PADDING + SHINGLE_LEN ])
        else:
            shingles.append(self.hash_fn(text))

        return shingles

    def __init__(self, 
                text, 
                by_sentence=True, 
                preprocess_fn=preprocess_text, 
                hash_fn=hashlib.md5):
        self.by_sentence = by_sentence # хэшим по предложениям или превращаем в сплошной текст
        self.hash_fn = hash_fn
        self.preprocess_fn = preprocess_fn
        self._orig_text = text # сохраняем оригинал
        self._shingled_text = []
        if preprocess_fn:
            text  = preprocess_fn(text)  
        if self.by_sentence:
            for sentence in text:
                self._shingled_text.append(text_to_shingles(sentence))
        else:
            self._shingled_text = text_to_shingles(text)

        #self._shingled_text = set(self._shingled_text)

    def calc_resemblance(self, text): # сравниваю множества по dice coeff.
        shingled_text = []
      
        text = self.preprocess_fn(text)

        if self.by_sentence:
            for sentence in text:
                shingled_text.append(text_to_shingles(sentence))
        else:
            shingled_text = text_to_shingles(text)

        tested_text_set = set(shingled_text)
        original_text_set = set(self._shingled_text)
        overlap = tested_text_set & original_text_set

        conicedence = 2.0 * len(overlap) / (len(original_text_set) + len(tested_text_set))

        return conicedence
        
        # return dice_coef(original_text_set, tested_text_set) # оставим для векторов
      
    def is_plagiarism(self, text, get_origin=False):
        #  плагиат или нет. возвращает tuple, первый индекс - диагноз, по второму - оригинальный текст
        result = self.calc_resemblance(text) >= THRESHOLD
        if get_origin:
            return (result, self._orig_text)
        return (result,)








