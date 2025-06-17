# Here custom commands for the project are described

All the commands below are called with py manage.py \<command\> \[arguments\].

Commands are given by applications.

## Users

### ccsu

Command to Create Super User. Creates admin user inside the database with email,
ysername and password provided in the .env file.

## DBapp

### ccdb

Command to create database with the name given in the .env file,
the database has default settings for a MSSQL database.
The command is given from the pad database given in .env.

### dropdb

Drops the current database. The caller will be asked to provide the name
of the current database as user input to confirm.

