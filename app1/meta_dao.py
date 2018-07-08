
import json

from models import MetaModel


SPLITTR = "#$#"

class MetaDao(object):
    @staticmethod
    def list_tables():
        try:
            tables = json.load(open(r"./conf/meta.json", "r"))
            return tables
        except Exception, e:
            print e
            return []

    @staticmethod
    def get_table(name):
        try:
            # get table meta from meta.
            tables = json.load(open(r"./conf/meta.json", "r"))
            for table in tables:
                if table["name"] == name:

                    return table
            return {}
        except Exception, e:
            print e
            return {}

    @staticmethod
    def get_table_data(name):
        try:
            # get table meta from meta.
            data_meta = MetaModel.objects.filter(table_name=name,type_name="data")
            data = []
            for x in data_meta:
                data.append(x.row_value.split(SPLITTR))
            return data
        except Exception, e:
            print e
            return []

    @staticmethod
    def add_table_row(name, col_values):
        try:
            # get table meta from meta.
            values = MetaModel.objects.filter(table_name=name)
            rowids = []
            for t in values:
                rowids.append(int(t.row_id))
            new_row_id = 1
            if rowids:
                new_row_id = max(rowids)+1
            c = MetaModel(
                table_name=name,
                type_name="data",
                row_id=new_row_id,
                row_value=SPLITTR.join(col_values))
            c.save()
            return True
        except Exception, e:
            print e
            return False

