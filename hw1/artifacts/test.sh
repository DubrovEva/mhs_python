#!/bin/bash

test_task1() {
    echo "=== Тестирование task1 (nl.py) ==="
    echo
    
    echo "Тест 1: Чтение из файла (первые 4 строки)"
    echo "Команда: python3 ../task1/nl.py input.txt | head -n 4"
    output=$(python3 ../task1/nl.py input.txt | head -n 4)
    echo "$output"
    line_count=$(echo "$output" | wc -l)
    if [ "$line_count" -eq 4 ]; then
        echo "✓ УСПЕХ: Выведено ровно 4 строки"
    else
        echo "✗ ОШИБКА: Выведено $line_count строк, ожидалось 4"
    fi
    if echo "$output" | grep -q "     1"; then
        echo "✓ УСПЕХ: Присутствует нумерация строк"
    else
        echo "✗ ОШИБКА: Нумерация строк отсутствует"
    fi
    echo
    
    echo "Тест 2: Чтение из stdin"
    echo "Команда: echo -e \"Line one\nLine two\nLine three\" | python3 ../task1/nl.py"
    output=$(echo -e "Line one\nLine two\nLine three" | python3 ../task1/nl.py)
    echo "$output"
    line_count=$(echo "$output" | wc -l)
    if [ "$line_count" -eq 3 ]; then
        echo "✓ УСПЕХ: Выведено ровно 3 строки"
    else
        echo "✗ ОШИБКА: Выведено $line_count строк, ожидалось 3"
    fi
    if echo "$output" | grep -q "     1.*Line one" && echo "$output" | grep -q "     3.*Line three"; then
        echo "✓ УСПЕХ: Строки правильно пронумерованы"
    else
        echo "✗ ОШИБКА: Неправильная нумерация строк"
    fi
    echo
    
    echo "Тест 3: Несуществующий файл (должна быть ошибка)"
    echo "Команда: python3 ../task1/nl.py nonexistent.txt"
    python3 ../task1/nl.py nonexistent.txt 2>&1
    exit_code=$?
    if [ "$exit_code" -ne 0 ]; then
        echo "✓ УСПЕХ: Возвращен код ошибки $exit_code"
    else
        echo "✗ ОШИБКА: Ожидался код ошибки, получен $exit_code"
    fi
    echo
    
    echo "=== Тестирование task1 завершено ==="
    echo
}

test_task2() {
    echo "=== Тестирование task2 (tail.py) ==="
    echo
    
    echo "Тест 1: Последние 10 строк из файла"
    echo "Команда: python3 ../task2/tail.py input.txt"
    output=$(python3 ../task2/tail.py input.txt)
    echo "$output"
    line_count=$(echo "$output" | wc -l)
    if [ "$line_count" -eq 10 ]; then
        echo "✓ УСПЕХ: Выведено ровно 10 строк"
    else
        echo "✗ ОШИБКА: Выведено $line_count строк, ожидалось 10"
    fi
    if echo "$output" | grep -q "Line 11" && echo "$output" | grep -q "Line 20"; then
        echo "✓ УСПЕХ: Выведены последние строки (Line 11 - Line 20)"
    else
        echo "✗ ОШИБКА: Выведены не последние строки"
    fi
    echo
    
    echo "Тест 2: Несколько файлов (должны выводиться имена файлов)"
    echo "Команда: python3 ../task2/tail.py input.txt input2.txt"
    output=$(python3 ../task2/tail.py input.txt input2.txt)
    echo "$output"
    if echo "$output" | grep -q "==> input.txt <==" && echo "$output" | grep -q "==> input2.txt <=="; then
        echo "✓ УСПЕХ: Присутствуют заголовки для обоих файлов"
    else
        echo "✗ ОШИБКА: Заголовки файлов отсутствуют или неверные"
    fi
    if echo "$output" | grep -q "Line 20" && echo "$output" | grep -q "With two lines"; then
        echo "✓ УСПЕХ: Содержимое файлов выведено корректно"
    else
        echo "✗ ОШИБКА: Содержимое файлов выведено неверно"
    fi
    echo
    
    echo "Тест 3: Чтение из stdin (последние 17 строк)"
    echo "Команда: cat input.txt | python3 ../task2/tail.py"
    output=$(cat input.txt | python3 ../task2/tail.py)
    echo "$output"
    line_count=$(echo "$output" | wc -l)
    if [ "$line_count" -eq 17 ]; then
        echo "✓ УСПЕХ: Выведено ровно 17 строк"
    else
        echo "✗ ОШИБКА: Выведено $line_count строк, ожидалось 17"
    fi
    echo
    
    echo "Тест 4: Несуществующий файл (должна быть ошибка)"
    echo "Команда: python3 ../task2/tail.py nonexistent.txt"
    python3 ../task2/tail.py nonexistent.txt 2>&1
    exit_code=$?
    if [ "$exit_code" -ne 0 ]; then
        echo "✓ УСПЕХ: Возвращен код ошибки $exit_code"
    else
        echo "✗ ОШИБКА: Ожидался код ошибки, получен $exit_code"
    fi
    echo
    
    echo "=== Тестирование task2 завершено ==="
    echo
}

