import csv
import json
import yaml

data = {
    '1': ['1', '2', '3'],
    '2': 2,
    '3': {
        '1$': '1',
        '2@': '2',
        '3&': '3'
    }
}

def get_data():
    files_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    result_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for file_name in files_list:
        with open('files/' + file_name, encoding='windows-1251') as data_file:
            data = data_file.read().split('\n')
            for i in data:
                row_data = i.split(':')
                if 'Изготовитель системы' in row_data[0]:
                    os_prod_list.append(row_data[1].strip())
                if 'Название ОС' in row_data[0]:
                    os_name_list.append(row_data[1].strip())
                if 'Код продукта' in row_data[0]:
                    os_code_list.append(row_data[1].strip())
                if 'Тип системы' in row_data[0]:
                    os_type_list.append(row_data[1].strip())
            result_data.append(
                [
                    os_prod_list[:1][0],
                    os_name_list[:1][0],
                    os_code_list[:1][0],
                    os_type_list[:1][0]
                ]
            )
    return result_data


def write_to_csv(file_name):
    with open(file_name, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        print(get_data())
        for row in get_data():
            csv_writer.writerow(row)


def write_order_to_json(item, quantity, price, buyer, date):
    orders_data = dict()
    with open('orders.json', 'r') as json_file:
        orders_data = json.load(json_file)
    if not 'orders' in orders_data:
        orders_data['orders'] = []
    orders_data['orders'].append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    })
    with open('orders.json', 'w') as json_file:
        json.dump(orders_data, json_file, indent=4)


write_to_csv('new_test.csv')

for i in range(10):
    write_order_to_json(f'Product#{i}', 4 * i, 100 * i, 'Roman', '12-10-2020')

with open('file.yaml', 'w') as fn:
    yaml.dump(data, fn, default_flow_style=True, allow_unicode=True)

with open('file.yaml') as fn:
    yaml_data = yaml.load(fn, Loader=yaml.FullLoader)

if yaml_data == data:
    print('данные совпали')
else:
    print('данные не совпали')
