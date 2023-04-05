import io


def generator_text(file, list_words):
    if not isinstance(file, (io.IOBase, str)):
        raise TypeError("file должен быть строкой или файловым объектом")
    if not isinstance(list_words, list):
        raise TypeError("list_words must be a list")
    if isinstance(file, str):
        try:
            file = open(file, encoding='utf-8')
        except FileNotFoundError as err:
            raise FileNotFoundError("Такого файла не существует") from err
    try:
        list_words = [word.lower() for word in list_words]
        for line in file:
            line = line.strip()
            words_in_line = line.split()
            for word in words_in_line:
                if word.lower() in list_words:
                    yield line
                    break
    finally:
        file.close()
