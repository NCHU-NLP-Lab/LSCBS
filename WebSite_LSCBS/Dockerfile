FROM webdevops/php-nginx:7.2-alpine

COPY . /app
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python