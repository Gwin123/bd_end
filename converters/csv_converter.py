import csv
from json import dump

from openpyxl import Workbook


def write_to_csv(model, filename):
    data = model.select().tuples()

    with open(f'{filename}.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        headers = [x for x in model._meta.sorted_field_names]
        csv_out.writerow(headers)

        for row in data:
            try:
                csv_out.writerow(row)
            except:
                print("Ошибка чтения кодировки")


def write_to_excel(model, filename):
    data = model.select().tuples()
    workbook = Workbook()
    worksheet = workbook.active

    headers = [x for x in model._meta.sorted_field_names]
    worksheet.append(headers)
    for row in data:
        worksheet.append([*row])

    workbook.save(filename=f'{filename}.xlsx')


def write_to_json(model, filename):
    data = [model_instance.__dict__['__data__'] for model_instance in model.select()]

    with open(f'{filename}.json', 'w') as file:
        dump(data, file)
