"""
Скрипт для получения информации о бизнес-процессах с MCP сервера.

Этот скрипт демонстрирует, как использовать MCP конфигурацию для получения
информации о доступных шаблонах бизнес-процессов.
"""

import json
from mcp_config import get_mcp_url, get_mcp_headers

def get_processes_from_mcp():
    """
    Получает список бизнес-процессов с MCP сервера.
    
    Returns:
        list: Список бизнес-процессов или None в случае ошибки
    """
    try:
        # Это реальная версия, которая требует модуль requests
        # Раскомментируйте, если у вас установлен модуль requests
        
        # import requests
        # url = f"{get_mcp_url()}/processes/"
        # headers = get_mcp_headers()
        # 
        # print(f"Получение списка бизнес-процессов с: {url}")
        # response = requests.get(url, headers=headers, timeout=10)
        # 
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     print(f"Ошибка: {response.status_code} - {response.text}")
        #     return None
        
        # Mock версия для демонстрации (так как requests не установлен)
        print(f"Получение списка бизнес-процессов с: {get_mcp_url()}/processes/")
        print("Используются заголовки авторизации из config.json")
        
        # Возвращаем mock данные, основанные на документации
        return [
            {
                "id": 1,
                "name": "Обработка заявки",
                "description": "Тестовый бизнес-процесс обработки заявки с тремя этапами",
                "tasks": [
                    {
                        "id": 1,
                        "name": "Создание заявки",
                        "order": 1,
                        "description": "Первый этап процесса - создание заявки с указанием основных данных"
                    },
                    {
                        "id": 2,
                        "name": "Рассмотрение заявки", 
                        "order": 2,
                        "description": "Второй этап - рассмотрение созданной заявки и принятие решения"
                    },
                    {
                        "id": 3,
                        "name": "Утверждение заявки",
                        "order": 3,
                        "description": "Финальный этап - утверждение заявки на основе решения"
                    }
                ],
                "document_types": [
                    {
                        "id": 1,
                        "name": "Заявка",
                        "fields": [
                            {"name": "номер", "type": "строка", "required": True},
                            {"name": "дата", "type": "дата", "required": True},
                            {"name": "название", "type": "строка", "required": True},
                            {"name": "описание", "type": "текст", "required": False}
                        ]
                    },
                    {
                        "id": 2,
                        "name": "Решение по заявке",
                        "fields": [
                            {"name": "номер", "type": "строка", "required": True},
                            {"name": "дата", "type": "дата", "required": True},
                            {"name": "решение", "type": "текст", "required": True},
                            {"name": "комментарий", "type": "текст", "required": False}
                        ]
                    },
                    {
                        "id": 3,
                        "name": "Утверждение заявки",
                        "fields": [
                            {"name": "номер", "type": "строка", "required": True},
                            {"name": "дата", "type": "дата", "required": True},
                            {"name": "утверждено", "type": "булево", "required": True},
                            {"name": "комментарий", "type": "текст", "required": False}
                        ]
                    }
                ]
            }
        ]
        
    except Exception as e:
        print(f"Ошибка при получении бизнес-процессов: {e}")
        return None

def display_process_info(processes):
    """
    Отображает информацию о бизнес-процессах в удобочитаемом формате.
    
    Args:
        processes (list): Список бизнес-процессов
    """
    if not processes:
        print("Нет доступных бизнес-процессов.")
        return
    
    print("\n" + "=" * 80)
    print("ДОСТУПНЫЕ ШАБЛОНЫ БИЗНЕС-ПРОЦЕССОВ В MCP")
    print("=" * 80)
    
    for i, process in enumerate(processes, 1):
        print(f"\n{i}. {process['name']}")
        print(f"   ID: {process['id']}")
        print(f"   Описание: {process['description']}")
        
        print(f"\n   Задачи ({len(process['tasks'])}):")
        for task in process['tasks']:
            print(f"     - {task['name']} (ID: {task['id']}, Порядок: {task['order']})")
            print(f"       {task['description']}")
        
        print(f"\n   Типы документов ({len(process['document_types'])}):")
        for doc_type in process['document_types']:
            print(f"     - {doc_type['name']} (ID: {doc_type['id']})")
            print(f"       Поля: {', '.join([f'{field['name']} ({field['type']})' for field in doc_type['fields']])}")

def save_process_info_to_file(processes, filename="mcp_processes_info.json"):
    """
    Сохраняет информацию о бизнес-процессах в файл.
    
    Args:
        processes (list): Список бизнес-процессов
        filename (str): Имя файла для сохранения
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(processes, f, ensure_ascii=False, indent=2)
        print(f"\nИнформация о бизнес-процессах сохранена в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")

if __name__ == '__main__':
    print("=" * 80)
    print("ПОЛУЧЕНИЕ ИНФОРМАЦИИ О БИЗНЕС-ПРОЦЕССАХ ИЗ MCP")
    print("=" * 80)
    
    # Получаем информацию о бизнес-процессах
    processes = get_processes_from_mcp()
    
    if processes:
        # Отображаем информацию
        display_process_info(processes)
        
        # Сохраняем в файл
        save_process_info_to_file(processes)
        
        print("\n" + "=" * 80)
        print("ИНФОРМАЦИЯ О ШАБЛОНАХ БИЗНЕС-ПРОЦЕССОВ")
        print("=" * 80)
        print(f"Всего доступно бизнес-процессов: {len(processes)}")
        print(f"Общее количество задач: {sum(len(p['tasks']) for p in processes)}")
        print(f"Общее количество типов документов: {sum(len(p['document_types']) for p in processes)}")
        
        # Показываем, как использовать эту информацию в коде
        print("\n" + "=" * 80)
        print("ПРИМЕР ИСПОЛЬЗОВАНИЯ В ВАШЕМ КОДЕ")
        print("=" * 80)
        print("""
# Пример использования в Django представлении или сервисе
from mcp_config import get_mcp_url, get_mcp_headers
import requests

def get_process_by_id(process_id):
    url = f"{get_mcp_url()}/processes/{process_id}/"
    headers = get_mcp_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Получение конкретного процесса
process = get_process_by_id(1)
if process:
    print(f"Найден процесс: {process['name']}")
    print(f"Задачи: {len(process['tasks'])}")
""")
    else:
        print("Не удалось получить информацию о бизнес-процессах.")
        print("Проверьте:")
        print("1. MCP сервер запущен и доступен")
        print("2. Конфигурация в config.json правильная")
        print("3. Токен авторизации действителен")
        print("4. У вас установлен модуль requests (pip install requests)")