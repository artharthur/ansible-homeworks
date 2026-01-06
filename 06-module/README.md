# Домашнее задание 6: Создание собственных модулей

## Что сделано

Написал собственный Ansible модуль `my_own_module`, который создаёт текстовый файл на удалённом хосте. Модуль принимает два параметра: `path` (путь к файлу) и `content` (содержимое). Реализована идемпотентность — если файл уже существует с нужным содержимым, модуль ничего не меняет.

Модуль упакован в коллекцию `my_own_namespace.yandex_cloud_elk` вместе с ролью `create_file`, которая является обёрткой над модулем.

## Ссылки

- Репозиторий коллекции: https://github.com/artharthur/my_own_collection
- Архив коллекции: https://github.com/artharthur/my_own_collection/blob/main/my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz

## Скриншоты

- [Шаг 4 — тест модуля локально](screenshots/step4-module-local-test.png)
- [Шаг 6 — проверка идемпотентности](screenshots/step6-playbook-idempotence.png)
- [Шаг 15 — установка коллекции из архива](screenshots/step15-collection-install.png)
- [Шаг 16 — запуск playbook](screenshots/step16-playbook-run.png)
