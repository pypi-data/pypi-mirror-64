from pangeamt_nlp.processor.base.validator_base import ValidatorBase
from pangeamt_nlp.seg import Seg


class LengthFactor(ValidatorBase):
    NAME = "length_customier"

    DESCRIPTION_TRAINING = """
            Remove pair if length factor is high between src and tgt
        """

    DESCRIPTION_DECODING = """
            Validators do not apply to decoding.
        """

    def __init__(self, src_lang: str, tgt_lang: str, length_factor: int) -> None:
        super().__init__(src_lang, tgt_lang)
        self._length_factor = length_factor

    def validate(self, seg: Seg) -> bool:
        if len(seg.src) > len(seg.tgt) * self._length_factor or len(seg.tgt) > len(seg.src) * self._length_factor:
            return True
        return False