test_task3() {
    echo "=== Тестирование task3 (wc.py) ==="
    echo
    
    echo "Тест 1: Один файл"
    echo "Команда: python3 ../task3/wc.py input2.txt"
    output=$(python3 ../task3/wc.py input2.txt)
    expected="      2       5      27 input2.txt"
    if [ "$output" = "$expected" ]; then
        echo "✓ УСПЕХ: $output"
    else
        echo "✗ ОШИБКА"
        echo "Ожидалось: $expected"
        echo "Получено:  $output"
    fi
    echo
    
    echo "Тест 2: Несколько файлов с итогом"
    echo "Команда: python3 ../task3/wc.py input2.txt input.txt"
    output=$(python3 ../task3/wc.py input2.txt input.txt)
    echo "$output"
    total_line=$(echo "$output" | tail -n 1)
    if echo "$total_line" | grep -q "total"; then
        echo "✓ УСПЕХ: Итоговая строка присутствует"
    else
        echo "✗ ОШИБКА: Итоговая строка отсутствует"
    fi
    echo
    
    echo "Тест 3: Чтение из stdin"
    echo "Команда: echo -e \"Line one\nLine two\" | python3 ../task3/wc.py"
    output=$(echo -e "Line one\nLine two" | python3 ../task3/wc.py)
    expected="      2       4      18"
    if [ "$output" = "$expected" ]; then
        echo "✓ УСПЕХ: $output"
    else
        echo "✗ ОШИБКА"
        echo "Ожидалось: $expected"
        echo "Получено:  $output"
    fi
    echo
    
    echo "Тест 4: Пустой ввод через stdin"
    echo "Команда: echo -n \"\" | python3 ../task3/wc.py"
    output=$(echo -n "" | python3 ../task3/wc.py)
    expected="      0       0       0"
    if [ "$output" = "$expected" ]; then
        echo "✓ УСПЕХ: $output"
    else
        echo "✗ ОШИБКА"
        echo "Ожидалось: $expected"
        echo "Получено:  $output"
    fi
    echo
    
    echo "=== Тестирование task3 завершено ==="
    echo
}

main() {
    cd "$(dirname "$0")" || exit 1
    
    if [ $# -eq 0 ]; then
        echo "=========================================="
        echo "Запуск всех тестов"
        echo "=========================================="
        echo
        test_task1
        test_task2
        test_task3
        echo "=========================================="
        echo "Все тесты завершены"
        echo "=========================================="
    elif [ "$1" = "task1" ]; then
        test_task1
    elif [ "$1" = "task2" ]; then
        test_task2
    elif [ "$1" = "task3" ]; then
        test_task3
    else
        echo "Использование: $0 [task1|task2|task3]"
        echo "  Без параметров - запуск всех тестов"
        echo "  task1 - тестирование только первой задачи"
        echo "  task2 - тестирование только второй задачи"
        echo "  task3 - тестирование только третьей задачи"
        exit 1
    fi
}

main "$@"
