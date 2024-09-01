russian_help = """
Телеграм бот может присылать текст и комментарий из книг Щрилы Прабхупады.
Для получения текста необходимо ввести сообветствующий запрос
1. Запрос обязательно должен начинаться со слова *verse*
2. Следующим словом необходимо указать язык, на котором вы хотите получить текст стиха. 
Список доступных языков:
'en' - англ., 'nl', 'ru' - русский, 'da', 'et', 'sk', 'es', 'de', 'uk' - украинский, 'lt', 'sl', 'fi', 'cs', 'hu', 'fr', 'ko', 'pt-br', 'bg', 'ja', 'zu'
3. Затем нужно указать книгу, из которой требуется получить текст. Вданным момент доступны книги:
BG - Бхагавад-гита. Как она есть
SB - Шримад Бхагаватам
CC - Чайтанья Чаритамрита (Adi, Madhya, Antya)

4. Затем нужно указать номер стиха (2.13, 3.25.25)


Примеры:
Бхагават-гита на украинском - Verse uk bg 2.13
Бхагаватам на русском - Verse ru sb 3.13.12
Чайтанья Чаритамрита на английском - Verse en CC Adi 8.17

Регистр букв не имеет значиния
"""


english_help = """
Telegram bot can send text and purport from books of Śrīla Prabhupāda.
To receive the text you need to enter the following request
1. The query must begin with the word *verse*.
2. The next word should be the language in which you want to receive the text of the verse. 
The list of available languages:
'en' - English, 'nl', 'ru' - Russian, 'da', 'et', 'sk', 'es', 'de', 'uk' - Ukrainian, 'lt', 'sl', 'fi', 'cs', 'hu', 'fr', 'ko', 'pt-br', 'bg', 'ja', 'zu'
3. Then you need to specify the book from which you want to retrieve the text. The books available at the moment are:
BG - Bhagavad-gita. As it is
SB - Srimad Bhagavatam.
CC - Chaitanya Charitamrita (Adi, Madhya, Antya).

4. Then you have to give the verse number (2.13, 3.25.25)


Examples:
Bhhagavat-gita in Ukrainian - Verse uk bg 2.13
Bhagavatam in Russian - Verse ru sb 3.13.12
Chaitanya Charitamrita in English - Verse en CC Adi 8.17
"""


def get_help(language:str) -> str:
    if language in ['ru', 'uk', 'be']:
        return russian_help
    return english_help

