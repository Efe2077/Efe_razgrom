import os
from math import ceil
import pymorphy3

from docxtpl import DocxTemplate

from declension import get_fio


def delete_file(id_of_file, folder, official=''):
    if f'{id_of_file}{official}.docx' in os.listdir(f'C:\PythonProject\Efe_razgrom/{folder}'):
        os.remove(f'{folder}/{id_of_file}{official}.docx')


def make_dicts(names):
    lst = []

    for value in names.split(', '):
        value = value.rstrip()
        lst.append(" ".join([name.capitalize() for name in value.split()]))

    all_dict = []

    x = 0

    for i in range(ceil(len(lst) / 3)):
        if x < len(lst):
            x += 3
            all_dict.append({"cols": lst[i * 3: x]})
        else:
            all_dict.append({"cols": lst[x - 1:]})

    return all_dict


def render_doc(name, post, event, grade, number, date, address, time1, date2, items, time2, name_of_file):
    doc = DocxTemplate("zayvka.docx")
    context = {
        "name": " ".join([nm.capitalize() for nm in name.split()]),
        "post": post.capitalize(),
        "event": event,
        "grade": grade,
        "number": number,
        "address": address.capitalize(),
        "date": date,
        "time1": time1,
        "time2": time2,
        "date2": date2,
        "tbl_contents": make_dicts(items)
    }
    doc.render(context)

    doc.save(f"outputs/{name_of_file}.docx")


def declension(name, case):
    morph = pymorphy3.MorphAnalyzer()
    parsed_name = morph.parse(name)[0]
    return parsed_name.inflect({case}).word


def render_official_doc(name, grade, address, event, date, time1, time2, name_of_file):
    a = get_fio(name)

    context = {
        "name": a[0],
        "name_gen": a[2],
        "name_dat": a[3],
        "name_acc": a[1],
        "grade": grade,
        "event": event,
        "address": address,
        "date": date,
        "time1": time1,
        "time2": time2
    }

    doc = DocxTemplate("prikaz.docx")
    doc.render(context)
    doc.save(f"outputs_from_admin/{name_of_file}res_prikaz.docx")