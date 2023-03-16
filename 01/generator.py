def generator_text(file_name, list_words):
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")
    if not isinstance(list_words, list):
        raise TypeError("list_words must be a list")
    try:
        with open(file_name, encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                words_in_line = line.split()
                list_words = [word.lower() for word in list_words]
                for word in words_in_line:
                    if word.lower() in list_words:
                        yield line
                        break
    except FileNotFoundError as err:
        raise FileNotFoundError("Такого файла не существует") from err
