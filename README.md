# GEXF Graph Parser

Консольная утилита для анализа GEXF-графа сервисов

## Что делает
- Читает GEXF-файл (например, собранный через HTTP Graph Collector)
- фильтрует host-узлы по домену
- считает общее число hits и долю каждого сервиса
- Выводит результат в виде таблицы/списка

## Установка
```bash
pip install -r requirements.txt
```

## Запуск
```bash
python graph_parser.py
```

Появится интерактивное меню:
- Указать GEXF-файл
- Указать домен
- Указать порог hits
- Показать все сервисы
- Показать сервисы с учетом порога

## Зависиомсти
 - networkx
 - itemlist
 - windows-curses (только для Windows)

## Формсат GEXF
Ожидается структура client -> domain -> host -> resource с атрибутами:
- node_type (тип узла)
- domain (домен узла)
- visited (количество hits)