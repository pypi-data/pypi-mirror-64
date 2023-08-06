from pangeamt_nlp.processor.base.validator_base import ValidatorBase
from pangeamt_nlp.seg import Seg
import re


class NoLinesWithOnlyMail(ValidatorBase):
    NAME = "no_lines_with_only mail"

    DESCRIPTION_TRAINING = """
            Filter paris with only mail
        """

    DESCRIPTION_DECODING = """
            Validators do not apply to decoding.
        """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)


    def validate(self, seg: Seg) -> bool:
        mails = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", seg.src)

        if len(mails) > 0:
            only_mail = True
            for token in seg.src.split(" "):
                if token not in mails:
                    only_mail = False
                    break

            if only_mail and len(seg.src.split(" ")) == 1:
                return True
            return True
