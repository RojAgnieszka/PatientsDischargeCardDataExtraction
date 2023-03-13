#!/usr/bin/env python
# coding: utf-8

from data_manager import DataManager
import utils
import csv
import os
import re


def main():
    dm = DataManager("pacjentka-1-2.pdf")

    with open(os.path.join("..", "config", "records.csv")) as records:
        reader = csv.reader(records, delimiter=';')
        for row in reader:
            load_records(dm, row)

        handle_custom(dm)
        dm.handle_tables()

    dm.pretty_print()
    dm.generate_excel_table(os.path.splitext("pacjentka-1-2.pdf")[0])


def load_records(dm, row):
    label = row.pop(0)
    data = dm.extract_data(row)

    if data:
        dm.add_record(label, data)


# miejsce na rzeczy, które nie pasują do zwykłego patternu
# (nie da się ich zrobić tylko extract_data)
def handle_custom(dm):
    handle_department_book(dm)
    handle_db_sentences(dm)


def handle_department_book(dm):
    data = utils.take_while(
            lambda letter: not letter.isupper(),
            dm.extract_data([
                "(?<=Księga Oddziałowa:).*",
                "[^R]+"
            ])
        )
    dm.add_record("Księga Oddziałowa", data)


def handle_db_sentences(dm):
    data = dm.extract_data([
                "(?<=Księga Oddziałowa:).*",
                "[^.]*"
            ])

    cleaned = utils.filter(
        lambda letter: not letter.isdigit() and letter != "/",
        data[0: data.index("ROZPOZNANIE")]
    )

    sentences = re.split(r'\s+(?=[A-Z](?!\s))',
                         re.sub(r"([A-Z])", r" \1", cleaned).strip())

    for sentence in sentences:
        dm.add_record(sentence, 1)


if __name__ == "__main__":
    main()
