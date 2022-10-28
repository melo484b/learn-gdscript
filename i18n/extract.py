import csv
import os
import re

from itertools import chain
from pathlib import Path
from typing import List

from babel.messages.extract import extract, extract_from_dir
from babel.messages import Catalog
from babel.messages import pofile


PROJECT = 'Learn GDScript From Zero'
VERSION = ' '
COPYRIGHT_HOLDER = 'GDQuest'
BUGS_ADDRESS = 'https://github.com/GDQuest/learn-gdscript/issues'
SCRIPT_DIR = Path(__file__).parent

GDSCRIPT_PATTERN = r'''(?:(#)\s*(.*)|(tr)\(['"](.*)['"]\))'''


def log_extraction_file(filename, method, options):
    print(f'  Extracting {filename}')


def extract_gdscript(fileobj, keywords, comment_tags, options):
    for message_lineno, line in enumerate(fileobj, 1):
        result = [g for m in re.finditer(GDSCRIPT_PATTERN, line.decode().strip()) for g in m.groups() if g is not None]
        if len(result) == 2 and result[1] != '':
            yield (message_lineno, result[0], [result[1]], [])


def extract_godot_scene(fileobj, keywords, comment_tags, options):
    print(fileobj, keywords, comment_tags, options)
    # yield (0, None, 'message', 'comments')
    return []


def extract_and_write_application():
    print('Reading application messages...')
    method_map = [
        ('resources/**/**.gd', extract_gdscript),
        ('ui/**/**.gd', extract_gdscript),
        # ('ui/**/**.tscn', extract_godot_scene),
    ]
    keywords = {
        # Properties stored in scenes.
        'Label/text': None,
        'Button/text': None,
        'RichTextLabel/bbcode_text': None,
        'LineEdit/placeholder_text': None,
        'title': None,
        # Code-based translated strings
        '#': None,
        'tr': None,
    }
    extract_and_write(method_map, keywords, SCRIPT_DIR / 'application.pot')


# def extract_course_messages() -> None:
#     lessons_directory = './course'
#     for filename in os.listdir(lessons_directory):
#         full_path = os.path.join(lessons_directory, filename)
#         if filename.startswith('lesson-') and os.path.isdir(full_path):
#             extract_lesson_messages(lesson=filename)


# def extract_lesson_messages(lesson: str) -> None:
#     print(
#         'Reading lesson messages from '' + 'course/' + lesson + '/lesson.tres' + ''...'
#     )

#     method_map = [
#         ('course/' + lesson + '/lesson.tres', 'godot_resource'),
#     ]
#     # options_map = {
#     #     'course/' + lesson + '/lesson.tres': {'encoding': 'utf-8'},
#     # }

#     keywords = {
#         # Content blocks.
#         'Resource/title': None,
#         'Resource/text': None,
#         # Quizzes.
#         'Resource/question': None,
#         'Resource/hint': None,
#         'Resource/content_bbcode': None,
#         'Resource/explanation_bbcode': None,
#         'Resource/valid_answer': None,
#         'Resource/answer_options': None,
#         'Resource/valid_answers': None,
#         # Practices.
#         'Resource/goal': None,
#         'Resource/description': None,
#         'Resource/hints': None,
#     }

#     extract_babel_and_write(
#         method_map=method_map,
#         # options_map=options_map,
#         keywords=keywords,
#         output_file='./i18n/' + lesson + '.pot',
#     )


def extract_and_write(method_map, keywords, output: str) -> None:
    catalog = Catalog(project=PROJECT, version=VERSION, copyright_holder=COPYRIGHT_HOLDER, msgid_bugs_address=BUGS_ADDRESS)
    extracted = extract_from_dir(method_map=method_map, keywords=keywords, callback=log_extraction_file)
    for (filename, message_lineno, message_id, comments, context) in extracted:
        catalog.add(id=message_id, string='', locations=[(filename, message_lineno)], user_comments=comments, context=context)
    with open(output, 'wb') as fileobj:
        pofile.write_po(fileobj, catalog)


# def extract_error_database() -> None:
#     print('Reading error database messages...')

#     extracted_fields = [
#         'error_explanation',
#         'error_suggestion',
#     ]

#     extract_csv_and_write(
#         source_file='./script_checking/error_database.csv',
#         extract_fields=extracted_fields,
#         reference_field='error_code',
#         output_file='./i18n/error_database.pot',
#     )


# def extract_classref_database() -> None:
#     print('Reading classref database messages...')

#     extracted_fields = [
#         'explanation',
#     ]

#     extract_csv_and_write(
#         source_file='./course/documentation.csv',
#         extract_fields=extracted_fields,
#         reference_field='identifier',
#         output_file='./i18n/classref_database.pot',
#     )


# def extract_glossary_database() -> None:
#     print('Reading glossary database messages...')

#     extracted_fields = [
#         'term',
#         'optional_plural_form',
#         'explanation',
#     ]

#     extract_csv_and_write(
#         source_file='./course/glossary.csv',
#         extract_fields=extracted_fields,
#         reference_field='term',
#         output_file='./i18n/glossary_database.pot',
#     )


# def extract_csv_and_write(
#     source_file: str,
#     extract_fields: List[str],
#     reference_field: str,
#     output_file: str,
# ) -> None:

#     print('  Starting extraction...')
#     catalog = Catalog(
#         project=PROJECT,
#         version=VERSION,
#         copyright_holder=COPYRIGHT_HOLDER,
#         msgid_bugs_address=BUGS_ADDRESS,
#     )

#     with open(source_file, 'r', newline='') as cvsfile:
#         reader = csv.DictReader(
#             cvsfile, delimiter=',', quotechar="'", skipinitialspace=True
#         )

#         for row in reader:
#             for field_name in extract_fields:
#                 message_id = row[field_name]
#                 if not message_id:
#                     continue

#                 message_id = message_id.replace('\r\n', '\n')

#                 catalog.add(
#                     id=message_id,
#                     string='',
#                     locations=[(source_file, reader.line_num)],
#                     auto_comments=['Reference: ' + row[reference_field]],
#                     context=None,
#                 )

#     with open(output_file, 'wb') as file:
#         pofile.write_po(
#             fileobj=file,
#             catalog=catalog,
#         )

#     print('  Finished extraction.')


def main():
    extract_and_write_application()
    # extract_course_messages()
    # extract_error_database()
    # extract_classref_database()
    # extract_glossary_database()


if __name__ == '__main__':
    main()
