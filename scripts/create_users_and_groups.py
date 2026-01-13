"""
Скрипт для создания пользователей и групп для бизнес-процесса "Обработка заявки".

Выполните этот скрипт через Django shell на сервере:
python manage.py shell < scripts/create_users_and_groups.py

Или в интерактивном режиме:
python manage.py shell
>>> exec(open('scripts/create_users_and_groups.py').read())
"""

from django.contrib.auth.models import User, Group
from django.db import transaction

# Создаем группы (роли)
GROUPS = [
    {
        'name': 'Создатели заявок',
        'description': 'Группа пользователей, которые создают заявки'
    },
    {
        'name': 'Рассматривающие заявки',
        'description': 'Группа пользователей, которые рассматривают заявки'
    },
    {
        'name': 'Утверждающие заявки',
        'description': 'Группа пользователей, которые утверждают заявки'
    }
]

# Создаем пользователей
USERS = [
    {
        'username': 'creator_user',
        'email': 'creator@example.com',
        'first_name': 'Иван',
        'last_name': 'Создатель',
        'password': 'creator123',
        'group': 'Создатели заявок'
    },
    {
        'username': 'reviewer_user',
        'email': 'reviewer@example.com',
        'first_name': 'Петр',
        'last_name': 'Рассматривающий',
        'password': 'reviewer123',
        'group': 'Рассматривающие заявки'
    },
    {
        'username': 'approver_user',
        'email': 'approver@example.com',
        'first_name': 'Сергей',
        'last_name': 'Утверждающий',
        'password': 'approver123',
        'group': 'Утверждающие заявки'
    }
]

@transaction.atomic
def create_groups_and_users():
    """Создает группы и пользователей для бизнес-процесса"""
    
    created_groups = {}
    created_users = {}
    
    # Создаем группы
    print("Создание групп (ролей)...")
    for group_data in GROUPS:
        group, created = Group.objects.get_or_create(name=group_data['name'])
        if created:
            print(f"✓ Создана группа: {group.name} (ID: {group.id})")
        else:
            print(f"→ Группа уже существует: {group.name} (ID: {group.id})")
        created_groups[group_data['name']] = group
    
    print("\nСоздание пользователей...")
    # Создаем пользователей
    for user_data in USERS:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✓ Создан пользователь: {user.username} (ID: {user.id})")
        else:
            print(f"→ Пользователь уже существует: {user.username} (ID: {user.id})")
        
        # Добавляем пользователя в группу
        group = created_groups[user_data['group']]
        user.groups.add(group)
        print(f"  → Пользователь {user.username} добавлен в группу '{group.name}'")
        
        created_users[user_data['username']] = user
    
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ:")
    print("="*60)
    print("\nГруппы (роли):")
    for group_name, group in created_groups.items():
        print(f"  - {group.name} (ID: {group.id})")
    
    print("\nПользователи:")
    for username, user in created_users.items():
        groups = ', '.join([g.name for g in user.groups.all()])
        print(f"  - {user.username} (ID: {user.id}, Группы: {groups})")
    
    print("\n" + "="*60)
    print("ИНФОРМАЦИЯ ДЛЯ НАЗНАЧЕНИЯ ОТВЕТСТВЕННЫХ:")
    print("="*60)
    print("\nДля задачи 'Создание заявки':")
    print(f"  - Пользователь: {created_users['creator_user'].id} ({created_users['creator_user'].username})")
    print(f"  - Группа: {created_groups['Создатели заявок'].id} ({created_groups['Создатели заявок'].name})")
    
    print("\nДля задачи 'Рассмотрение заявки':")
    print(f"  - Пользователь: {created_users['reviewer_user'].id} ({created_users['reviewer_user'].username})")
    print(f"  - Группа: {created_groups['Рассматривающие заявки'].id} ({created_groups['Рассматривающие заявки'].name})")
    
    print("\nДля задачи 'Утверждение заявки':")
    print(f"  - Пользователь: {created_users['approver_user'].id} ({created_users['approver_user'].username})")
    print(f"  - Группа: {created_groups['Утверждающие заявки'].id} ({created_groups['Утверждающие заявки'].name})")
    
    return {
        'groups': created_groups,
        'users': created_users
    }

if __name__ == '__main__':
    result = create_groups_and_users()
    print("\n✓ Готово! Теперь можно назначить ответственных через MCP API.")

