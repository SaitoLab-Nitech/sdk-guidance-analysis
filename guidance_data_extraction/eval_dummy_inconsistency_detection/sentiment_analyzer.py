import re
import emoji
import unicodedata
from transformers import pipeline, RobertaForSequenceClassification, RobertaTokenizer

class SentimentAnalyzer():

    def __init__(self, path_to_model):
        self.analyzer = pipeline(
            task="sentiment-analysis",
            model=RobertaForSequenceClassification.from_pretrained(path_to_model),
            tokenizer=RobertaTokenizer.from_pretrained("siebert/sentiment-roberta-large-english")
        )

    def analyze(self, original_value):
        final_result = None
        final_text = None

        value_without_url = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "", original_value)
        processed_value = ''
        for c in value_without_url:
            if (emoji.is_emoji(c)):
                c = emoji.demojize(c, delimiters=('', '')).replace('_', ' ')
                # print(c)
            elif (unicodedata.east_asian_width(c) != 'Na'):
                c = ' '
            elif (c == '*'):
                c = ' '
            processed_value += c
        for text in processed_value.split('. '):
            text = text.strip()
            text = text.capitalize()
            if (not text.endswith('.')): text += '.'
            # print(f'{text = }')
            result = self.analyzer(text)
            if (final_result is None or result[0]['label'] == 'POSITIVE'):
                final_result = result
                final_text = text

        return final_result, final_text
