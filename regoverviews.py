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
                parser = argparse.ArgumentParser(description='Registrar application: show overviews of classes')
                parser.add_argument('-d', type=str, metavar='dept', help='show only those classes whose department contains dept')
                parser.add_argument('-n', type=str, metavar='num', help='show only those classes whose course number contains num')
                parser.add_argument('-a', type=str, metavar='area', help='show only those classes whose distrib area contains area')
                parser.add_argument('-t', type=str, metavar='title', help='show only those classes whose course title contains title')
                args = parser.parse_args()

                # Header
                print(f"{'ClssId':<6} {'Dept':<4} {'CrsNum':<6} {'Area':<4} {'Title':<5}")
                print(f"{'-' * 6} {'-' * 4} {'-' * 6} {'-' * 4} {'-' * 5}")

                stmt_str = "SELECT classid, dept, coursenum, area, title "
                stmt_str += "FROM classes, crosslistings, courses "
                stmt_str += "WHERE courses.courseid = classes.courseid AND courses.courseid = crosslistings.courseid "

                if args.n and args.d:
                    stmt_str += "AND coursenum LIKE ? AND dept LIKE ? "
                    stmt_str += "ORDER BY dept ASC, coursenum ASC"
                    cursor.execute(stmt_str, ['%' + args.n + '%', args.d])
                    table = cursor.fetchall()
                    printtable(table)
                elif args.d:
                    stmt_str += "AND dept = ? "
                    stmt_str += "ORDER BY dept ASC, coursenum ASC"
                    cursor.execute(stmt_str, [args.d])
                    table = cursor.fetchall()
                    printtable(table)
                elif args.n:
                    stmt_str += "AND coursenum LIKE ? "
                    stmt_str += "ORDER BY dept ASC, coursenum ASC"
                    cursor.execute(stmt_str, ['%' + args.n + '%'])
                    table = cursor.fetchall()
                    printtable(table)
                elif args.a:
                    stmt_str += "AND area LIKE ? "
                    stmt_str += "ORDER BY dept ASC, coursenum ASC"
                    cursor.execute(stmt_str, [args.a + '%'])
                    table = cursor.fetchall()
                    printtable(table)

                elif args.t:
                    teststr = '\'\\\''
                    stmt_str += f"AND title LIKE ? ESCAPE {teststr} "
                    stmt_str += "ORDER BY dept ASC, coursenum ASC"
                    new_argst = args.t
                    # checks if the characters are in the string, then will insert an
                    ## escape \ if necessary
                    # only loops if the characters are in the string to save mem, otherwise
                    ## will skip over
                    if '_' in args.t or '%' in args.t:
                        new_argst = ''
                        for c in args.t:
                            if c == '_' or c == '%':
                                new_argst += f'\\{c}'
                            else:
                                new_argst += c
                    cursor.execute(stmt_str, ['%' + new_argst + '%'])
                    table = cursor.fetchall()
                    printtable(table)


    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def printtable(table):
    for row in table:
        line = f"{row[0]:>6} {row[1]:>4} {row[2]:>6} {row[3]:>4} {row[4]:<49}"
        while len(line) > 73:
            break_index = line.rfind(' ', 0, 74)
            print(line[:break_index])
            line = ' ' * 24 + line[break_index + 1:]
        print(line)

if __name__ == '__main__':
    main()
