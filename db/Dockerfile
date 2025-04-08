FROM mysql:8.3

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=todo_db
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

COPY init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 3306
