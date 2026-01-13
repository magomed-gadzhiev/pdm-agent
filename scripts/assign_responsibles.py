"""
Скрипт для назначения ответственных пользователей и групп для задач бизнес-процесса "Обработка заявки".

Выполните этот скрипт через Django shell на сервере:
python manage.py shell < scripts/assign_responsibles.py

Или в интерактивном режиме:
python manage.py shell
>>> exec(open('scripts/assign_responsibles.py').read())
"""

from processes.models import Task
from django.contrib.auth.models import User, Group

# ID задач
TASK_CREATE_ID = 1  # Создание заявки
TASK_REVIEW_ID = 2   # Рассмотрение заявки
TASK_APPROVE_ID = 3  # Утверждение заявки

# ID пользователей
USER_CREATOR_ID = 2   # creator_user
USER_REVIEWER_ID = 3  # reviewer_user
USER_APPROVER_ID = 4  # approver_user

# ID групп
GROUP_CREATORS_ID = 1    # Создатели заявок
GROUP_REVIEWERS_ID = 2   # Рассматривающие заявки
GROUP_APPROVERS_ID = 3   # Утверждающие заявки

def assign_responsibles():
    """Назначает ответственных пользователей и группы для задач"""
    
    # Задача 1: Создание заявки
    try:
        task_create = Task.objects.get(id=TASK_CREATE_ID)
        user_creator = User.objects.get(id=USER_CREATOR_ID)
        group_creators = Group.objects.get(id=GROUP_CREATORS_ID)
        
        task_create.responsible = user_creator
        task_create.responsible_groups.set([group_creators])
        task_create.save()
        
        print(f"✓ Назначен ответственный для задачи '{task_create.name}':")
        print(f"  - Пользователь: {user_creator.username} (ID: {user_creator.id})")
        print(f"  - Группа: {group_creators.name} (ID: {group_creators.id})")
    except Task.DoesNotExist:
        print(f"Ошибка: Задача с ID {TASK_CREATE_ID} не найдена")
    except User.DoesNotExist:
        print(f"Ошибка: Пользователь с ID {USER_CREATOR_ID} не найден")
    except Group.DoesNotExist:
        print(f"Ошибка: Группа с ID {GROUP_CREATORS_ID} не найдена")
    
    # Задача 2: Рассмотрение заявки
    try:
        task_review = Task.objects.get(id=TASK_REVIEW_ID)
        user_reviewer = User.objects.get(id=USER_REVIEWER_ID)
        group_reviewers = Group.objects.get(id=GROUP_REVIEWERS_ID)
        
        task_review.responsible = user_reviewer
        task_review.responsible_groups.set([group_reviewers])
        task_review.save()
        
        print(f"✓ Назначен ответственный для задачи '{task_review.name}':")
        print(f"  - Пользователь: {user_reviewer.username} (ID: {user_reviewer.id})")
        print(f"  - Группа: {group_reviewers.name} (ID: {group_reviewers.id})")
    except Task.DoesNotExist:
        print(f"Ошибка: Задача с ID {TASK_REVIEW_ID} не найдена")
    except User.DoesNotExist:
        print(f"Ошибка: Пользователь с ID {USER_REVIEWER_ID} не найден")
    except Group.DoesNotExist:
        print(f"Ошибка: Группа с ID {GROUP_REVIEWERS_ID} не найдена")
    
    # Задача 3: Утверждение заявки
    try:
        task_approve = Task.objects.get(id=TASK_APPROVE_ID)
        user_approver = User.objects.get(id=USER_APPROVER_ID)
        group_approvers = Group.objects.get(id=GROUP_APPROVERS_ID)
        
        task_approve.responsible = user_approver
        task_approve.responsible_groups.set([group_approvers])
        task_approve.save()
        
        print(f"✓ Назначен ответственный для задачи '{task_approve.name}':")
        print(f"  - Пользователь: {user_approver.username} (ID: {user_approver.id})")
        print(f"  - Группа: {group_approvers.name} (ID: {group_approvers.id})")
    except Task.DoesNotExist:
        print(f"Ошибка: Задача с ID {TASK_APPROVE_ID} не найдена")
    except User.DoesNotExist:
        print(f"Ошибка: Пользователь с ID {USER_APPROVER_ID} не найден")
    except Group.DoesNotExist:
        print(f"Ошибка: Группа с ID {GROUP_APPROVERS_ID} не найдена")
    
    print("\n" + "="*60)
    print("Проверка назначенных ответственных:")
    print("="*60)
    
    # Проверяем результат
    for task_id, task_name in [
        (TASK_CREATE_ID, "Создание заявки"),
        (TASK_REVIEW_ID, "Рассмотрение заявки"),
        (TASK_APPROVE_ID, "Утверждение заявки")
    ]:
        try:
            task = Task.objects.get(id=task_id)
            responsible = task.responsible
            groups = task.responsible_groups.all()
            
            print(f"\nЗадача: {task_name} (ID: {task_id})")
            if responsible:
                print(f"  Ответственный пользователь: {responsible.username} (ID: {responsible.id})")
            else:
                print(f"  Ответственный пользователь: не назначен")
            
            if groups:
                print(f"  Ответственные группы: {', '.join([g.name for g in groups])}")
            else:
                print(f"  Ответственные группы: не назначены")
        except Task.DoesNotExist:
            print(f"Задача с ID {task_id} не найдена")

if __name__ == '__main__':
    assign_responsibles()
    print("\n✓ Готово!")


