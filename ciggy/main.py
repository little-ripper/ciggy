import asyncio
import json
import tarfile
from ciggy.config import bookmarks_path
from ciggy.api.api import fetch_status
from bs4 import BeautifulSoup as bs
import pathlib
from ciggy.db import cur, conn, async_session_context


class CiggyAttrs:
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


class Ciggy:
    def __init__(self, tags: set = set(), file_name: str = str()):
        self.tags = tags
        self.file_name = file_name
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


class JsonNy:
    def __init__(self, js: dict = {}):
        self.js = js
        self.__create_(self.js)

    def __create_(self, js):
        if isinstance(js, dict):
            iterator = js.items()
        else:
            iterator = enumerate(js)

        for key, value in iterator:
            try:
                hash(value)
                setattr(self, key, value)
            except TypeError:
                setattr(self, key, [])
                attr = getattr(self, key)
                for v in value:
                    attr.append(JsonNy(v))

    def _display(self, attrs: dict, deep: str) -> str:
        output = f'{deep}JsonNy(\n'
        items = list(attrs.items())
        for i, (key, value) in enumerate(items):
            if isinstance(value, list):
                output += f'{deep}\t{key}: [\n'
                for j, val in enumerate(value):
                    output += self._display(val, deep + '\t\t')
                    if j < len(value) - 1:
                        output += ',\n'
                    else:
                        output += '\n'
                output += f'{deep}\t]\n'
            else:
                output += f'{deep}\t{key}: {value}'
                if i < len(items) - 1:
                    output += ','
                output += '\n'
        output += f'{deep})'
        return output

    def __str__(self):
        return self._display(self.js, '')

    def __repr__(self):
        return str(type(self))


def is_json(soup):
    try:
        return json.loads(soup.text)
    except json.decoder.JSONDecodeError:
        return


def _file_parsing(content, file_name: str = ''):
    """Given the file descriptor parse the page and extract the content.
    Mainly title and s tags
    """
    soup = bs(content, 'lxml')
    if data := is_json(soup):
        return JsonNy(data)
    else:
        tags = set([tag.name for tag in soup.find_all()])
        cg = Ciggy(file_name=file_name, tags=tags)
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


def parse_file(file) -> dict:
    with open(file, mode='r', encoding='utf-8') as f:
        file_name = str(file)
        content = f.read()
        return {
            'file_name': file,
            'data': _file_parsing(content, file_name)
        }


def parse_tarfile(file, path_to):
    with tarfile.open(file, "r") as tf:
        tf.extractall(path=path_to)


def parse_folder(path: pathlib.PosixPath, rec_th: int):
    results = []
    if rec_th < 0:
        return []
    for file in path.iterdir():
        try:
            results.append(parse_file(file))
        except UnicodeDecodeError:
            path_to = file.parent
            parse_tarfile(file, path_to)
        except IsADirectoryError:
            rec_th -= 1
            results += parse_folder(path=file, rec_th=rec_th)
    return results


async def main(urls):
    async with async_session_context() as session:
        results = await asyncio.gather(
            *(fetch_status(u) for u in urls)
        )
        for url, status in results:
            cur.execute("INSERT OR REPLACE INTO urls (url, status) VALUES (?, ?)", (url, status))
        conn.commit()

urls = [
    'https://imagemagick.org/script/display.php',
    'https://www.hyperbola.info/',
    'https://www.parabola.nu/'
]

asyncio.run(main(urls))
conn.close()


if __name__ == '__main__':
    data = parse_folder(bookmarks_path, 2)

# data = parse_folder(bookmarks_path, 2)
