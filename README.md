# Ansible — Домашние задания

Репозиторий с выполненными домашними заданиями по курсу Ansible.

---

## Выполненные модули

### [01-intro](01-intro/) — Введение в Ansible

**Задания:**
- Запуск playbook на test и prod окружениях
- Работа с group_vars и переменными
- Шифрование ansible-vault
- Плагины подключения (local)
- Настройка localhost через local connection

**Окружение:** 
- Control node: macOS
- Managed hosts: 2 LXC контейнера на Proxmox (Ubuntu 22.04)

**[Полный отчёт →](01-intro/README.md)**

---

### [02-playbook](02-playbook/) — Работа с Playbook

**Задания:**
- Установка ClickHouse из репозитория
- Установка Vector из tar.gz архива
- Использование модулей get_url, unarchive, template, file
- Проверка ansible-lint
- Режимы --check и --diff
- Тест на идемпотентность

**Технологии:**
- ClickHouse — аналитическая СУБД для логов
- Vector — агент для сбора и отправки логов

**[Полный отчёт →](02-playbook/README.md)**

---

## Технологии

- Ansible 2.10+
- Proxmox VE
- LXC контейнеры (Ubuntu 22.04)
- SSH с ProxyJump
- ClickHouse
- Vector

---
