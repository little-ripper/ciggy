from ciggy.config import bookmarks_path
from bs4 import BeautifulSoup as bs


def _file_parsing(content):
    """Given the file descriptor parse the page and extract the content.
    Mainly title and s tags
    """
    results = {}
    atext = []
    aattrs = []
    soup = bs(content, 'lxml')
    tags = set([tag.name for tag in soup.find_all()])
    for tag in tags:
        if tag == 'title' or tag == 'h1':
            results[tag] = soup.find(tag).text
        if tag == 'a':
            results[tag] = {}
            for a_tag in soup.find_all(tag):
                atext.append(a_tag.text)
                aattrs.append(a_tag.attrs)
            results[tag].update({
                'text': atext,
                'attrs': aattrs
            })
    return results


def main():
    results = []
    file_content = {}
    for file in bookmarks_path.iterdir():
        if file.is_file():
            try:
                with open(file, mode='r', encoding='utf-8') as f:
                    content = f.read()
                    file_content.update({
                        'file_name': file,
                        'data': _file_parsing(content)
                    })
                    results.append(file_content)
            except UnicodeDecodeError:
                continue
    return results


if __name__ == '__main__':
    data = main()
