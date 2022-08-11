# crehana

### Start Application

```python
uvicorn src.main:app --reload
```

http://127.0.0.1:8000/items/5?q=holis

## Run Application

### Requirements

```python
python >= 3.9
pipenv instalado
```


### Create Migrations

```bash
alembic init --template generic ./scripts
alembic revision --autogenerate -m "create posts and comments models"
```

### Applying to DB
```bash
alembic upgrade heads

alembic upgrade ff0610ae2eb2
alembic upgrade 9338a9bec1e1
```

### Handle Data iun DB Via Command Line

```python
>>> from src.db import models
>>> from src.db.database import SessionLocal

>>> db = SessionLocal()
>>> db.query(models.Comment).filter(models.Comment.id > 0).delete()
>>> db.query(models.Post).filter(models.Post.id > 0).delete()
>>> db.commit()
```