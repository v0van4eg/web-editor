import os
# Указываем имя выходного файла
output_file_name = "Исходники.txt"

# Функция для получения содержимого файла
def get_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)  # В случае ошибки вернуть текст ошибки


# Функция для построения дерева каталога, исключая скрытые файлы и директории
def list_directory_tree(startpath, report_file, prefix=''):
    items = os.listdir(startpath)
    items.sort()  # Сортируем для последовательности вывода

    for i, item in enumerate(items):
        # Исключаем скрытые файлы и каталоги
        if item.startswith('.'):
            continue

        path = os.path.join(startpath, item)
        connector = '└── ' if i == len(items) - 1 else '├── '
        # Записываем в файл
        report_file.write(f"{prefix}{connector}{item}\n")

        if os.path.isdir(path):  # Если это директория, рекурсивно вызываем функцию
            list_directory_tree(path, report_file, prefix + ('    ' if connector == '└── ' else '│   '))


# Основная функция, создающая текстовый файл со структурой каталога и содержимым файлов
def create_directory_tree_report(output_file):
    current_dir = os.getcwd()

    with open(output_file, 'w') as report_file:
        report_file.write(f"Дерево текущего каталога: {current_dir}\n\n")
        list_directory_tree(current_dir, report_file)  # Вывод дерева каталогов

        # Проверяем наличие специфичных файлов и записываем их содержимое
        files_to_check = ['main.py', 'static/css/styles.css', 'static/js/main.js', 'templates/index.html']
        report_file.write("\nСодержимое файлов:\n\n")

        for file_name in files_to_check:
            # Преобразуем в полный путь
            file_path = os.path.join(current_dir, file_name)
            report_file.write(f"Имя файла: {file_name}\n")
            # Если файл существует, добавляем его содержимое
            if os.path.isfile(file_path):
                content = get_file_content(file_path)
                report_file.write(f"Содержимое файла:\n{content}\n")
            else:
                report_file.write("Файл не найден.\n")
            report_file.write("\n")



create_directory_tree_report(output_file_name)

print(f"Отчёт о каталоге сохранён в {output_file_name}")
