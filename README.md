## Проект

Каталог ссылок URLcatalog. Через веб-интерфейс или api можно просмотривать, удалять и сохранять сслыки в каталог. 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/A-A-Tyurin/URLcatalog
```

Создать файл .env по шаблону .env.template

### Через docker:

Собрать образ из Dockerfile:

```
sudo docker build . -t url-catalog
```

Запустить контейнер:

```
sudo docker run -dp 5000:5000 url-catalog
```

### Локальный dev-сервер:

```
python3 run.py
```

## API:

Получить список ссылок

```
[GET] /api/v1/
```

### Получить отфильтрованный список ссылок

```
[GET] /api/v1/?param_1=value_1&param_2=value_2&...
```
Доступные параметры: id, uuid, scheme, domain, zone, path

### Сохранить ссылку

```
[POST] /api/v1/
```
JSON схема: { "url": "url_value" }

### Сохранить список ссылок из csv файла

```
[POST] /api/v1/
```

### Получить ссылку по id

```
[GET] /api/v1/<int:id>
```

### Получить ссылку по uuid

```
[GET] /api/v1/<uuid>
```

### Получить последние 20 записей лога

```
[GET] /api/v1/log
```
