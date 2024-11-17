import os
from docxtpl import DocxTemplate


def render_doc(name, post, event, grade, number, date, address, time1, date2, items, time2, name_of_file):
    doc = DocxTemplate("test2.docx")
    context = {
        "name": name,
        "post": post,
        "event": event,
        "grade": grade,
        "number": number,
        "address": address,
        "date": date,
        "time1": time1,
        "time2": time2,
        "date2": date2,
        "items": items
    }
    doc.render(context)
    doc.save(f"outputs/{name_of_file}.docx")


def delete_file(id_of_file, folder):
    if f'{id_of_file}.docx' in os.listdir(f'C:\PythonProject\Efe_razgrom/{folder}'):
        os.remove(f'{folder}/{id_of_file}.docx')


def render_official_doc(name, grade, address, event, date, time1, time2, name_of_file):
    doc = DocxTemplate("prikaz.docx")
    context = {
        "name": name,
        "grade": grade,
        "address": address,
        "event": event,
        "date": date,
        "time1": time1,
        "time2": time2
    }
    doc.render(context)
    doc.save(f"outputs_from_admin/{name_of_file}.docx")
