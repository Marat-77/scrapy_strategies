# Получение информации о имеющиихся стратегиях с сайта "comon.ru"

### Получаем данные: ?????????????????
- название товаров;
- изображения товаров;
- ссылки на товары;
- цены товаров (без скидки/со скидкой);
- характеристики товаров.

### Обработанные данные сохраняем в базу данных MongoDB.

Изображения сохраняются в ```productsparser/prod_images/full/```
* можно указать иной путь в ```productsparser/settings.py```:
```python
IMAGES_STORE = 'prod_images'
```
Для каждого товара своя подпапка с изображениями ```productsparser/prod_images/full/{код товара}/```

Код товара используется и в базе данных в качестве ```'_id'```

В базу данных сохраняется путь к файлу изображения.

---
## Для работы необходимо:

1. Установить **scrapy**, **pymongo** и **pillow**:
```commandline
pip install scrapy
pip install pymongo
pip install pillow ------------------------?????????????????????????????
```
или из файла ```requirements.txt```:
```commandline
pip install -r requirements.txt
```
или
```commandline
python -m pip install -r requirements.txt
```
2. Запустить контейнер с MongoDB:
```commandline
docker run -d --name mongo_scrap -p 27017:27017 -v mongodb_scrap:/data/db mongo
```
В файле ```productsparser/settings.py``` необходимо указать IP-адрес и порт сервера MongoDB:
```python
# Настройки для MongoDB:
MONGO_HOST = '192.168.2.230'
MONGO_PORT = 27017
```
Так же можно указать базу данных (comon_db):
```python
MONGO_DATABASE = 'comon_db'
```
и коллекцию:
```python
MONGO_COLLECTION = 'strategies'
```
3. запустите ```productsparser/runner.py```
