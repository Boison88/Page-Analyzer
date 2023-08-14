## Study project #3 — «Page Analyzer»
[![Actions Status](https://github.com/Boison88/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Boison88/python-project-83/actions)
[![CI](https://github.com/Boison88/python-project-83/actions/workflows/CI.yml/badge.svg)](https://github.com/Boison88/python-project-83/actions/workflows/CI.yml)

This repository was created as part of a [Hexlet study project](https://ru.hexlet.io/programs/python/projects/83).  

*Page Analyzer* this is a full-fledged application based on the Flask framework.
This is a site that analyzes the specified pages for SEO suitability.

### Try the project in work [HERE](https://page-analyzer-3b9q.onrender.com)  

***
### How to install
#### 1. Clone this repository
```
    git clone https://github.com/Boison88/python-project-83
```

#### 2. Change Directory
```
    cd python-project-83
```

#### 3. Create PostgreSQL database
```
    createdb {dbname}
    psql {dbname} < database.sql
```
#### 4. Install Poetry
```
    poetry install
```
#### 5. Create file with name `.env` for environment variables with the following information
```
    DATABASE_URL = postgresql://{your username}:{password}@{host}:{port}/{db name}
    SECRET_KEY = '{your secret key}'
```
#### 6. Use make-command for run
```
    # for dev and local use
    make dev
    
    # for deploy
    make start
```