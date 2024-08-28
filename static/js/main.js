// Получаем ссылку на редактор CodeMirror
var editor = CodeMirror.fromTextArea(document.getElementById('file-content'), {
    mode: 'yaml',
    lineNumbers: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    indentUnit: 2,
    tabSize: 2,
    theme: 'material'
});

// Обработчик события для кнопки 'Открыть'
document.getElementById('dir-form').addEventListener('submit', function(event) {
    var dirPathInput = document.getElementById('dir_path');
    var currentPath = dirPathInput.value.trim(); // Получаем текущий путь и удаляем пробелы
    // Проверяем, является ли введенный путь пустым
    if (currentPath === '') {
        dirPathInput.value = '/home'; // Устанавливаем путь по умолчанию
    }
    // Теперь можно отправлять форму
});


// Обработчик события для кнопки загрузки файла
document.getElementById('upload-file-button').addEventListener('click', function() {
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            // Устанавливаем содержимое файла в редактор
            editor.setValue(e.target.result);
            setEditorMode(file.name); // Устанавливаем режим редактора

            // Отправляем файл на сервер
            fetch('/upload_file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_name: file.name,
                    file_content: e.target.result
                })
            })
            .then(response => response.text())
            .then(data => {
                console.log(data); // Логируем ответ от сервера
                window.location.reload(); // Перезагружаем страницу для обновления файла
            })
            .catch(error => {
                console.error('Ошибка загрузки файла:', error);
            });
        };
        reader.readAsText(file); // Читаем файл как текст
    }
});

// Функция для изменения режима в зависимости от типа файла
function setEditorMode(fileName) {
    var extension = fileName.split('.').pop().toLowerCase(); // Получаем расширение файла
    var mode;

    switch (extension) {
        case 'py':
            mode = 'text/x-python';
            break;
        case 'yml':
            mode = 'text/x-yaml';
            break;

        case 'yaml':
            mode = 'text/x-yaml';
            break;
        case 'ruml':
            mode = 'text/x-yaml';
            break;
        case 'sh':
            mode = 'text/x-sh';
            break;
        case 'js':
            mode = 'application/javascript';
            break;
        case 'ini':
            mode = 'text/x-ini ';
            break;
        case 'json':
            mode = 'application/json';
            break;

        default:
            mode = 'text/plain';
    }

    editor.setOption("mode", mode); // Устанавливаем режим
}

// Обработчик события для кнопки "Наверх"
document.getElementById('up-button').addEventListener('click', function() {
    // Получаем текущий путь из текстового поля
var dirPathInput = document.getElementById('dir_path');
var currentPath = dirPathInput.value;
    // Извлекаем родительский каталог
var parentPath = currentPath.substring(0, currentPath.lastIndexOf('/'));
    // Устанавливаем новый путь в текстовое поле
dirPathInput.value = parentPath;
    // Отправляем форму для обновления списка файлов
document.getElementById('dir-form').submit();
});
