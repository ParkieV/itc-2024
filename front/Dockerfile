# Используем официальный образ Node.js 20
FROM node:20 AS base

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем package.json и package-lock.json в контейнер
COPY package.json .

# Устанавливаем зависимости
RUN npm install

# Устанавливаем `serve` для хостинга статических файлов
RUN npm install -g serve

FROM base AS base_with_vue

# Устанавливаем Quasar CLI глобально
RUN npm install -g @quasar/cli


FROM base_with_vue

# Копируем все файлы из текущей директории (где находится Dockerfile) в рабочую директорию контейнера
COPY . .

RUN quasar build

# Команда для запуска сервера
CMD ["serve", "-s", "dist/spa", "-l", "9000"]
