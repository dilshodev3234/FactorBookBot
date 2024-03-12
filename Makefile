extract:
	pybabel extract bot -o locales/messages.pot

init:
	pybabel init -i locales/messages.pot -d locales -D messages -l en
	pybabel init -i locales/messages.pot -d locales -D messages -l uz

update:
	pybabel update -d locales -D messages -i locales/messages.pot

compile:
	pybabel compile -d locales -D messages

upgrade:
	alembic upgrade head

generate:
	alembic revision --autogenerate -m "Added account table"

admin:
	uvicorn admin:app --host=0.0.0.0 --port=8080

#10.10.1.241:8080/admin
