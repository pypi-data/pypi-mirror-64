from os import listdir
from os.path import join
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
# from .tasks import extract_file, extract_models_callback
# from celery.task import chord
# import multiprocessing
from django.db import connection
from django.core import serializers


def db_load(*args, **options):

#     def chunk(seq: list, num: int) -> list:
#         avg: float = len(seq) / float(num)
#         last: float = 0.0
#         while last < len(seq):
#             el: list = seq[int(last):int(last + avg)]
#             if len(el) != 0:
#                 yield el
#             last += avg

    def extract_file_no_celery(file_path):
        unparsed = False
        with open(file_path, "r", encoding='utf-8') as file:
            print(f'Попытка запарсить {file_path}')
            data = file.read()
            num = 0
            for obj in serializers.deserialize("json", data):
                num += 1
                try:
                    obj.save()
                except:
                    unparsed = True
            print(f'{num} записей в файле')
            print(f'{apps.get_model(file_path.split("/")[-1].split("_")[0], "_".join(file_path.split("/")[-1].split("_")[1:-1])).objects.count()} в модели на данный момент')
        return unparsed

    dump_path = join(settings.BASE_DIR, 'db_dump')
    models_connections = {}
    models_list = apps.get_models()
    for model in models_list:
        models_connections[f"{model._meta.app_label}_{model._meta.model_name}"] = [f"{key.related_model._meta.app_label}_{key.related_model._meta.model_name}" for key in model._meta.fields if key.related_model]
    parse_order = []
    while len(parse_order) < len(models_list):
        for model_key in models_connections:
            if model_key not in parse_order:
                add_ability = True
                for key in models_connections[model_key]:
                    if key not in parse_order and key != model_key:
                        add_ability = False
                        break
                if add_ability:
                    parse_order.append(model_key)
            else:
                continue
    for model_key in parse_order:
        unparsed = True
        while unparsed:
#             if ???:
#                 chunks = chunk(
#                     [join(dump_path, file_name) for file_name in listdir(dump_path) if f'{model_key}_' in file_name],
#                     multiprocessing.cpu_count())
#             	unparsed = chord([extract_file.s(c) for c in chunks], extract_models_callback.s()).delay().get()
#             else:
            files = [join(dump_path, file_name) for file_name in listdir(dump_path) if f'{model_key}_' in file_name]
            unparsed = any([extract_file_no_celery(file) for file in files])
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"alter sequence {model_key}_id_seq restart with {apps.get_model(model_key.split('_')[0], '_'.join(model_key.split('_')[1:])).objects.count() + 1};")
            except:
                pass

