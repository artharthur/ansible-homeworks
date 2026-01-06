# Ansible Collection: my_own_namespace.yandex_cloud_elk

Ansible collection для создания текстовых файлов. Домашнее задание Netology.

## Установка
```bash
ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz
```

## Содержимое

### Модули

- `my_own_module` — создаёт текстовый файл с указанным содержимым

### Роли

- `create_file` — роль-обёртка для модуля my_own_module

## Использование

### Модуль напрямую
```yaml
- name: Create file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/test.txt
    content: "Hello, World!"
```

### Через роль
```yaml
- hosts: localhost
  roles:
    - role: my_own_namespace.yandex_cloud_elk.create_file
      file_path: /tmp/test.txt
      file_content: "Hello, World!"
```

## Параметры модуля

| Параметр | Обязательный | Описание |
|----------|--------------|----------|
| path     | да           | Путь к файлу |
| content  | да           | Содержимое файла |

## Лицензия

GPL-3.0-or-later

## Автор

Arthur (@artharthur)
