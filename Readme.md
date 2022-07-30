# Получение информации об имеющихся стратегиях с сайта "comon.ru"
<svg xmlns="http://www.w3.org/2000/svg" width="60" height="20" role="img">
    <rect x="0" y="0" rx="5" ry="5" width="60" height="20" fill="#0d1117"/>
    <rect x="1" y="1" rx="5" ry="5" width="58" height="18" fill="white"/>
    <rect x="2" y="2" rx="5" ry="5" width="56" height="16" fill="#0d1117"/>
    <text font-size="14" text-anchor="start" x="5" y="14" fill="white">Python</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" width="62" height="20" role="img">
    <rect x="0" y="0" rx="5" ry="5" width="62" height="20" fill="#0d1117"/>
    <rect x="1" y="1" rx="5" ry="5" width="60" height="18" fill="white"/>
    <rect x="2" y="2" rx="5" ry="5" width="58" height="16" fill="#0d1117"/>
    <text font-size="14" text-anchor="start" x="5" y="14" fill="white">Docker</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" width="72" height="20" role="img">
    <rect x="0" y="0" rx="5" ry="5" width="72" height="20" fill="#0d1117"/>
    <rect x="1" y="1" rx="5" ry="5" width="70" height="18" fill="white"/>
    <rect x="2" y="2" rx="5" ry="5" width="68" height="16" fill="#0d1117"/>
    <text font-size="14" text-anchor="start" x="5" y="14" fill="white">MongoDB</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" width="70" height="20" role="img">
    <rect x="0" y="0" rx="5" ry="5" width="70" height="20" fill="#0d1117"/>
    <rect x="1" y="1" rx="5" ry="5" width="68" height="18" fill="white"/>
    <rect x="2" y="2" rx="5" ry="5" width="66" height="16" fill="#0d1117"/>
    <text font-size="14" text-anchor="start" x="5" y="14" fill="white">PyMongo</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" width="60" height="20" role="img">
    <rect x="0" y="0" rx="5" ry="5" width="60" height="20" fill="#0d1117"/>
    <rect x="1" y="1" rx="5" ry="5" width="58" height="18" fill="white"/>
    <rect x="2" y="2" rx="5" ry="5" width="56" height="16" fill="#0d1117"/>
    <text font-size="14" text-anchor="start" x="5" y="14" fill="white">Scrapy</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" width="80" height="20" role="img">
    <rect x="0" y="0" rx="5" ry="5" width="80" height="20" fill="#0d1117"/>
    <rect x="1" y="1" rx="5" ry="5" width="78" height="18" fill="white"/>
    <rect x="2" y="2" rx="5" ry="5" width="76" height="16" fill="#0d1117"/>
    <text font-size="14" text-anchor="start" x="5" y="14" fill="white">Selenium</text>
</svg>
<svg xmlns="http://www.w3.org/2000/svg" width="138" height="20" role="img">
    <rect x="0" y="0" rx="5" ry="5" width="138" height="20" fill="#0d1117"/>
    <rect x="1" y="1" rx="5" ry="5" width="136" height="18" fill="white"/>
    <rect x="2" y="2" rx="5" ry="5" width="134" height="16" fill="#0d1117"/>
    <text font-size="14" text-anchor="start" x="5" y="14" fill="white">Scrapy-Selenium</text>
</svg>

### Получаем данные:
- id стратегии
- ссылка на стратегию
- название стратегии
- ссылка на автора стратегии
- автор стратегии
- количество подписчиков
- доходность за год
- минимальная сумма
- максимальная просадка
- риск
- описание

### Обработанные данные сохраняем в базу данных MongoDB.
**comon_db**

---
## Для работы необходимо:

1. Установить **scrapy**, **selenium**, **scrapy-selenium** и **pymongo**:
```commandline
pip install scrapy
pip install selenium
pip install scrapy-selenium
pip install pymongo
```
или из файла ```requirements.txt```:
```commandline
pip install -r requirements.txt
```
или
```commandline
python -m pip install -r requirements.txt
```

2. Скачать и распаковать драйвер для вашего браузера в папку с проектом ```strategiesparser/```

*Можно найти на странице: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/*

3. Запустить контейнер с MongoDB:
```commandline
docker run -d --name mongo_scrap -p 27017:27017 -v mongodb_scrap:/data/db mongo
```

4. В файле ```strategiesparser/settings.py``` необходимо указать IP-адрес и порт сервера MongoDB:
```python
# Настройки для MongoDB:
MONGO_HOST = '192.168.2.230'
MONGO_PORT = 27017
```
Так же можно указать свою базу данных (comon_db):
```python
MONGO_DATABASE = 'comon_db'
```
и свою коллекцию:
```python
MONGO_COLLECTION = 'strategies'
```

5. запустите ```strategiesparser/runner.py```
