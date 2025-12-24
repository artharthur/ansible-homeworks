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

**[Полный отчёт →](02-playbook/README.md)**

---

### [03-lighthouse](03-lighthouse/) — Использование Ansible

**Задания:**
- Установка полного стека: ClickHouse + Vector + Lighthouse
- Настройка nginx для Lighthouse
- Git clone репозитория
- Шаблонизация конфигов
- Проверка идемпотентности

**Технологии:**
- ClickHouse — СУБД для логов
- Vector — агент сбора логов
- Lighthouse — веб-интерфейс для ClickHouse
- Nginx — веб-сервер

**[Полный отчёт →](03-lighthouse/README.md)**

---

## Технологии

- Ansible 2.10+
- Proxmox VE
- LXC контейнеры (Ubuntu 22.04)
- SSH с ProxyJump
- ClickHouse, Vector, Lighthouse, Nginx

---
