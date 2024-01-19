import json

from mongoengine.errors import NotUniqueError

import connect
from models import Author, Quote


def import_data_from_json(file_name, model_name, related_model=None, related_field=None):
    with open(file_name, encoding='utf-8') as fh:
        data = json.load(fh)
        for el in data:
            try:
                obj = model_name(**el)
                if related_model and related_field:
                    obj_values, *_ = related_model.objects(fullname=el.get(related_field))
                    setattr(obj, related_field, obj_values)
                obj.save()
            except NotUniqueError:
                print(f"{model_name.__name__} already exists: {el.get('fullname')}")

if __name__ == '__main__':
    import_data_from_json('authors.json', Author)
    import_data_from_json('quotes.json', Quote, related_model=Author, related_field='author')
