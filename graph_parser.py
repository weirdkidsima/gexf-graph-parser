import os
import networkx as nx
from itemlist import item

# Глобальные переменные
GEXF_FILE = None
DOMAIN = None
MIN_HITS = None

# Логика
def load_and_filter_hosts():
    """Загружает граф и фильтрует host-узлы по домену"""
    if GEXF_FILE is None:
        print("Ошибка: GEXF-файл не указан")
        return None
    if not os.path.exists(GEXF_FILE):
        print(f"Ошибка: файл {GEXF_FILE} не найден")
        return None

    try:
        G = nx.read_gexf(GEXF_FILE)
    except Exception as e:
        print(f"Ошибка чтения GEXF: {e}")
        return None

    hosts = []
    for node, data in G.nodes(data=True):
        if data.get("node_type") != "host":
            continue
        if DOMAIN is not None and not node.endswith(DOMAIN):
            continue
        hosts.append((node, data))

    if not hosts:
        print("Хосты не найдены")
        return None

    return hosts

def calculate_shares(hosts):
    """Считает общее число hits и долю каждого хоста"""
    total_hits = 0
    for node, data in hosts:
        total_hits += int(data.get("visited", 0) or 0)

    results = []
    for node, data in hosts:
        hits = int(data.get("visited", 0) or 0)
        percent = (hits / total_hits * 100) if total_hits > 0 else 0
        results.append((node, hits, percent))

    results.sort(key=lambda x: x[1], reverse=True)
    return results, total_hits

@item
def set_file(description="Указать GEXF-файл"):
    """Меняет путь к GEXF-файлу"""
    global GEXF_FILE
    current = GEXF_FILE if GEXF_FILE else "не задан"
    new_value = input(f"Текущий файл: {current}\nВведите новый путь: ").strip()
    if new_value:
        GEXF_FILE = new_value
        print(f"Файл: {GEXF_FILE}")
    else:
        print("Оставлено без изменений")

@item
def set_domain(description="Указать домен"):
    """Меняет домен для фильтрации"""
    global DOMAIN
    current = DOMAIN if DOMAIN else "не задан"
    new_value = input(f"Текущий домен: {current}\nВведите новый домен: ").strip()
    if new_value:
        DOMAIN = new_value
        print(f"Домен: {DOMAIN}")
    else:
        print("Оставлено без изменений")


@item
def set_min_hits(description="Указать порог hits"):
    """Меняет порог hits"""
    global MIN_HITS
    current = MIN_HITS if MIN_HITS is not None else "не задан"
    new_value = input(f"Текущий порог: {current}\nВведите новый порог: ").strip()
    if new_value:
        try:
            MIN_HITS = int(new_value)
            print(f"Порог: {MIN_HITS}")
        except ValueError:
            print("Ошибка: нужно число. Оставлено без изменений")
    else:
        print("Оставлено без изменений")

@item
def show_all(description="Показать все сервисы (без порога)"):
    """Выводит все хосты без ограничения по hits"""
    hosts = load_and_filter_hosts()
    if hosts is None:
        return
    results, total = calculate_shares(hosts)
    print(f"\nВсего hits: {total}\n")
    for node, hits, percent in results:
        print(f"{node} — {hits} hits ({percent:.2f}%)")


@item
def show_with_threshold(description="Показать с порогом hits"):
    """Выводит хосты с порогом MIN_HITS"""
    if MIN_HITS is None:
        print("Ошибка: порог не задан. Укажите его через меню")
        return
    hosts = load_and_filter_hosts()
    if hosts is None:
        return
    results, total = calculate_shares(hosts)
    filtered = [r for r in results if r[1] >= MIN_HITS]

    print(f"\nВсего hits: {total}, порог: {MIN_HITS}\n")
    print(f"{'Сервис (host)':<40} {'hits':<10} {'%':<6}")
    print("-" * 60)
    for node, hits, percent in filtered:
        print(f"{node:<40} {hits:<10} {percent:.2f}%")

def main():
    while True:
        selected = item.select()
        item.endwin()

        selected_name, selected_func, selected_func_description = selected

        if selected_func == item._cancel:
            print("Выход")
            break
        else:
            print(f"\n=== {selected_name} ===\n")
            try:
                selected_func()
            except Exception as e:
                print(f"Ошибка выполнения: {e}")
            input("\nНажмите Enter, чтобы вернуться в меню...")


if __name__ == "__main__":
    main()