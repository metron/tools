"""
Утилита составляет в памяти список с именами файлов по пути base_path, в
поддиректориях good_paths, с допустимыми расширениями good_extensions
Затем, вторым шагом, анализирует, нет ли (дублей) файлов с таким же именем и
размером с расположением base_path_double в поддиректориях bad_paths
Если дубли находятся, то они перемещаются в папку base_path_junk в
соответствующие поддиректории
"""

import os
import shutil
import pathlib

# базовый путь, где имеются оригинальные файлы
base_path = '/media/wd/natali/Фотографии'
# базовый путь, где лежат возможные дубли оригиналов
base_path_double = '/media/wd/irina/Foto'
# базовый путь, куда перемещать найденные файлы дубли
base_path_junk = '/media/wd/natali/Фото_junk'

# поддиректории внутри base_path, которые нельзя удалять, основные данные
good_paths = [
    'sub_dir1', 'sub_dir2',
]
good_extensions = [
    '.JPG', '.AVI', '.jpg', 'jpeg', '.png', '.ORF', '.mp4', '.MOV', '.doc'
]

# поддиректории внутри base_path_double, которыe нужно анализировать на дубли
bad_paths = [
    '',
]

# 1. Заполняем словарь хорошими данными
good_files = {}
for good_path in good_paths:
    path = os.path.join(base_path, good_path)
    # перебираем все поддиректории рекуррентно
    for cur_walk in os.walk(path):
        # перебираем все имена файлов типа JPG
        for file_name in cur_walk[2]:
            if not file_name[-4:] in good_extensions:
                continue
            file_path = os.path.join(cur_walk[0], file_name)
            good_files[file_name] = [cur_walk[0], os.path.getsize(file_path)]

# перебираем файлы, кандидаты на удаление дублей
for bad_path in bad_paths:
    path = os.path.join(base_path_double, bad_path)
    # перебираем все поддиректории рекуррентно
    for cur_walk in os.walk(path):
        # перебираем все имена файлов типа JPG
        for file_name in cur_walk[2]:
            if not file_name[-4:] in good_extensions:
                continue
            # если такое имя файла уже имеется среди хороших файлов
            if file_name in good_files:
                file_path = os.path.join(cur_walk[0], file_name)
                # и размеры файлов совпали
                if good_files[file_name][1] == os.path.getsize(file_path):
                    target_dir = os.path.join(
                        base_path_junk,
                        os.path.relpath(cur_walk[0], start=base_path_double)
                    )
                    pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)
                    # то перемещаем файл в мусорную директорию
                    print(file_path, 'copy in', good_files[file_name][0])
                    shutil.move(file_path, target_dir)

