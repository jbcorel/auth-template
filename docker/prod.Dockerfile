# Python образ с предустановленным uv
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

# Размещение проекта в `/app`- директории
WORKDIR /app

# Установка сторонних зависимостей
RUN apt update \
    && apt install media-types procps --yes \
    && apt clean && apt autoclean && apt autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

# Установка python-зависимостей
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --compile-bytecode --locked --no-cache --no-install-project --no-dev
ENV PATH="/app/.venv/bin:$PATH"

# Запуск приложения
COPY ./src/server ./server
ARG SERVICE_VERSION
ENV SERVICE_VERSION=$SERVICE_VERSION
ENTRYPOINT alembic -c ./server/alembic.ini upgrade head \
    & python -m server.main
