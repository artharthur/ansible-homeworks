# Ansible — Домашние задания

Репозиторий с выполненными домашними заданиями по курсу Ansible.

---

## Выполненные модули

### [01-intro](01-intro/) — Введение в Ansible

- Запуск playbook на test и prod окружениях
- Работа с group_vars и переменными
- Шифрование ansible-vault
- Плагины подключения (local)

**[Полный отчёт →](01-intro/README.md)**

---

### [02-playbook](02-playbook/) — Работа с Playbook

- Установка ClickHouse из репозитория
- Установка Vector из tar.gz архива
- Использование модулей get_url, unarchive, template, file
- Проверка ansible-lint, --check, --diff

**[Полный отчёт →](02-playbook/README.md)**

---

### [03-lighthouse](03-lighthouse/) — Использование Ansible

- Установка полного стека: ClickHouse + Vector + Lighthouse
- Настройка nginx для Lighthouse
- Git clone репозитория
- Шаблонизация конфигов

**[Полный отчёт →](03-lighthouse/README.md)**

---

### [04-roles](04-roles/) — Работа с roles

- Разбиение playbook на отдельные роли
- Создание ролей vector и lighthouse
- Использование внешней роли clickhouse
- Публикация ролей в отдельных репозиториях

**Репозитории ролей:**
- [vector-role](https://github.com/artharthur/vector-role)
- [lighthouse-role](https://github.com/artharthur/lighthouse-role)

**[Полный отчёт →](04-roles/README.md)**

---

## Технологии

- Ansible 2.10+
- Proxmox VE
- LXC контейнеры (Ubuntu 22.04)
- ClickHouse, Vector, Lighthouse, Nginx

---
