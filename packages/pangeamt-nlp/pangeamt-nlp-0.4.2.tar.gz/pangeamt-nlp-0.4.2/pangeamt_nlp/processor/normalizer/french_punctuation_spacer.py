import sys

from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.processor.normalizer.quotenormalizer import QuotesInfo
from pangeamt_nlp.seg import Seg
import unicodedata

# Source for rules followed
class FrenchPunctuationSpacer(NormalizerBase):
    """To be applied after quotation character normalisation
    Adds a non-breaking space before each "?" , "!", ":" and ";"
    Adds a normal space before the opening bracket ( and the standard quotation marks as defined in
    quotenormalizer.QuotesInfo
    """

    NAME = "french_punctuation_spacer"

    DESCRIPTION_TRAINING = """
        Applies the french punctuation spacer to src or tgt, checking
        with the src_lang and tgt_lang to decide where to apply it.        
    """
    DESCRIPTION_DECODING = """
        Apply the french punctuation spacer to src or tgt, checking
        with the src_lang and tgt_lang to decide where to apply it
    """

    def __init__(self, src_lang: str, tgt_lang: str):
        # Source:  http://grammaire.reverso.net/5_1_10_les_espaces_et_la_ponctuation.shtml
        # Addition (from Cath): before the ending quotes and after the opening quotes: non-breaking space
        super().__init__(src_lang, tgt_lang)
        self.nb_space = "\u00A0" #non-breaking space
        self.all_spaces = self._get_unicode_space_characters()
        self.punct_with_pre_np_space = ["?", "!", ":", ";"]
        self.punct_with_pre_np_space.extend(QuotesInfo.get_standard_close_quotes_for_language("fr"))

        self.punct_with_pre_space = QuotesInfo.get_standard_open_quotes_for_language("fr")
        self.punct_with_pre_space.append("(")

        self.punct_with_post_space = QuotesInfo.get_standard_close_quotes_for_language("fr")
        self.punct_with_post_space.append(")")

        self.punct_with_post_np_space = QuotesInfo.get_standard_open_quotes_for_language("fr")


    @classmethod
    def _get_unicode_space_characters(cls):
        """ Returns all unicode characters in the "seperator, space" category (Zs)"""
        # Based on https://stackoverflow.com/questions/14245053/how-can-i-get-all-whitespaces-in-utf-8-in-python
        spaces = []
        for i in range(sys.maxunicode + 1):
            if unicodedata.category(chr(i)) == 'Zs':
                spaces.append(chr(i))
        return spaces

    def _normalize(self, text):

        res = []
        i = 0
        while i < len(text):
            if text[i] in self.punct_with_pre_np_space:
                if i > 0 and text[i-1] in self.all_spaces: #space found
                    res[-1] = self.nb_space
                else:
                    res.append(self.nb_space)
            elif text[i] in self.punct_with_pre_space:
                if i > 0 and text[i-1] in self.all_spaces: #space found
                    res[-1] = " "
                else:
                    res.append(" ")
            res.append(text[i])
            if text[i] in self.punct_with_post_space:
                res.append(" ")
                if i < len(text)+1 and text[i+1] in self.all_spaces: #space found
                    i += 1 #Skip the space character
            elif text[i] in self.punct_with_post_np_space:
                res.append(self.nb_space)
                if i < len(text)+1 and text[i+1] in self.all_spaces: #space found
                    i += 1 #Skip the space character
            i += 1

        return "".join(res)

    # Called when training
    def process_train(self, seg: Seg) -> None:
        if self.get_src_lang() == "fr":
            seg.src = self._normalize(seg.src)
        if seg.tgt is not None and self.get_tgt_lang() == "fr":
            seg.tgt = self._normalize(seg.tgt)

    # Called when using model (before calling model to translate)
    def process_src_decoding(self, seg: Seg) -> None:
        if self.get_src_lang() == "fr":
            seg.src = self._normalize(seg.src)

    # Called after the model translated (in case this would be necessary; usually not the case)
    def process_tgt_decoding(self, seg: Seg) -> None:
        pass
