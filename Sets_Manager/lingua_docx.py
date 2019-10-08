from docx import Document
import re


class lingua_docx_parser:
    def __init__(self, file_name):
        self.docx_document = Document(file_name)


    def print_file(self):
        for paragraph in self.docx_document.paragraphs:
            print(paragraph.text)


    def create_words_set(self):
        words_set = []
        for paragraph in self.docx_document.paragraphs:
            words_set_elem_parts = paragraph.text.split(u' \u2014 ')
            words_set_elem = dict.fromkeys(["word", "transcription", "translation"])
            if words_set_elem_parts[0] is not u'':
                words_set_elem["word"] = words_set_elem_parts[0]
                if len(words_set_elem_parts) == 3:
                    words_set_elem["transcription"] = words_set_elem_parts[1]
                    words_set_elem["translation"] = words_set_elem_parts[2]
                elif len(words_set_elem_parts) == 2:
                    if re.search(r'\[*\]', words_set_elem_parts[1]) is not None:
                        words_set_elem["transcription"] = words_set_elem_parts[1]
                    else:
                        words_set_elem["translation"] = words_set_elem_parts[1]
                words_set.append(words_set_elem)
        return words_set

    
