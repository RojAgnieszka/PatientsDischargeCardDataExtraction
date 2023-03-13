import PyPDF2 as readpdf
import pandas as pd
import tabula.io
import utils
import os
import re
from colorama import Fore, Back, Style


class DataManager:
    def __init__(self, filename):
        self.path = os.path.join("..", "data", filename)
        self.reader = readpdf.PdfFileReader(open(self.path, "rb"))
        self.record_list = []
        self.pages = []

        self.init_pages()

    def init_pages(self):
        for i in range(0, self.reader.getNumPages()):
            self.pages.append(
                utils.fix_polish_chars(
                    self.reader.getPage(i).extractText()
                )
            )

    def extract_data(self, regex_list):
        data = self.search_in_pdf(regex_list.pop(0))

        for regex in regex_list:
            search = re.search(regex, data)
            if search:
                data = search.group()

        return data

    def search_in_pdf(self, regex):
        data = ""
        for page in self.pages:
            search = re.search(regex, page)
            if search:
                data = search.group()

            if data.strip():
                return data

        return data

    def add_record(self, label, data):
        self.record_list.append((label, data))

    def print_record_list(self):
        print(self.record_list)

    def pretty_print(self):
        for record in self.record_list:
            print(record[0], end=": ")
            print(Fore.YELLOW + str(record[1]))
            print(Style.RESET_ALL, end="")

    def handle_tables(self):
        tables = tabula.io.read_pdf(self.path, pages='all')
        for i, table in enumerate(tables, 0):
            if i != len(tables) - 1:
                self.extract_table_data(table)

    def extract_table_data(self, table):
        for item in table.iteritems():
            column = pd.Series.tolist(item[1])
            column.insert(0, item[0])

            record = []
            for value in column:
                if not pd.isna(value):
                    self.parse_value(value, record)

    def parse_value(self, value, record):
        record.append(value)
        # print(value, end=", type=")
        print(type(value))
        if len(record) < 2:
            return
        else:
            self.add_record(record[0], record[1])
            record.clear()

    def generate_excel_table(self, name):
        table = pd.DataFrame(
            self.record_list, columns=["Wpis", "Wartość"]
        ).set_index("Wpis")
        table.to_excel("dane_pacjentów.xlsx", sheet_name=name)
