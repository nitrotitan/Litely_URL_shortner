# Project Title

A url shortner with FastAPI framework.

## Getting Started

This app made with async support, all the APIs and even the sqlite DB is running on Async mode,
might cause some error related to DB connections and Async in that case please dont reach out to me,
im not paid enough :(

### Prerequisites

The things you need before installing the software.

* Basic understanding of FastAPI framework, more on https://fastapi.tiangolo.com/
* Alembic incase you want to change implementation of DB migrations
* For DB querying SQLAlchemy is being used, you can refer more on here https://docs.sqlalchemy.org/en/14/

### Installation

A step by step guide that will tell you how to get the development environment up and running on you local system

```
$ Install all the requirements from requirement.txt file
$ Once all the installation has been completed, setup an virtual env on local
$ Run the file name manage.py, this will create an initialization and migration folder in you directory named as 'migration'
$ Once above steps is completed run the app using command uvicorn command with reload as argument so you dont have run the command again and again in development 
```

## Usage

A few examples of useful commands and/or tasks.

```
$ #To install all requirements do 
$ pip install -r requirement.txt
$ python manage.py # this will setup your migrations
$ uvicorn your_app_name.main:app --reload  # this will run the app and also create a DB named 'shorter-url.db'
```

## Deployment

will add later

### Server

* Live: TBH


### Branches

* Master: main

## Additional Documentation and Acknowledgments

* I'm too tired to add
* please do a bit of research 
* and most important dont bug me, cause as i said im not paid enough
