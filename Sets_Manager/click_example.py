import click
from docx import Document

from api import get_wordset
from docx_helpers import save_to_file


@click.group()
def cli():
    pass


@click.command(help='Импорт файла в словарь Lingualeo')
@click.option('--wordset', default='Мой словарь', prompt='Название словаря для импорта',
              help='Название словаря для импорта')
@click.option('--filename', default="Мой словарь", prompt='Имя файла для импорта', help='Имя файла для импорта')
def imp(wordset, filename):
    full_filename = '%s.docx' % filename
    document = Document(full_filename)

    for table in document.tables:
        print('Название словаря при импорте:', wordset)
        for row in table.rows:
            word = row.cells[0].text
            transcription = row.cells[1].text
            translation = row.cells[2].text
            print(word, '\n\t[', transcription, '] - ', translation, '\n')


@click.command(help='Экспорт словарь Lingualeo в файл docx')
@click.option('--wordset', default='Мой словарь', help='Название словаря Lingualeo для экспорта')
@click.option('--filename', default="Мой словарь", prompt='Имя файла для экспорта', help='Имя файла для экспорта')
@click.option('--many', default="Нет", prompt='Выводить несколько значений перевода', help='Имя файла для экспорта')
def exp(wordset, filename, many):
    many_translations = many.lower() == 'да'
    words = get_wordset(wordset)
    save_to_file(wordset, words, filename, many_translations)


cli.add_command(imp)
cli.add_command(exp)

if __name__ == '__main__':
    cli()
