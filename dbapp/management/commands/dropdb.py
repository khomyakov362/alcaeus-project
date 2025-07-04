from django.core.management import BaseCommand
import pyodbc
from config.settings import USER, PASSWORD, HOST, DRIVER, PAD_DATABASE, DATABASE

class Command(BaseCommand):

    help = """Drops the current database. The caller will be asked to provide the name
of the current database as user input to confirm."""

    def handle(self, *args, **kwargs):
        connection_string = f'''DRIVER={DRIVER};SERVER={HOST};DATABASE={PAD_DATABASE};UID={USER};PWD={PASSWORD}'''
    
        try:
            conn = pyodbc.connect(connection_string)
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            user_input = input("Are you sure you want to drop the database?\n"
                               "Enter the name of the current database to confirm: ")
            if user_input != DATABASE:
                print("The name of the database has not been given.\n"
                      "The database will not be dropped.")
                return

            conn.autocommit = True
            try:
                conn.execute(fr'DROP DATABASE {DATABASE};')
            except pyodbc.ProgrammingError as ex:
                print(ex)
            else:
                print(f'The databse {DATABASE} has been dropped.')