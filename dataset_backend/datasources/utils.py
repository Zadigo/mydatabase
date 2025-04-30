import pandas
from django.utils.crypto import get_random_string
from rest_framework.exceptions import ValidationError


def create_file_name(instance, filename):
    """Creates a simple file name for an
    uploaded file"""
    new_name = get_random_string(length=20)
    return f'sheets/{instance.data_source_id}/{new_name}.csv'


# class CSVData:
#     """Utilities to work with the data from a
#     csv file using Pandas"""

#     def __init__(self, instance, columns_to_keep=[]):
#         self.base_dataframe = None
#         self.dataframe = None
#         self.columns_to_keep = columns_to_keep
#         self.instance = instance
#         try:
#             self.filepath = pathlib.Path(instance.csv_file.path)
#         except:
#             pass
#         else:
#             if self.filepath.exists() and self.filepath.is_file():
#                 self.base_dataframe = pandas.read_csv(self.filepath)
#                 if self.columns_to_keep:
#                     self.dataframe = self.base_dataframe[[
#                         self.columns_to_keep]]

#     def __repr__(self):
#         return f'<CSVData {self.filepath}>'

#     @property
#     def columns(self):
#         return self.base_dataframe.columns

#     @property
#     def count(self):
#         return self.base_dataframe[self.columns[0]].count()

#     def return_data(self, sort_by=None, unique_values=False):
#         df = self.base_dataframe.copy()

#         if sort_by is not None:
#             if sort_by not in self.columns:
#                 raise ValidationError('Column does not exist')
#             df = df.sort_values(sort_by)

#         if unique_values:
#             df = df.drop_duplicates()

#         string_json = df.reset_index().to_json(
#             orient='records',
#             force_ascii=False
#         )
#         # with open(self.filepath, mode='r', encoding='utf-8') as f:
#         #     return list(csv.reader(f))
#         return json.loads(string_json)

#     def save(self, create_copy=False):
#         """Save a new version of the file either as a copy
#         or either as an overwrite of the current file"""
#         if create_copy:
#             filename = f'{self.instance.data_source_id}/{self.filepath.stem}_copy.csv'

#             self.dataframe.to_csv(settings.MEDIA_ROOT / filename)
#             reader = open(filename, mode='r', encoding='utf-8')

#             file = File(reader, name=filename)
#             self.instance.csv_file = file
#             self.instance.save()

#             reader.close()
#         else:
#             self.dataframe.to_csv(self.filepath)

#     def apply_to_dataframe(self, columns, func):
#         """Apply a function to the dataframe calling `df.apply`"""
#         for column in columns:
#             self.dataframe[column] = self.dataframe[column].apply(func)


def create_column_data_types(columns):
    """Function that creates a list that stores the
    column types for each column on the dataset"""
    return [{'name': column, 'column_type': 'Text'} for column in list(columns)]


def check_columns_exists(instance, columns: list[str]):
    if instance.csv_file:
        df = pandas.read_csv(instance.csv_file.path)

        invalid_columns = []
        for item in columns:
            exists = item in df.columns
            if not exists:
                invalid_columns.append(item['column'])
                continue

        if invalid_columns:
            raise ValidationError('Columns are not valid')
