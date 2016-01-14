#!/bin/bash
export OPENSHIFT_MYSQL_DB_HOST=localhost
export OPENSHIFT_MYSQL_DB_PORT=3306
start_server() {
	python manage.py runserver
}
pyshell() {
	python manage.py shell
}
create_app() {
	python manage.py startapp $1
}
