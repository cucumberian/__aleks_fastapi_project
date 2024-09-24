# Fastapi Project

## docker-compose

1. Создать в корне `.env` файл с переменными окружения:

    ```shell
    DB_USER=postgres
    DB_PASS=_random_password_1815u123nbsdf24
    DB_NAME=al_test
    DB_SCHEMA=recommendation
    HASH_TOKEN=_RANDOM_SALT_17uiqkj4131
    CIPHER_TYPE=SH256
    ALGORITHM=HS256

    PGADMIN_DEFAULT_EMAIL=admin@admin.email
    PGADMIN_DEFAULT_PASSWORD=default_pgadmin_password
    ```

2. Запустить docker-compose:

    ```shell
    docker-compose up -d
    ```

## Тесты pytest

Перед запуском тестов из директории `./src` выполнить команду `export PYTHONPATH=$(pwd)`

### Запуск тестов

```sh
pytest
```
