#!/bin/bash

# Запрашиваем ввод числа у пользователя
echo "Введите число:"
read num

echo "1.____"
# Проверяем, является ли число положительным, отрицательным или нулем
if [ $num -gt 0 ]; then
  echo "Число положительное."
  echo "2.____"
    i=1
  while [ $i -le $num ]; do
    echo $i
    i=$((i+1))
  done
elif [ $num -lt 0 ]; then
  echo "Число отрицательное."
else
  echo "Число равно нулю."
fi
