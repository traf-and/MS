#!/bin/bash

# Функция, которая принимает строку и выводит её с префиксом "Hello, "
greet() {
    local name=$1
    echo "Hello, $name"
}

# Функция, которая принимает два числа и возвращает их сумму
sum() {
    local num1=$1
    local num2=$2
    echo $((num1 + num2))
}

# Вызов функции greet
# echo 
read -p "Введите ваше имя:"  name
greet "$name"

# Вызов функции sum
read -p "Введите первое число:" num1
read -p "Введите второе число:" num2
result=$(sum "$num1" "$num2")
echo "Сумма $num1 и $num2 равна: $result"
