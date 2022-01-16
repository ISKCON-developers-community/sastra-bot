# Parser Vedabase
from bs4 import BeautifulSoup as bs
import bs4
import requests
import time
from memory import memory


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


def __formate_verse_number(query_arr: list, attr_num: int, digits: int):
    try:
        attrs = query_arr[attr_num].split('.')
    except IndexError:
        return False
    if len(attrs) != digits:
        return False
    for i in range(len(attrs) - 1):
        if not attrs[i].isdigit():
            return False
    verses = attrs[-1].split('-')
    if len(verses) > 2 or (len(verses) == 1 and not verses[0].isdigit()):
        return False
    if len(verses) == 2 and (not verses[0].isdigit() or not verses[1].isdigit()):
        return False

    return '/'.join(attrs)


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
        try:
            cc_volume = attrs[2].lower()
        except IndexError:
            cc_volume = 'error'
        if attrs[1].lower() == 'cc' and cc_volume not in cc_books:
            errors.append('Wrong volume code of CC')
        elif attrs[1].lower() == 'cc' and attrs[2].lower() in cc_books:
            verse_link = __formate_verse_number(attrs, 3, 2)
            if verse_link:
                url_arr.append(f'cc/{attrs[2].lower()}/{verse_link}')
            else:
                errors.append('Wrong chapter or verse of CC (Example: 5.25)')

        elif attrs[1].lower() == 'sb':
            verse_link = __formate_verse_number(attrs, 2, 3)
            if verse_link:
                url_arr.append(f'sb/{verse_link}')
            else:
                errors.append('Wrong chapter or verse of SB (Example: 1.5.25)')
        else:
            verse_link = __formate_verse_number(attrs, 2, 2)
            if verse_link:
                url_arr.append(f'bg/{verse_link}')
            else:
                errors.append('Wrong chapter or verse of BG (Example: 5.25)')
    if errors:
        return {'errors': errors}
    else:
        return {'link': '/'.join(url_arr), 'attrs': attrs}


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
        purport_text = title + ' Purport\n\n' + '\n\n'.join([__formate_purport_paragraph(
            div) for div in purport_block.find_all('div')])
        purport_id = '_'.join(parsed_query['attrs']).replace('.', '_')
        memory.set(purport_id, purport_text, ex=600)
    else:
        purport_id = ''

    return {
        'link': url,
        'title': title,
        'verse': verse_text,
        'word-by-word': word_by_word,
        'translation': translation,
        'purport_id': purport_id
    }
