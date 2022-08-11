# crehana

### Start Application

```bash
uvicorn src.main:app --reload
```

## Run Application

### Requirements

```bash
python >= 3.9
pipenv, version 2021.11.23
```

### Install Dependecies

```bash
python -m pipenv sync --dev
or 
python -m pipenv sync
or
pipenv sync
```

### PostgresDB Credentials

```
DB User = crehana
DB Password = crehana
DB server = localhost
DB Name = crehana
```

### Run Migrations
```bash
python -m pipenv run alembic upgrade heads
```

Output:

```bash
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> ff0610ae2eb2, create posts and comments models
INFO  [alembic.runtime.migration] Running upgrade ff0610ae2eb2 -> 9338a9bec1e1, adding external id column to posts and comments models
INFO  [alembic.runtime.migration] Running upgrade 9338a9bec1e1 -> e84a82b1f90b, delete posts cascade
INFO  [alembic.runtime.migration] Running upgrade e84a82b1f90b -> 28ced816a423, delete posts cascade
````

### Execute FastAPI Server
```bash
python -m pipenv run uvicorn src.main:app --reload
or
python -m pipenv shell
uvicorn src.main:app --reload
```

Output:

```bash
INFO:     Will watch for changes in these directories: ['D:\\GitHub\\crehana']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13152] using WatchFiles
INFO:     Started server process [1072]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Execute integration from CLI

We can run the integration in two ways: (1) execute the integration via CLI:

```bash
python -m pipenv run python managment.py --help
python -m pipenv run python managment.py --confirm
uvicorn src.main:app --reload
```

Output:

```bash
{'posts_created': 100, 'posts_updated': 0, 'comments_created': 500, 'comments_updated': 0}
```

(2) go to the next endpoint: http://127.0.0.1:8000/call_integration/

### GraphQl Examples

```bash
{
  getPost(postId: 100){
    id
    title
    body
  }
}
```

Output:

```bash
{
  listPosts{
    title
  }
}
```

Output:

```bash
{
  "data": {
    "listPosts": [
      {
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
      },
      {
        "title": "qui est esse"
      },
      {
        "title": "ea molestias quasi exercitationem repellat qui ipsa sit aut"
      },
      {
        "title": "eum et est occaecati"
      },
      {
        "title": "nesciunt quas odio"
      },
...
```

```bash
mutation {
  addPost(title:"I'm a new tittle", body:"I'm a new body"){
    id
    title
    body
    userId
  }
}
```

Output:


```bash
{
  "data": {
    "addPost": {
      "id": 101,
      "title": "I'm a new tittle",
      "body": "I'm a new body",
      "userId": 1
    }
  }
}
```

Output:

```bash
```

Output:
# Documentation

### Create Migrations

```bash
alembic init --template generic ./scripts
alembic revision --autogenerate -m "create posts and comments models"
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