from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging


def grabs_folder(path: Path):
    for el in path.iterdir():

        if el.is_dir():
            th = Thread(target=grabs_folder, args=(el,))
            th.start()
            threads.append(th)
            folders.append(el)


def sort_file(path: Path):
    for el in path.iterdir():

        if el.is_file():
            ext = el.suffix
            new_path = target_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as e:
                logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    folders = []
    threads = []

    base_folder = Path(r'C:\Users\BigPC\PycharmProjects\GoIT Education\Web block\homework-03\file_sort\мотлох')
    target_folder = Path(r'C:\Users\BigPC\PycharmProjects\GoIT Education\Web block\homework-03\file_sort\sorted')

    folders.append(base_folder)
    grabs_folder(base_folder)

    [th.join() for th in threads]

    threads = []

    for folder in folders:
        th = Thread(target=sort_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print('Files sorted')
