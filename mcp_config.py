"""
Конфигурация MCP сервера для тестирования веб-приложения.

Этот модуль предоставляет доступ к конфигурации MCP сервера.
"""

import json
import os

# Путь к файлу конфигурации
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    """
    Загружает конфигурацию MCP сервера из файла config.json.
    
    Returns:
        dict: Конфигурация MCP сервера
    """
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Конфигурационный файл {CONFIG_FILE} не найден")
    except json.JSONDecodeError:
        raise ValueError(f"Ошибка чтения конфигурационного файла {CONFIG_FILE}")

def get_mcp_config():
    """
    Возвращает конфигурацию MCP сервера.
    
    Returns:
        dict: Конфигурация MCP сервера
    """
    config = load_config()
    return config.get('pdm', {})

def get_mcp_url():
    """
    Возвращает URL MCP сервера.
    
    Returns:
        str: URL MCP сервера
    """
    mcp_config = get_mcp_config()
    return mcp_config.get('url', 'http://localhost:8001/mcp')

def get_mcp_headers():
    """
    Возвращает заголовки для запросов к MCP серверу.
    
    Returns:
        dict: Заголовки для запросов
    """
    mcp_config = get_mcp_config()
    return mcp_config.get('headers', {})

# Пример использования
if __name__ == '__main__':
    try:
        config = get_mcp_config()
        print("Конфигурация MCP сервера:")
        print(f"URL: {get_mcp_url()}")
        print(f"Заголовки: {get_mcp_headers()}")
    except Exception as e:
        print(f"Ошибка: {e}")