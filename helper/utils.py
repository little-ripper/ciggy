from pprint import pprint as pp


def infod(func):
    def wrapper(*args, **kwargs):
        results = func(*args)
        for result in results:
            try:
                string = f'{repr(result)} => {getattr(*args, result)}'
                pp(string)
            except:
                string = f'{repr(result)} => None'
                pp(string)
    return wrapper


@infod
def info(f):
    return dir(f)
