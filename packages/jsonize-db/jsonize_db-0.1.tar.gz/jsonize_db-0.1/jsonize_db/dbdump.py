from os.path import join
from os import listdir, mkdir
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from django.core import serializers


def db_dump(*args, **options):

    dump_path = join(settings.BASE_DIR, 'db_dump')
    if 'db_dump' not in listdir(settings.BASE_DIR):
        mkdir(dump_path)
    models_list = apps.get_models()
    for model in models_list:
        if model.objects.count() > 100000:
            i = 0
            while i < model.objects.count():
                i += 100000
                with open(join(dump_path, f"{model._meta.app_label}_{model._meta.model_name}_{int(i/100000)}.json"), "w", encoding='utf-8') as out:
                    serializers.serialize("json", model.objects.order_by('pk').all()[i - 100000:i], stream=out, ensure_ascii=False)
        else:
            with open(join(dump_path, f"{model._meta.app_label}_{model._meta.model_name}_1.json"), "w", encoding='utf-8') as out:
                serializers.serialize("json", model.objects.order_by('pk').all(), stream=out, ensure_ascii=False)

