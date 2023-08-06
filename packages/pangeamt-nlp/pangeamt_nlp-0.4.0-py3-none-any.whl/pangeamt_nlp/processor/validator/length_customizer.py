from pangeamt_nlp.processor.base.validator_base import ValidatorBase
from pangeamt_nlp.seg import Seg


class LengthCustomizer(ValidatorBase):
    NAME = "length_customizer"

    DESCRIPTION_TRAINING = """
        Remove pair of sentences with less tha a minimum and mora than a maximum length
    """

    DESCRIPTION_DECODING = """
        Validators do not apply to decoding.
    """

    def __init__(self, src_lang: str, tgt_lang: str, minimum: int, maximum:int) -> None:
        super().__init__(src_lang, tgt_lang)
        self._min = minimum
        self._max = maximum

    def validate(self, seg: Seg) -> None:
        if len(seg.tgt.split()) > self._max  or len(seg.tgt.split()) < self._min:
            return True
        return False
