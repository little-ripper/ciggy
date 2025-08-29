from ciggy.config import bookmarks_path
from bs4 import BeautifulSoup as bs


class CiggyAttrs():
    def __init__(self, attrs: dict = dict(), text: str = str):
        self.attrs = attrs
        self.text = text
        self.__set_init_attrs()

    def __set_init_attrs(self):
        for attr, value in self.attrs.items():
            setattr(self, attr, value)

    def __repr__(self):
        output = 'CiggyAttrs(\n'
        for key in self.attrs.keys():
            output += f'\t{key}: {getattr(self, key)}\n'
        output += ')'
        return output


class Ciggy():
    def __init__(self, tags: set = set(), file_name: str = str()):
        self.tags = tags
        self.title = file_name
        self.__set_init_tags()

    def __set_init_tags(self):
        for tag in self.tags:
            setattr(self, tag, None)

    def set_tag_value(self, tag_str, value):
        setattr(self, tag_str, value)

    def __repr__(self):
        output = 'Ciggy('
        for tag in self.tags:
            output += f'{tag}, '
        output += ')'
        return output


def _file_parsing(content):
    """Given the file descriptor parse the page and extract the content.
    Mainly title and s tags
    """
    soup = bs(content, 'lxml')
    tags = set([tag.name for tag in soup.find_all()])
    cg = Ciggy(file_name="hello", tags=tags)
    for tag in tags:
        all_tags = soup.find_all(tag)
        if len(all_tags) == 1:
            try:
                cg.set_tag_value(tag, all_tags[0].text)
            except AttributeError:
                continue
        else:
            cg.set_tag_value(
                tag,
                [CiggyAttrs(at.attrs, at.text) for at in all_tags]
            )
    return cg


def main():
    results = []
    file_content = {}
    for file in bookmarks_path.iterdir():
        if file.is_file():
            try:
                with open(file, mode='r', encoding='utf-8') as f:
                    content = f.read()
                    file_content.update({
                        'file_name': str(file),
                        'data': _file_parsing(content)
                    })
                    results.append(file_content)
            except UnicodeDecodeError:
                continue
    return results


if __name__ == '__main__':
    data = main()

data = main()
