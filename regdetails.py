import contextlib
import sqlite3
import argparse
import sys

DATABASE_URL = 'file:reg.sqlite?mode=rw'

def main():
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                # Help menu
                parser = argparse.ArgumentParser(description='Registrar application: show details about a class')
                parser.add_argument('classid', type=str, help='the id of the class whose details should be shown')
                args = parser.parse_args()

                print('-------------')
                print('Class Details')
                print('-------------')

                stmt_str = "SELECT classid, days, starttime, endtime, bldg, roomnum "
                stmt_str += "FROM classes WHERE classid = ?"

                cursor.execute(stmt_str, [args.classid])
                table = cursor.fetchall()

                for row in table:
                    print('Class Id:', row[0])
                    print('Days:', row[1])
                    print('Start time:', row[2])
                    print('End time:', row[3])
                    print('Building:', row[4])
                    print('Room:', row[5])




    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()