"""
Скрипт для завершения настройки тестового бизнес-процесса "Обработка заявки".

Выполните этот скрипт через Django shell:
python manage.py shell < scripts/setup_test_process.py

Или в интерактивном режиме:
python manage.py shell
>>> exec(open('scripts/setup_test_process.py').read())
"""

from processes.models import BusinessProcess, Task, TaskStartCondition, EntityType

# ID созданных сущностей
BUSINESS_PROCESS_ID = 1
TASK_CREATE_ID = 1
TASK_REVIEW_ID = 2
TASK_APPROVE_ID = 3
ENTITY_TYPE_APPLICATION_ID = 1
ENTITY_TYPE_DECISION_ID = 2
ENTITY_TYPE_APPROVAL_ID = 3

# Получаем бизнес-процесс
try:
    bp = BusinessProcess.objects.get(id=BUSINESS_PROCESS_ID)
    print(f"Найден бизнес-процесс: {bp.name}")
except BusinessProcess.DoesNotExist:
    print(f"Ошибка: Бизнес-процесс с ID {BUSINESS_PROCESS_ID} не найден")
    exit(1)

# 1. Привязываем типы документов к бизнес-процессу
entity_types = EntityType.objects.filter(id__in=[
    ENTITY_TYPE_APPLICATION_ID,
    ENTITY_TYPE_DECISION_ID,
    ENTITY_TYPE_APPROVAL_ID
])
bp.entity_types.set(entity_types)
print(f"✓ Привязано {entity_types.count()} типов документов к бизнес-процессу")

# 2. Привязываем документы к задачам
try:
    task_create = Task.objects.get(id=TASK_CREATE_ID)
    task_create.editable_entity_types.set([EntityType.objects.get(id=ENTITY_TYPE_APPLICATION_ID)])
    print(f"✓ Привязаны документы к задаче '{task_create.name}'")
except Task.DoesNotExist:
    print(f"Ошибка: Задача с ID {TASK_CREATE_ID} не найдена")

try:
    task_review = Task.objects.get(id=TASK_REVIEW_ID)
    task_review.readable_entity_types.set([EntityType.objects.get(id=ENTITY_TYPE_APPLICATION_ID)])
    task_review.editable_entity_types.set([EntityType.objects.get(id=ENTITY_TYPE_DECISION_ID)])
    print(f"✓ Привязаны документы к задаче '{task_review.name}'")
except Task.DoesNotExist:
    print(f"Ошибка: Задача с ID {TASK_REVIEW_ID} не найдена")

try:
    task_approve = Task.objects.get(id=TASK_APPROVE_ID)
    task_approve.readable_entity_types.set([
        EntityType.objects.get(id=ENTITY_TYPE_APPLICATION_ID),
        EntityType.objects.get(id=ENTITY_TYPE_DECISION_ID)
    ])
    task_approve.editable_entity_types.set([EntityType.objects.get(id=ENTITY_TYPE_APPROVAL_ID)])
    print(f"✓ Привязаны документы к задаче '{task_approve.name}'")
except Task.DoesNotExist:
    print(f"Ошибка: Задача с ID {TASK_APPROVE_ID} не найдена")

# 3. Создаем условия запуска задач
try:
    task_review = Task.objects.get(id=TASK_REVIEW_ID)
    # Удаляем существующее условие, если есть
    TaskStartCondition.objects.filter(task=task_review).delete()
    # Создаем новое условие
    condition = TaskStartCondition.objects.create(
        task=task_review,
        condition_tree={
            "assignment_task": "Создание заявки",
            "operator": "equals",
            "value": "completed"
        }
    )
    print(f"✓ Создано условие запуска для задачи '{task_review.name}'")
except Task.DoesNotExist:
    print(f"Ошибка: Задача с ID {TASK_REVIEW_ID} не найдена")

try:
    task_approve = Task.objects.get(id=TASK_APPROVE_ID)
    # Удаляем существующее условие, если есть
    TaskStartCondition.objects.filter(task=task_approve).delete()
    # Создаем новое условие
    condition = TaskStartCondition.objects.create(
        task=task_approve,
        condition_tree={
            "assignment_task": "Рассмотрение заявки",
            "operator": "equals",
            "value": "completed"
        }
    )
    print(f"✓ Создано условие запуска для задачи '{task_approve.name}'")
except Task.DoesNotExist:
    print(f"Ошибка: Задача с ID {TASK_APPROVE_ID} не найдена")

print("\n✓ Настройка бизнес-процесса завершена!")
print(f"Бизнес-процесс '{bp.name}' готов к использованию.")

