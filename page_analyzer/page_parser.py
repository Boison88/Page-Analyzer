from bs4 import BeautifulSoup

TAGS = (
    ('h1', ''),
    ('title', ''),
    ('meta', {'name': 'description'}),
)


def get_page_data(page_content):
    page_data = {}
    soup = BeautifulSoup(page_content, 'lxml')
    for tag, attribute in TAGS:
        found_data = soup.find(tag, attribute)
        if found_data:
            page_data[tag] = found_data.get_text() or found_data.get('content')

    return page_data
