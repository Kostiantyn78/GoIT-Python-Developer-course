def main():

    import shutil
    import os
    import pathlib
    import re
    import sys

    #create a table for transliteration of Russian characters

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}

    for letter_cyr, letter_trans in zip(CYRILLIC_SYMBOLS, TRANSLATION):

        TRANS[ord(letter_cyr)] = letter_trans
        TRANS[ord(letter_cyr.upper())] = letter_trans.upper()

    path_to_sort_foulder = r'C:\Users\BigPC\Desktop\Мотлох'
    # path = r'C:\Users\BigPC\Desktop\Мотлох'

    # path_to_sort_foulder = fr'c:\Users{sys.argv[1]}'
    # path = fr'c:\Users{sys.argv[1]}'

    dest_dirs = ['images', 'video', 'audio', 'documents', 'archives']
    work_extension = {'images': ('.JPEG', '.PNG', '.JPG', '.SVG'),
                      'video': ('.AVI', '.MP4', '.MOV', '.MKV'),
                      'audio': ('.MP3', '.OGG', '.WAV', '.AMR'),
                      'documents': ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'),
                      'archives': ('.ZIP', '.GZ', '.TAR')}
    sorted_files = {}
    found_extension = set()
    unknown_extension = set()

    def sort_files(path):

        for path_element in pathlib.Path(path).iterdir():
            if path_element.is_dir() and path_element.name not in dest_dirs:
                sort_files(path_element)
                if not any(path_element.iterdir()):
                    pathlib.Path(path_element).chmod(0o777)
                    pathlib.Path(path_element).rmdir()

            elif path_element.suffix.upper() in work_extension['video']:
                try:
                    shutil.move(path_element, r'C:\Users\BigPC\Desktop\Мотлох\video')
                    found_extension.add(path_element.suffix)
                    sorted_files.setdefault('video', []).append(path_element.name)
                except shutil.Error as error:
                    print(f"File move error: {error}")

            elif path_element.suffix.upper() in work_extension['images']:
                try:
                    shutil.move(path_element, r'C:\Users\BigPC\Desktop\Мотлох\images')
                    found_extension.add(path_element.suffix)
                    sorted_files.setdefault('images', []).append(path_element.name)
                except shutil.Error as error:
                    print(f"File move error: {error}")

            elif path_element.suffix.upper() in work_extension['audio']:
                try:
                    shutil.move(path_element, r'C:\Users\BigPC\Desktop\Мотлох\audio')
                    found_extension.add(path_element.suffix)
                    sorted_files.setdefault('audio', []).append(path_element.name)
                except shutil.Error as error:
                    print(f"File move error: {error}")

            elif path_element.suffix.upper() in work_extension['documents']:
                try:
                    shutil.move(path_element, r'C:\Users\BigPC\Desktop\Мотлох\documents')
                    found_extension.add(path_element.suffix)
                    sorted_files.setdefault('documents', []).append(path_element.name)
                except shutil.Error as error:
                    print(f"File move error: {error}")

            elif path_element.suffix.upper() in work_extension['archives']:
                try:
                    shutil.unpack_archive(path_element, fr'{path_to_sort_foulder}\archives\{path_element.stem}')
                    pathlib.Path(path_element).unlink()
                    found_extension.add(path_element.suffix)
                    sorted_files.setdefault('archives', []).append(path_element.name)
                except shutil.Error as error:
                    print(f"File move / unpack error: {error}")

            else:
                path_element.suffix != '' and unknown_extension.add(path_element.suffix)


    def normalize(name):

        name = name.translate(TRANS)
        res = re.sub(r'\W', '_', name)

        return res

    # normalizing folder and file names
    def name_normalize(path):

        for path_element in pathlib.Path(path).iterdir():
            if path_element.is_dir() and path_element.name in dest_dirs:
                continue
            elif path_element.is_dir():
                name_normalize(path_element)
                pathlib.Path(path_element).rename(rf'{path_element.parent}\{normalize(path_element.name)}')
            else:
                if path_element.suffix.upper() == '.GZ': # "crutch" for GZ archives with "double" extension
                    pathlib.Path(path_element).rename(rf'{path_element.parent}\{path_element.stem[:-4]}.{path_element.stem[-3:]}{path_element.suffix}')
                else:
                    pathlib.Path(path_element).rename(rf'{path_element.parent}\{normalize(path_element.stem)}{path_element.suffix}')

    def output_sort_information():

        if sorted_files:
            print(f'The script sorted the files: {sorted_files}')
            print(f'The script sorted the files with extensions: {found_extension}')
        if unknown_extension:
            print(f'The script did not sort files with unknown extensions: {unknown_extension}')


    # check if there are folders 'images', 'video', 'audio', 'documents', 'archives'
    # in the folder to be sorted. If these folders are missing, they are created
    for folder in dest_dirs:
        if not pathlib.Path(fr'{path_to_sort_foulder}\{folder}').exists():
            pathlib.Path(fr'{path_to_sort_foulder}\{folder}').mkdir()

    name_normalize(path_to_sort_foulder)
    sort_files(path_to_sort_foulder)
    output_sort_information()

if __name__ == '__main__':
    main()

