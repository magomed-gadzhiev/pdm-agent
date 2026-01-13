"""
Тестовый скрипт для проверки соединения с MCP сервером.

Этот скрипт демонстрирует, как использовать конфигурацию MCP сервера
для выполнения запросов к API.
"""

import requests
from mcp_config import get_mcp_url, get_mcp_headers

def test_mcp_connection():
    """
    Тестирует соединение с MCP сервером.
    
    Returns:
        bool: True, если соединение успешно, False в противном случае
    """
    try:
        url = get_mcp_url()
        headers = get_mcp_headers()
        
        print(f"Тестирование соединения с MCP сервером: {url}")
        print(f"Используемые заголовки: {headers}")
        
        # Выполняем GET запрос к корневому URL MCP сервера
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Статус код: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Соединение с MCP сервером успешно!")
            print(f"Ответ: {response.text[:200]}...")  # Показываем первые 200 символов
            return True
        else:
            print(f"✗ Ошибка соединения. Статус код: {response.status_code}")
            print(f"Ответ: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Ошибка соединения: {e}")
        return False

def get_processes():
    """
    Получает список бизнес-процессов с MCP сервера.
    
    Returns:
        list: Список бизнес-процессов или None в случае ошибки
    """
    try:
        url = f"{get_mcp_url()}/processes/"
        headers = get_mcp_headers()
        
        print(f"Получение списка бизнес-процессов: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            processes = response.json()
            print(f"✓ Получено {len(processes)} бизнес-процессов")
            return processes
        else:
            print(f"✗ Ошибка получения бизнес-процессов. Статус код: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Ошибка при получении бизнес-процессов: {e}")
        return None

if __name__ == '__main__':
    print("=" * 60)
    print("Тестирование соединения с MCP сервером")
    print("=" * 60)
    
    # Тестируем соединение
    if test_mcp_connection():
        print("\n" + "=" * 60)
        print("Получение данных с MCP сервера")
        print("=" * 60)
        
        # Получаем бизнес-процессы
        processes = get_processes()
        
        if processes:
            print("\nСписок бизнес-процессов:")
            for i, process in enumerate(processes, 1):
                print(f"{i}. {process.get('name', 'Неизвестный процесс')}")
    
    print("\n" + "=" * 60)
    print("Тестирование завершено")
    print("=" * 60)