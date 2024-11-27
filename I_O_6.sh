#!/bin/bash

# Пытаемся выполнить команду ls и перенаправляем ошибки в error.log
ls input.txt 2>> error.log

# Читаем данные из input.txt и подсчитываем количество строк, перенаправляя вывод в output.txt
wc -l < input.txt >> output.txt

# Уведомление о завершении
echo "Скрипт выполнен. Результаты записаны в output.txt и error.log."
