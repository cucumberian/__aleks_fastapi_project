# Fastapi Project

## docker-compose

1. Создать в корне `.env` файл с переменными окружения:
    ```shell
    DB_USER=db_user
    DB_PASS=_random_password_1815u123nbsdf24
    DB_NAME=al_test
    DB_SCHEMA=public
    HASH_TOKEN=_RANDOM_SALT_17uiqkj4131
    CIPHER_TYPE=SH256
    ```
2. Запустить docker-compose:
    ```shell
    docker-compose up -d
    ```
