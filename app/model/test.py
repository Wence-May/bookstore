import json 
from create_db import OrderBooks,StoreBooks
# 

def to_dict(result:object,dropwords:list)->dict:
    dic = {}
    for att in dir(result):
        if att.startswith("_") or att in dropwords:
            continue
        value = getattr(result,att)
        dic[att] = value
    return dic
a = StoreBooks()
print(to_dict(a,["metadata"]))