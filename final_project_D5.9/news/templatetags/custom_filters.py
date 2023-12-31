from django import template


register = template.Library()

BED_WORDS = [
    'редиска',
    'какашка',
]

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Фильтр только для строк')

    words = value.split()
    for i, word in enumerate(words):
        if word.lower() in BED_WORDS:
            words[i] = '*' * len(word)
    return ' '.join(words)