# from typing import List
# from fogz.celery import app
# from django.apps import apps
# from django.core import serializers
# 
# 
# @app.task(name='extract_file')
# def extract_file(file_pathes: List[str]):
#     unparsed = False
#     for file_path in file_pathes:
#         with open(file_path, "r", encoding='utf-8') as file:
#             print(f'Попытка запарсить {file_path}')
#             data = file.read()
#             num = 0
#             for obj in serializers.deserialize("json", data):
#                 num += 1
#                 try:
#                     obj.save()
#                 except:
#                     unparsed = True
#             print(f'{num} записей в файле')
#             print(f'{apps.get_model(file_path.split("/")[-1].split("_")[0], "_".join(file_path.split("/")[-1].split("_")[1:-1])).objects.count()} в модели на данный момент')
#     return unparsed
# 
# 
# @app.task(name='extract_models_callback')
# def extract_models_callback(results):
#     return any(results)

