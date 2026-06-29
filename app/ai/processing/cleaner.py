import re


class TextCleaner:
    """
    Cleans extracted PDF text.
    """



    def clean(
        self,
        text: str
    ) -> str:


        text = re.sub(
            r"\s+",
            " ",
            text
        )


        text = text.strip()


        return text