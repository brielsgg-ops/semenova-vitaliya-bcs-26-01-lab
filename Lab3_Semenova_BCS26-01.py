import string  # импортируем модуль для работы со строками


def task1():  # расчет средней оценки по физике
    print("\n" + "~°" * 25)
    print(" Задача 1: средняя оценка (20 учеников)")
    print("~°" * 25)
    lst = []  # список для сохранения введенных оценок
    for i in range(1, 21):  # цикл для опроса 20 учеников по очереди
        while True:
            try:
                val = input(f"Введите оценку ученика №{i} (от 2 до 5): ")
                g = int(val)
                if 2 <= g <= 5:  # проверка на допустимый диапазон оценки
                    lst.append(g)
                    break
                else:
                    print("Ошибка: оценка должна быть от 2 до 5")
            except ValueError:
                print("Ошибка: нужно ввести целое число, а не текст")
    avg = sum(lst) / len(lst)  # вычисление среднего значения оценок
    print(f"\n все 20 оценок введены!")
    print(f"Средняя оценка класса: {avg:.2f}\n")


def task2():  # поиск гармонического ряда
    print("\n" + "~°" * 25)
    print(" Задача 2: поиск наибольшего k для гармонического ряда")
    print("~°" * 25)
    while True:
        try:
            val = input("Введите число a (строго больше 1): ")
            a = float(val)
            if a > 1:  # проверка условия для числа а
                break
            else:
                print("Ошибка: число а должно быть больше 1")
        except ValueError:
            print("Ошибка: введите числовое значение")

    k = 0  # счетчик элементов
    total = 0.0  # накопительная сумма ряда
    while True:
        next_val = 1 / (k + 1)  # следующий элемент ряда вида 1/(k+1)
        if total + next_val >= a:  # проверяем, не превысила ли сумма число а
            break
        k += 1
        total += next_val

    print(f"\n Результаты вычислений:")
    print(f"Найденное k: {k}")
    print(f"Итоговая сумма: {total:.6f}\n")


def task3():  # преобразование английского предложения
    print("\n" + "~°" * 25)
    print(" Задача 3: заглавные буквы в предложении")
    print("~°" * 25)
    while True:
        text = input("Введите предложение на английском языке: ").strip()
        if not text:
            print("Ошибка: строка не должна быть пустой")
            continue

        has_rus = any(
            "\u0400" <= c <= "\u04ff" for c in text
        )  # проверяем на наличие русских букв
        if has_rus:
            print("Ошибка: обнаружены русские символы")
            continue

        if not any(c.isalpha() for c in text):  # проверяем наличие букв вообще
            print("Ошибка: строка должна содержать буквы")
            continue
        break

    res = text.title()  # делаем каждую букву каждого слова заглавной
    print(f"\n Результаты:")
    print(f"Исходная строка: {text}")
    print(f"Измененная строка: {res}\n")


def task4():  # поиск дубликатов в списке
    print("\n" + "~°" * 25)
    print(" Задача 4: поиск повторяющихся элементов")
    print("~°" * 25)
    while True:
        text = input("Введите элементы списка через пробел: ").strip()
        if text:
            items = text.split()  # разделяем введенную строку на элементы
            break
        print("Ошибка: список не может быть пустым")

    seen = set()  # множество уже встреченных элементов
    dups = set()  # множество найденных дубликатов
    for item in items:
        if item in seen:
            dups.add(item)
        else:
            seen.add(item)

    print(f"\n Результаты:")
    print(f" Ваш список: {items}")
    if dups:
        print(f"Найденные дубликаты: {list(dups)}")
    else:
        print("Повторяющиеся элементы отсутствуют")
    print()


def task5():  # преобразование массива чисел
    print("\n" + "~°" * 25)
    print(" Задача 5: преобразование массива из 15 элементов")
    print("~°" * 25)
    print("Правила: элементы < 10 станут равны 0, а > 20 станут равны 1")
    while True:
        text = (
            input("Введите ровно 15 целых чисел через пробел: ").strip()
        )
        if not text:
            print("Ошибка: ввод не должен быть пустым")
            continue
        parts = text.split()
        if len(parts) != 15:  # проверка на точное количество чисел
            print(f"Ошибка: введено {len(parts)} вместо 15")
            continue
        try:
            arr = [int(x) for x in parts]  # переводим элементы в целые числа
            break
        except ValueError:
            print("Ошибка: все элементы должны быть целыми числами")

    new_arr = []
    for x in arr:
        if x < 10:
            new_arr.append(0)
        elif x > 20:
            new_arr.append(1)
        else:
            new_arr.append(x)

    print(f"\n Результаты:")
    print(f"Старый массив: {' '.join(map(str, arr))}")
    print(f"Новый массив: {' '.join(map(str, new_arr))}\n")


def main():  # главное меню для выбора задач
    while True:
        print("Главное меню программы:")
        print("1. Задача 1: средняя оценка")
        print("2. Задача 2: гармонический ряд")
        print("3. Задача 3: заглавные буквы")
        print("4. Задача 4: проверка дубликатов")
        print("5. Задача 5: преобразование массива")
        print("6. Выход из программы")
        print("~°" * 25)

        choice = input("Выберите пункт меню (от 1 до 6): ").strip()
        if choice == "1":
            task1()
        elif choice == "2":
            task2()
        elif choice == "3":
            task3()
        elif choice == "4":
            task4()
        elif choice == "5":
            task5()
        elif choice == "6":
            print("\n Работа программы завершена. До свидания!")
            break
        else:
            print("\n Неверный выбор! Введите цифру от 1 до 6. \n")


if __name__ == "__main__":
    main()
