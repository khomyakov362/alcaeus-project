from django.core.management import BaseCommand, CommandError
import pyodbc
from config.settings import USER, PASSWORD, HOST, DRIVER, PAD_DATABASE, DATABASE

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('database', nargs='+', type=str)
        parser.add_argument('init_or_difer', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        backupdb = kwargs['database'][0]
        init_or_difer = kwargs['init_or_difer'][0]

        if not kwargs:
            raise CommandError('Two arguments must be provided for this command: name of the backup database and backup type.')
        
        if backupdb == DATABASE:
            raise CommandError('The name of the backup database must not be the same as the name of the current database.')
        
        if init_or_difer not in ('init', 'differential'):
            raise CommandError('The seceond argument must be either "init" or "differential."')

        
        connection_string = f'''DRIVER={DRIVER};SERVER={HOST};DATABASE={PAD_DATABASE};UID={USER};PWD={PASSWORD}'''
    
        try:
            conn = pyodbc.connect(connection_string)
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            conn.autocommit = True
            try:
                conn.execute(fr'''BACKUP DATABASE {DATABASE}   
                                    TO {backupdb}   
                                  WITH {init_or_difer};''')

            except pyodbc.ProgrammingError as ex:
                print(ex)
            else:
                print(f'The backup for {DATABASE} named {args[0]} was created with {args[1]}.')

