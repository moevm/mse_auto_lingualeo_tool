from docx import Document
import re


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
        words_set = []
        for paragraph in self.docx_document.paragraphs:
            words_set_elem_parts = paragraph.text.split('-')
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
                words_set.append(words_set_elem)
        return words_set

    
