"""
Простой тестовый скрипт для проверки конфигурации MCP сервера.

Этот скрипт проверяет, что конфигурация загружается правильно,
без необходимости устанавливать дополнительные модули.
"""

from mcp_config import get_mcp_config, get_mcp_url, get_mcp_headers

def test_config():
    """
    Тестирует загрузку конфигурации MCP сервера.
    """
    print("=" * 60)
    print("Testing MCP server configuration")
    print("=" * 60)
    
    try:
        # Тестируем загрузку полной конфигурации
        config = get_mcp_config()
        print("[OK] Full configuration loaded successfully:")
        print(f"  {config}")
        
        # Тестируем получение URL
        url = get_mcp_url()
        print(f"\n[OK] MCP server URL: {url}")
        
        # Тестируем получение заголовков
        headers = get_mcp_headers()
        print(f"[OK] Authorization headers:")
        for key, value in headers.items():
            if key.lower() == 'authorization':
                # Маскируем токен для безопасности
                token = value.split()[-1] if ' ' in value else value
                masked_token = token[:10] + '...' + token[-10:] if len(token) > 20 else token
                print(f"  {key}: Bearer {masked_token}")
            else:
                print(f"  {key}: {value}")
        
        # Проверяем, что все необходимые поля присутствуют
        required_fields = ['url', 'headers']
        missing_fields = [field for field in required_fields if field not in config]
        
        if missing_fields:
            print(f"\n[ERROR] Missing required fields: {', '.join(missing_fields)}")
            return False
        
        # Проверяем, что заголовок авторизации присутствует
        if 'Authorization' not in headers:
            print("\n[ERROR] Missing authorization header")
            return False
        
        print("\n" + "=" * 60)
        print("[SUCCESS] All configuration checks passed!")
        print("=" * 60)
        
        print("\nConfiguration is ready to use.")
        print("You can use it in your scripts:")
        print("  from mcp_config import get_mcp_url, get_mcp_headers")
        print("  url = get_mcp_url()")
        print("  headers = get_mcp_headers()")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error loading configuration: {e}")
        return False

if __name__ == '__main__':
    success = test_config()
    exit(0 if success else 1)