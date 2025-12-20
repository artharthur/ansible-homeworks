# Домашнее задание к занятию 1 «Введение в Ansible»

---

## Подготовка

Ansible установлен на macOS. Для тестов подняты 2 LXC контейнера на Proxmox:
- **210** (ansible-test-1): 192.168.1.68
- **211** (ansible-test-2): 192.168.1.71

Доступ через SSH с мака через ProxyJump (pve 192.168.1.83).

---

## Задание 1

Запустил playbook на test.yml:
```bash
ansible-playbook -i inventory/test.yml site.yml
```

Значение `some_fact` для localhost: **12**

![Test Run](screenshots/01-test-run.png)

---

## Задание 2

Нашёл переменную в `group_vars/all/examp.yml`, поменял значение с `12` на `"all default fact"`.

После изменения playbook выводит новое значение:

![Changed Fact](screenshots/02-changed-fact.png)

---

## Задание 3

Создал `inventory/prod.yml` с двумя группами (deb и el) для контейнеров в Proxmox. Проверил подключение:
```bash
ansible -i inventory/prod.yml all -m ping
```

Оба хоста доступны:

![Prod Ping](screenshots/03-prod-ping.png)

---

## Задание 4

Запустил playbook на prod.yml:
```bash
ansible-playbook -i inventory/prod.yml site.yml
```

Оба хоста показали `some_fact`: `"all default fact"` (используют переменную из group_vars/all).

![Prod Run](screenshots/04-prod-run.png)

---

## Задание 5

Создал отдельные файлы переменных:
- `group_vars/deb/examp.yml` → `some_fact: "deb default fact"`
- `group_vars/el/examp.yml` → `some_fact: "el default fact"`

![Group Vars Structure](screenshots/05-group-vars-structure.png)

---

## Задание 6

Запустил playbook снова. Каждая группа получила своё значение:
- ansible-test-1 (deb): `"deb default fact"`
- ansible-test-2 (el): `"el default fact"`

![Prod Group Vars](screenshots/06-prod-group-vars.png)

---

## Задание 7

Зашифровал файлы переменных паролем `netology`:
```bash
ansible-vault encrypt group_vars/deb/examp.yml
ansible-vault encrypt group_vars/el/examp.yml
```

Файлы теперь зашифрованы:

![Vault Encrypted](screenshots/07-vault-encrypted.png)

---

## Задание 8

Запустил playbook с запросом пароля vault:
```bash
ansible-playbook -i inventory/prod.yml site.yml --ask-vault-pass
```

Playbook расшифровал переменные и вывел правильные значения для deb и el групп.

![Vault Playbook Run](screenshots/08-vault-playbook-run.png)

---

## Задание 9

Посмотрел список плагинов подключения:
```bash
ansible-doc -t connection -l
```

Для работы на control node используется плагин `ansible.builtin.local` — выполняет команды локально без SSH.

![Connection Local Doc](screenshots/09-connection-local-doc.png)

---

## Задание 10

Добавил в `inventory/prod.yml` группу `local` с localhost и создал `group_vars/local/examp.yml` со значением `"local default fact"`.

![Local Group Added](screenshots/10-local-group-added.png)

---

## Задание 11

Финальный запуск playbook с vault:
```bash
ansible-playbook -i inventory/prod.yml site.yml --ask-vault-pass
```

Все три группы вывели корректные значения:
- localhost (local): `"local default fact"`
- ansible-test-1 (deb): `"deb default fact"`
- ansible-test-2 (el): `"el default fact"`

![Final Playbook Run](screenshots/11-final-playbook-run.png)

---

## Ответы на вопросы

**Где расположен файл с переменной `some_fact`?**

В `group_vars/all/examp.yml` — для всех хостов.
Плюс создал отдельные файлы для каждой группы: deb, el, local.

**Какой плагин используется для работы на control node?**

`ansible.builtin.local` — для выполнения команд локально на машине где запущен Ansible.

**Зачем нужен ansible-vault?**

Для шифрования секретов (пароли, токены) чтобы их можно было безопасно хранить в git.

---
