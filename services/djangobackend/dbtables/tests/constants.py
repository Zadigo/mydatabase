from tabledocuments.validation_models import ColumnOptionsModel

OPENDATASOFT_URL = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/panneaux4x3-feuille1@issy-les-moulineaux/records?limit=5'


OPENDATASOFT_COLUMN_TYPES = [
    ColumnOptionsModel(name='numero').model_dump(),
    ColumnOptionsModel(name='numero').model_dump(),
    ColumnOptionsModel(name='etat').model_dump(),
    ColumnOptionsModel(name='date_de_1er_montage').model_dump(),
    ColumnOptionsModel(name='type_panneau').model_dump(),
    ColumnOptionsModel(name='affichage').model_dump(),
    ColumnOptionsModel(name='adresse_emplacement').model_dump(),
    ColumnOptionsModel(name='details_emplacements').model_dump(),
    ColumnOptionsModel(name='code_postal').model_dump(),
    ColumnOptionsModel(name='commune').model_dump(),
    ColumnOptionsModel(name='coordonnees_gps').model_dump(),
    ColumnOptionsModel(name='street_view').model_dump()
]


JSONPLACEHOLDER_URL = 'https://jsonplaceholder.typicode.com/posts'


JSONPLACEHOLDER_COLUMN_TYPES = [
    ColumnOptionsModel(name='userId').model_dump(),
    ColumnOptionsModel(name='id').model_dump(),
    ColumnOptionsModel(name='title').model_dump(),
    ColumnOptionsModel(name='body').model_dump()
]


UPLOAD_DOCUMENT_COLUMN_TYPE = {
    'name': 'firstname',
    'newName': 'firstname',
    'columnType': 'String',
    'unique': False,
    'nullable': True,
    'visible': True,
}


UPLOAD_DOCUMENT_DATA = {
    'name': 'Some file',
    'using_columns': [],
    'documents': [],
    'merge': False
}
