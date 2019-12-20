from docx import Document


# Класс парсера docx файла, хранящего в себе набор слов для серсива Lingualeo
class lingua_docx_parser:
    # Конструктор парсера от пути к файлу
    def __init__(self, file_name):
        self.docx_document = Document(file_name)


    # Функция печати содержимого docx файла в консоль
    def print_file(self):
        for paragraph in self.docx_document.paragraphs:
            print(paragraph.text)


    # Функция, создающая список слов из docx файла вместе с переводами и транскрипцией
    def create_words_set(self):
        words_set, dublicates = [], []
        for paragraph in self.docx_document.paragraphs:
            words_set_elem_parts = paragraph.text.split('—')
            words_set_elem = dict.fromkeys(["word", "transcription", "translation"])
            if words_set_elem_parts[0]:
                if len(words_set_elem_parts) == 3:
                    words_set_elem["word"] = words_set_elem_parts[0].strip()
                    words_set_elem["transcription"] = words_set_elem_parts[1].strip()
                    words_set_elem["translation"] = words_set_elem_parts[2].strip()
                elif len(words_set_elem_parts) == 2:
                    words_set_elem["word"] = words_set_elem_parts[0].strip()
                    words_set_elem["translation"] = words_set_elem_parts[1].strip()
                else:
                    words_set_elem["word"] = words_set_elem_parts[0].strip()
                already_exists = False
                for elem in words_set:
                    if elem["word"] == words_set_elem["word"]:
                        already_exists = True
                        dublicates.append(words_set_elem)
                        break
                if not already_exists:
                    words_set.append(words_set_elem)
        for dublicated_elem in dublicates:
            if dublicated_elem["translation"] is None:
                continue
            for words_set_elem in words_set:
                if dublicated_elem["word"] == words_set_elem["word"]:
                    if words_set_elem["translation"] is None:
                        words_set_elem["translation"] = dublicated_elem["translation"]
                    elif dublicated_elem["translation"] != words_set_elem["translation"] and \
                            words_set_elem["translation"].find(dublicated_elem["translation"]) == -1:
                        words_set_elem["translation"] += '; ' + dublicated_elem["translation"] 
        return words_set

