# Here custom commands for the project are described

All the commands below are called with py manage.py \<command\> \[arguments\].

Commands are given by applications.

## Users

### ccsu

Command to Create Super User. Creates admin user inside the database with email,
username and password provided in the .env file.

## DBapp

### ccdb

Command to create database with the name given in the .env file,
the database has default settings for an MSSQL database.
The command is given from the pad database set in .env.

### dropdb

Drops the current database. The caller will be asked to provide the name
of the current database as user input to confirm.

### setupdb

Sets up a fresh database for the project;
is the equivalent of running the following commands:

```bash
    py manage.py ccdb
    py manage.py makemigrations <for each app>
    py manage.py migrate
    py manage.py ccsu
    py manage.py clonerepo
    py manage.py loadbooks
```

## Books

### clonerepo

The command clones the repository from settings.BOOKS_REPO 
and puts it into settings.TEMP_FOLDER. 
If the folder is not empty, its contents will be deleted;
if it is not present, it will be created.

The command does the equivalent of 
```bash
    git clone --depth 1 <BOOKS_REPO> <TEMP_FOLDER\
```

### deltemp

Deletes temporary files at settings.TEMP_FOLDER.

### loadbooks

Loads all the books from the repository data directory into the database.
Does not check, if the books are already there. The same book can be loaded many times.
