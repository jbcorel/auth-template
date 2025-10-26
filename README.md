Generic шаблон проекта с модулем авторизации и миграциями. Запускается как docker compose up --build -d.

Чтобы прогнать миграции -  docker compose exec app alembic -c ./server/alembic.ini upgrade head

Включает также контейнеры с minio, kafka и redis, чтоб были.