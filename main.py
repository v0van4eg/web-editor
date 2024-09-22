from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Задайте начальный путь к каталогу
dir_path = '/home/poly/PythonProjects/web-editor'
allowed_file_types = ['.txt', '.ini', '.yml', '.ruml', '.cfg', '.xml', '.json', '.yaml', '.py', '.js', '.html', '']

@app.route('/upload_file', methods=['POST'])
def upload_file():
    data = request.get_json()
    file_name = data['file_name']
    file_content = data['file_content']

    # Путь для сохранения файла
    file_path = os.path.join(dir_path, file_name)

    try:
        # Записываем содержимое в новый файл
        with open(file_path, 'w') as f:
            f.write(file_content)
        return 'Файл успешно загружен'
    except OSError as e:
        return f'Ошибка при загрузке файла: {e.strerror}', 500
    except Exception as e:
        return f'Неизвестная ошибка: {str(e)}', 500


@app.route('/file_list')
def file_list():
    global dir_path

    files = []
    try:
        for item in os.listdir(dir_path):
            if item.startswith('.'):
                continue
            file_path = os.path.join(dir_path, item)
            if os.path.isfile(file_path):
                files.append({'name': item, 'path': url_for('index', file=file_path)})
    except FileNotFoundError:
        return {'error': "Указанный каталог не найден."}, 404
    except PermissionError:
        return {'error': "Недостаточно прав для доступа к каталогу."}, 403
    except Exception as e:
        return {'error': str(e)}, 500

    return {'files': files}


@app.route('/', methods=['GET', 'POST'])
def index():
    global dir_path

    # Обработка формы для выбора каталога
    if request.method == 'POST' and 'dir_path' in request.form:
        new_dir_path = request.form['dir_path']
        # Проверяем, является ли введенный путь к каталогу действительным
        if os.path.isdir(new_dir_path):
            dir_path = new_dir_path
            return redirect(url_for('index', dir=dir_path))  # Используем url_for
        else:
            return render_template('index.html', error="Недопустимый путь к каталогу")

    # Обработка пути из URL
    selected_dir = request.args.get('dir', '')
    if selected_dir:
        dir_path = os.path.join(dir_path, selected_dir)

    # Получение списка файлов в каталоге
    directories = []
    files = []
    error_message = None  # Переменная для хранения сообщения об ошибке
    try:
        for item in os.listdir(dir_path):
            full_path = os.path.join(dir_path, item)
            if os.path.isdir(full_path):
                if item.startswith("."):
                    continue  # Пропускаем скрытые файлы
                directories.append((item, os.path.getmtime(full_path)))
            elif os.path.isfile(full_path):
                if item.startswith("."):
                    continue  # Пропускаем скрытые файлы
                if any(item.endswith(ext) for ext in allowed_file_types):
                    files.append((item, os.path.getmtime(full_path)))

        # Сортировка списков по времени изменения
        directories.sort(key=lambda x: x[1], reverse=True)
        files.sort(key=lambda x: x[1], reverse=True)

        # Извлечение только имен файлов и каталогов
        directories = [d[0] for d in directories]
        files = [f[0] for f in files]
    except FileNotFoundError:
        error_message = "Файл или каталог не найден"
    except PermissionError:
        error_message = "Недостаточно прав для доступа к каталогу."
    except Exception as e:
        error_message = f"Ошибка при получении списка файлов: {str(e)}."

    # Обработка запроса с параметром file (открытие файла)
    selected_file = request.args.get('file', '')
    file_content = ''
    if selected_file:
        try:
            with open(selected_file, 'r') as f:
                file_content = f.read()
        except FileNotFoundError:
            error_message = "Файл не найден"
        except IsADirectoryError:
            error_message = "Указанный путь является каталогом, а не файлом."
        except PermissionError:
            error_message = "Недостаточно прав для доступа к файлу."
        except Exception as e:
            error_message = f"Ошибка при открытии файла: {str(e)}."

    # Обработка формы для сохранения файла
    if request.method == 'POST' and 'save' in request.form:
        file_path = request.form['save']
        new_content = request.form['file_content']
        try:
            with open(file_path, 'w') as f:
                f.write(new_content)
            return render_template('index.html',
                                   dir_path=dir_path,
                                   directories=directories,
                                   files=files,
                                   selected_file=selected_file,
                                   file_content=new_content,
                                   success="Файл успешно сохранен!")
        except OSError as e:
            error_message = f"Ошибка при сохранении файла: {e.strerror}"
        except Exception as e:
            error_message = f"Неизвестная ошибка: {str(e)}"

    # Обработка формы для удаления файла
    if request.method == 'POST' and 'delete' in request.form:
        file_path = request.form['delete']
        try:
            if os.path.isfile(file_path):  # Проверяем, является ли путь файлом
                os.remove(file_path)
                return render_template('index.html',
                                       dir_path=dir_path,
                                       directories=directories,
                                       files=files,
                                       selected_file=None,
                                       file_content='',
                                       success="Файл успешно удален!")
            else:
                error_message = "Невозможно удалить каталог"
        except OSError as e:
            error_message = f"Ошибка при удалении файла: {e.strerror}"
        except Exception as e:
            error_message = f"Неизвестная ошибка: {str(e)}"

    # Отображение данных в шаблоне
    return render_template('index.html',
                           dir_path=dir_path,
                           directories=directories,
                           files=files,
                           selected_file=selected_file,
                           file_content=file_content,
                           error=error_message)  # Передаем сообщение об ошибке, если есть


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')