# Ansible — Конспект домашних заданий

## Окружение

- **Control node:** macOS (Apple Silicon)
- **Managed hosts:** LXC контейнеры на Proxmox (Ubuntu 22.04)
  - 210 (ansible-test-1): 192.168.1.68 — ClickHouse
  - 211 (ansible-test-2): 192.168.1.71 — Vector
  - 212 (lighthouse-01): 192.168.1.51 — Lighthouse
- **Proxmox:** 192.168.1.83
- **SSH:** Через ProxyJump (macOS → pve → контейнеры)

---

## Репозитории

- **ansible-homeworks:** https://github.com/artharthur/ansible-homeworks
- **vector-role:** https://github.com/artharthur/vector-role
- **lighthouse-role:** https://github.com/artharthur/lighthouse-role

---

## 01-intro: Введение в Ansible

### Ключевые концепции

- **Control node** — машина с которой запускается Ansible (macOS)
- **Managed hosts** — машины которые настраиваем (LXC контейнеры)
- **Inventory** — файл с описанием хостов и групп
- **Playbook** — YAML файл с задачами
- **group_vars** — переменные для групп хостов
- **ansible-vault** — шифрование секретов

### SSH через ProxyJump
```yaml
# inventory/prod.yml
clickhouse:
  hosts:
    clickhouse-01:
      ansible_host: 192.168.1.68
      ansible_user: root
      ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q root@192.168.1.83"'
```

### Ansible Vault
```bash
# Шифрование
ansible-vault encrypt group_vars/deb/examp.yml

# Запуск с vault
ansible-playbook -i inventory/prod.yml site.yml --ask-vault-pass
```

### Тег: `08-ansible-02-playbook`

---

## 02-playbook: Работа с Playbook

### Модули

- `ansible.builtin.apt` — установка пакетов Debian/Ubuntu
- `ansible.builtin.get_url` — скачивание файлов
- `ansible.builtin.unarchive` — распаковка архивов
- `ansible.builtin.template` — Jinja2 шаблоны
- `ansible.builtin.file` — создание файлов/директорий
- `ansible.builtin.systemd` — управление сервисами

### Режимы запуска
```bash
# Проверка синтаксиса
ansible-playbook site.yml --syntax-check

# Линтер
ansible-lint site.yml

# Dry-run (ничего не меняет)
ansible-playbook -i inventory/prod.yml site.yml --check

# С показом изменений
ansible-playbook -i inventory/prod.yml site.yml --diff

# Обычный запуск
ansible-playbook -i inventory/prod.yml site.yml
```

### Идемпотентность

Playbook идемпотентен если повторный запуск показывает `changed=0`.

### Тег: `08-ansible-02-playbook`

---

## 03-lighthouse: Использование Ansible

### Стек

- **ClickHouse** — аналитическая СУБД для логов
- **Vector** — агент сбора логов
- **Lighthouse** — веб-интерфейс для ClickHouse (nginx + статика)

### Структура playbook
```yaml
---
- name: Install Clickhouse
  hosts: clickhouse
  # tasks...

- name: Install Vector
  hosts: vector
  # tasks...

- name: Install Lighthouse
  hosts: lighthouse
  # tasks...
```

### Lighthouse через git
```yaml
- name: Download Lighthouse from git
  ansible.builtin.git:
    repo: "https://github.com/VKCOM/lighthouse.git"
    dest: "/var/www/lighthouse"
    version: master
  when: not lighthouse_git.stat.exists
```

### Тег: `08-ansible-03-yandex`

---

## 04-roles: Работа с roles

### Создание роли
```bash
ansible-galaxy role init vector-role
```

### Структура роли
```
vector-role/
├── defaults/main.yml    # Переменные по умолчанию (можно переопределить)
├── vars/main.yml        # Внутренние переменные
├── tasks/main.yml       # Задачи
├── handlers/main.yml    # Handlers (перезапуск сервисов)
├── templates/           # Jinja2 шаблоны
├── meta/main.yml        # Метаданные роли
└── README.md
```

### requirements.yml
```yaml
---
- src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
  scm: git
  version: "1.13"
  name: clickhouse

- src: git@github.com:artharthur/vector-role.git
  scm: git
  version: "1.0.1"
  name: vector

- src: git@github.com:artharthur/lighthouse-role.git
  scm: git
  version: "1.0.1"
  name: lighthouse
```

### Установка ролей
```bash
ansible-galaxy install -r requirements.yml -p roles
```

### Playbook с ролями
```yaml
---
- name: Install Clickhouse
  hosts: clickhouse
  roles:
    - clickhouse

- name: Install Vector
  hosts: vector
  roles:
    - vector

- name: Install Lighthouse
  hosts: lighthouse
    - lighthouse
```

### Тег: `08-ansible-04-roles`

---

## 05-testing: Тестирование roles

### Molecule

Тестирование Ansible ролей в изолированных контейнерах.

#### Установка
```bash
pip3 install molecule molecule-docker molecule-podman
```

