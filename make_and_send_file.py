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


def delete_file(id_of_file):
    if f'{id_of_file}.docx' in os.listdir('C:\PythonProject\Efe_razgrom\outputs'):
        os.remove(f'outputs/{id_of_file}.docx')