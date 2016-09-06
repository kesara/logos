import io
import random
import re

import aalib
import PIL.Image
import requests
import wikipedia

LOGO_REGEX = re.compile('.*logo.*', re.I)
WIKIPEDIA_URL = 'https://en.wikipedia.org/wiki/'
WIKIPEDIA_MAIN_PAGE = 'List of free and open-source software packages'
SCREEN_HEIGHT = 40
SCREEN_WIDTH = 80

software_list = []


def getLogo(software_list):
    entry = random.sample(software_list, 1)[0]
    software_list.remove(entry)
    if (len(entry.split(' ')) > 2):
        return getLogo(software_list)
    try:
        info = wikipedia.page(entry)
    except Exception as e:
        print(e)
        return getLogo(software_list)
    images = info.images
    logo = None
    if not images:
        return getLogo(software_list)
    else:
        logo = findLogo(entry, images)
    if logo:
        return {
            'entry': entry,
            'url': ''.join([WIKIPEDIA_URL, entry.replace(' ', '_')]),
            'summary': info.summary,
            'logo': logo}
    else:
        return getLogo(software_list)


def doubleCheck(entry, image):
    words = entry.lower().split(' ')
    for word in words:
        if word in image.lower():
            return True
    return False


def findLogo(entry, images):
    for image in images:
        if LOGO_REGEX.match(image) and doubleCheck(entry, image):
            return image
    return None


def printLogo(logo_url):
    screen = aalib.AsciiScreen(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    logo = io.BytesIO(requests.get(logo_url).content)
    image = PIL.Image.open(logo).convert('L').resize(screen.virtual_size)
    screen.put_image((0, 0), image)
    print(screen.render())


def game():
    print('Generating software list from Wikipedia...')
    software_list = wikipedia.page(WIKIPEDIA_MAIN_PAGE).links
    entries = 0
    wins = 0
    while True:
        try:
            print('Searching Wikipedia...')
            entry = getLogo(software_list)
            printLogo(entry['logo'])
            entries += 1
            guess = input('Guess the logo (quit for exit): ')
            if str(guess).lower() == 'quit':
                break
            if str(guess).lower() in entry['entry'].lower().split(' '):
                wins += 1
                print('Correct!')
            else:
                print('Wrong!')
            print('{name} ({url})\n{summary}\n'.format(
                name=entry['entry'],
                url=entry['url'],
                summary=entry['summary']))
        except:
            pass
    print('{wins} wins out of {entries}'.format(wins=wins, entries=entries))


if __name__ == '__main__':
    game()