#### Создание сценария
```bash
cd vector-role
molecule init scenario
```

#### Структура molecule
```
molecule/
├── default/
│   ├── molecule.yml      # Конфигурация сценария
│   ├── converge.yml      # Применение роли
│   ├── verify.yml        # Тесты
│   ├── create.yml        # Создание контейнеров
│   └── destroy.yml       # Удаление контейнеров
```

#### molecule.yml для Docker
```yaml
---
driver:
  name: docker

platforms:
  - name: ubuntu2204
    image: ubuntu:22.04
    command: sleep infinity
    privileged: true

provisioner:
  name: ansible
  inventory:
    hosts:
      all:
        hosts:
          ubuntu2204:
            ansible_connection: docker

verifier:
  name: ansible

scenario:
  name: default
  test_sequence:
    - destroy
    - create
    - converge
    - idempotence
    - verify
    - destroy
```

#### verify.yml с assert
```yaml
---
- name: Verify
  hosts: all
  become: true
  tasks:
    - name: Check vector binary exists
      ansible.builtin.stat:
        path: /opt/vector/bin/vector
      register: vector_binary

    - name: Assert vector binary exists
      ansible.builtin.assert:
        that:
          - vector_binary.stat.exists
        fail_msg: "Vector binary not found"
        success_msg: "Vector binary exists"

    - name: Validate vector config syntax
      ansible.builtin.command: /opt/vector/bin/vector validate --no-environment /etc/vector/vector.yml
      register: vector_validate
      changed_when: false

    - name: Assert vector config is valid
      ansible.builtin.assert:
        that:
          - vector_validate.rc == 0
```

#### Запуск тестов
```bash
molecule test                              # Полный цикл
molecule converge                          # Только применить
molecule verify                            # Только тесты
molecule test -s compatibility             # Другой сценарий
molecule destroy                           # Удалить контейнеры
```

### Tox

Автоматизация запуска тестов на разных версиях Python/Ansible.

#### tox.ini
```ini
[tox]
minversion = 1.8
basepython = python3.10
envlist = py310
skipsdist = true

[testenv]
sitepackages = true
passenv = *
setenv =
    LANG = en_US.UTF-8
    LC_ALL = en_US.UTF-8
allowlist_externals =
    molecule
commands =
    {posargs:molecule test -s compatibility --destroy always}
```

#### tox-requirements.txt
```
molecule
molecule_podman
jmespath
ansible-compat
ansible-core
```

#### Запуск
```bash
tox
```

### Проблемы и решения

#### Apple Silicon (ARM) + Docker x86

Molecule на Mac с Apple Silicon работает медленно из-за эмуляции. Tox лучше запускать на x86 машине (Proxmox LXC).

#### Molecule не находит роль
```yaml
# converge.yml — указать путь к роли
- name: Include vector role
  ansible.builtin.include_role:
    name: "{{ lookup('env', 'MOLECULE_PROJECT_DIRECTORY') }}"
```

#### Нет systemd в контейнере
```yaml
# tasks/main.yml — пропускать systemd задачи
- name: Enable and start Vector service
  ansible.builtin.systemd:
    name: vector
    enabled: true
    state: started
  when: ansible_service_mgr == "systemd"
```

### Теги

- **vector-role 1.1.0** — molecule default сценарий
- **vector-role 1.2.0** — tox и compatibility сценарий
- **ansible-homeworks:** `08-ansible-05-testing`

---

## Полезные команды

### Ansible
```bash
# Проверка доступности хостов
ansible -i inventory/prod.yml all -m ping

# Выполнить команду на хосте
ansible -i inventory/prod.yml clickhouse-01 -m shell -a "systemctl status clickhouse-server" -b

# Посмотреть facts хоста
ansible -i inventory/prod.yml clickhouse-01 -m setup
```

### LXC на Proxmox
```bash
# Список контейнеров
pct list

# Войти в контейнер
pct enter 210

# Выполнить команду в контейнере
pct exec 210 -- ip a

# Получить IP по DHCP
pct exec 210 -- dhclient eth0
```

### Git
```bash
# SSH через порт 443 (если 22 заблокирован)
# ~/.ssh/config
Host github.com
  HostName ssh.github.com
  Port 443
  IdentityFile ~/.ssh/id_ed25519
```

---

## Структура проекта
```
~/Netology/ansible_hw1/
├── 01-intro/
│   ├── README.md
│   ├── site.yml
│   ├── inventory/
│   └── group_vars/
├── 02-playbook/
│   ├── README.md
│   └── playbook/
├── 03-lighthouse/
│   ├── README.md
│   └── playbook/
├── 04-roles/
│   ├── README.md
│   └── playbook/
│       ├── roles/
│       │   ├── clickhouse/      # Внешняя роль
│       │   ├── vector/          # git: vector-role
│       │   └── lighthouse/      # git: lighthouse-role
│       └── requirements.yml
├── 05-testing/
│   ├── README.md
│   └── screenshots/
└── README.md
```

---
