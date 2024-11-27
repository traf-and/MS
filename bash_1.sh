#!/bin/bash

# Проверяем, был ли передан аргумент
if [ $# -ne 1 ]; then
    echo "Использование: $0 <имя_файла>"
    exit 1
fi

target_file=$1
echo "1.______"
# Создание списка всех файлов и их типов в текущей директории
echo "Список файлов в текущей директории:"
for item in *; do
    if [ -f "$item" ]; then
        type="Файл"
    elif [ -d "$item" ]; then
        type="Каталог"
    else
        type="Другое"
    fi
    echo "$item: $type"
done
echo "2.______"

# Проверка наличия заданного файла
if [ -e "$target_file" ]; then
    echo "Файл '$target_file' существует."
else
    echo "Файл '$target_file' не найден."
fi
echo "3.______"

# Вывод информации о каждом файле: имя и права доступа
echo "Информация о файлах и их правах доступа:"
for item in *; do
    permissions=$(ls -l "$item" | awk '{print $1}')
    echo "$item: $permissions"
done
