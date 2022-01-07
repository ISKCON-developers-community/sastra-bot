# Parser Vedabase
from bs4 import BeautifulSoup as bs
import bs4
import requests
import time


def __get_soup(url) -> bs4.BeautifulSoup:
    '''Returns soup from site page'''
    while True:  # повтор запроса к странице после ожидания, если сервер закрыает соединение
        try:
            r = requests.get(url)
        except requests.exceptions.RequestException:
            time.sleep(30)
        else:
            break
    r.encoding = 'utf-8'
    return bs(r.text, 'html.parser')


def __construct_link(query: str) -> dict:
    url_arr = ['https://vedabase.io']
    languages = ['en', 'nl', 'ru', 'da', 'et', 'sk', 'es', 'de', 'uk',
                 'lt', 'sl', 'fi', 'cs', 'hu', 'fr', 'ko', 'pt-br', 'bg', 'ja', 'zu']
    cc_books = ['adi', 'madhya', 'antya']
    books = ['bg', 'sb', 'cc']
    errors = []
    attrs = query.split()
    # check query attribs
    lang_code = attrs[0].lower()
    if lang_code not in languages:
        errors.append("Wrong language code.")
    else:
        url_arr.append(f'{lang_code}/library')
    if attrs[1].lower() not in books:
        errors.append("Wrong book code. Try one of 'bg', 'sb', 'cc'")
    else:
        if attrs[1].lower() == 'cc' and attrs[2].lower() not in cc_books:
            errors.append('Wrong volume code of CC')
        elif attrs[1].lower() == 'cc' and attrs[2].lower() in cc_books:
            try:
                chapter, verse = attrs[3].split('.')
                int(chapter)
                verses = verse.split('-')
                if len(verses) > 2 or (len(verses) == 2 and (not verses[0].isdigit() or not verses[1].isdigit())):
                    raise ValueError
            except ValueError:
                errors.append('Wrong chapter or verse of CC')
            else:
                url_arr.append(f'cc/{attrs[2].lower()}/{chapter}/{verse}')
        elif attrs[1].lower() == 'sb':
            try:
                volume, chapter, verse = attrs[2].split('.')
                int(volume)
                int(chapter)
                verses = verse.split('-')
                if len(verses) > 2 or (len(verses) == 2 and (not verses[0].isdigit() or not verses[1].isdigit())):
                    raise ValueError
            except ValueError:
                errors.append('Wrong SB verse')
            else:
                url_arr.append(f'sb/{volume}/{chapter}/{verse}')
        else:
            try:
                chapter, verse = attrs[2].split('.')
                int(chapter)
                verses = verse.split('-')
                if len(verses) > 2 or (len(verses) == 2 and (not verses[0].isdigit() or not verses[1].isdigit())):
                    raise ValueError
            except ValueError:
                errors.append(f'Wrong chapter or verse of {attrs[1]}')
            else:
                url_arr.append(
                    f'{attrs[1]}/{chapter}/{verse}')
    if errors:
        return {'errors': errors}
    else:
        return {'link': '/'.join(url_arr)}


def __formate_purport_paragraph(div):
    if 'r-verse-text' in div['class']:
        return div.get_text('\n', strip=True)
    else:
        return div.get_text()

# getting data


def get_full_verse(query: str) -> dict:
    parsed_query = __construct_link(query)
    if 'errors' in parsed_query:
        return {'errors': parsed_query['errors']}
    url = parsed_query['link']
    soup = __get_soup(url)
    title = soup.title.text
    if title == '':
        return {'errors': [f'Verse not found. Maybe this verse in the block of verses. Example: bg 1.16-18\nhttps://vedabase.io/en/library/bg/1/16-18/']}
    try:
        verse_text = soup.find(
            'div', class_='wrapper-verse-text').find_all(class_='r-verse-text')
        verse_text = '\n\n'.join([v.get_text('\n', strip=True)
                                  for v in verse_text])
        word_by_word = soup.find(class_='r-synonyms').get_text()
        translation = soup.find(class_='r-translation').get_text()
        purport_block = soup.find('div', class_='wrapper-puport')
    except Exception:
        return {'errors': ['Page not found']}

    if purport_block:
        purport_text = '\n\n'.join([__formate_purport_paragraph(
            div) for div in purport_block.find_all('div')])
    else:
        purport_text = ''
    return {
        'link': url,
        'title': title,
        'verse': verse_text,
        'word-by-word': word_by_word,
        'translation': translation,
        'purport-text': purport_text
    }
