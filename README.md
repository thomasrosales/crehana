# crehana

## Start Application

```python
uvicorn src.main:app --reload
```

http://127.0.0.1:8000/items/5?q=holis


## Create Migrations

```bash
alembic init --template generic ./scripts
alembic revision --autogenerate -m "create posts and comments models"
```

### Applying to DB
```bash
alembic upgrade heads
```