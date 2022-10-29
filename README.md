# shortener_v2

## Quick start

### To start:

```bash
docker-compose up -d --build
```

### Run tests:

```bash
docker-compose exec shortener_app pytest .
```
## Repositirity structure

```bash
url_shortener_v2
├── app
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── db.py
│   │   └── models.py
│   ├── router
│   │   ├──api_v1
│   │   │   ├── __init__.py
│   │   │   └── endpoints.py
│   │   └── __init__.py
│   ├── shortener_url
│   │   ├── tests
│   │   │   ├── data
│   │   │   │   └── data.json
│   │   │   ├── __init__.py
│   │   │   └── tests.py
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── crud.py
│   │   ├── dependencies.py
│   │   └── models.py
│   ├── __init__.py
│   ├── conftest.py
│   └── main.py
├── migrations
│   ├── versions
│   │    └── 0001_89d72c1f9a9c_urls.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── postgres_test_db
│   └── init.sql
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── README.md
└── reuirements.txt
```
