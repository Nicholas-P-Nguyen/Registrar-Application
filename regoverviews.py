import contextlib
import sqlite3
import argparse
import sys

DATABASE_URL = 'file:reg.sqlite?mode=rw'

def main():
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                parser = argparse.ArgumentParser(description='Registrar application: show overviews of classes')
                parser.add_argument('-d', type=str, metavar='dept', help='show only those classes whose department contains dept')
                parser.add_argument('-n', type=str, metavar='num', help='show only those classes whose course number contains num')
                parser.add_argument('-a', type=str, metavar='area', help='show only those classes whose distrib area contains area')
                parser.add_argument('-t', type=str, metavar='title', help='show only those classes whose course title contains title')
                args = parser.parse_args()

                if args.d:
                    stmt_str = "SELECT classid, dept, coursenum, area, title "
                    stmt_str += "FROM classes, crosslistings, courses "
                    stmt_str += "WHERE dept = ? AND courses.courseid = classes.courseid AND courses.courseid = crosslistings.courseid"
                    cursor.execute(stmt_str, [args.d])

                    table = cursor.fetchall()
                    print(f"{'ClssId':<6} {'Dept':<4} {'CrsNum':<6} {'Area':<4} {'Title':<5}")
                    print(f"{'-' * 6} {'-' * 4} {'-' * 6} {'-' * 4} {'-' * 5}")
                    for row in table:
                        line = f"{row[0]:>6} {row[1]:>4} {row[2]:>6} {row[3]:>4} {row[4]:<49}"
                        while len(line) > 73:
                            break_index = line.rfind(' ', 0, 74)
                            print(line[:break_index])
                            line = ' ' * 24 + line[break_index + 1:]
                        print(line)

                elif args.n:
                    stmt_str = "SELECT classid, dept, coursenum, area, title "
                    stmt_str += "FROM classes, crosslistings, courses "
                    stmt_str += "WHERE coursenum LIKE ? AND courses.courseid = classes.courseid AND courses.courseid = crosslistings.courseid"
                    cursor.execute(stmt_str, [args.n + '%'])

                    table = cursor.fetchall()
                    print('ClsId Dept CrsNum Area Title')
                    print('----- ---- ------ ---- -----')
                    for i, row in enumerate(table):
                        print(str(i), str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
                elif args.a:
                    stmt_str = "SELECT classid, dept, coursenum, area, title "
                    stmt_str += "FROM classes, crosslistings, courses "
                    stmt_str += "WHERE area LIKE ? AND courses.courseid = classes.courseid AND courses.courseid = crosslistings.courseid"
                    cursor.execute(stmt_str, [args.a + '%'])

                    table = cursor.fetchall()
                    print('ClsId Dept CrsNum Area Title')
                    print('----- ---- ------ ---- -----')
                    for i, row in enumerate(table):
                        print(str(i), str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
                elif args.t:
                    stmt_str = "SELECT classid, dept, coursenum, area, title "
                    stmt_str += "FROM classes, crosslistings, courses "
                    stmt_str += "WHERE title LIKE ? AND courses.courseid = classes.courseid AND courses.courseid = crosslistings.courseid"
                    cursor.execute(stmt_str, ['%' + args.t + '%'])

                    table = cursor.fetchall()
                    print('ClsId Dept CrsNum Area Title')
                    print('----- ---- ------ ---- -----')
                    for i, row in enumerate(table):
                        print(str(i), str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))
                else:
                    stmt_str = "SELECT classid, dept, coursenum, area, title "
                    stmt_str += "FROM classes, crosslistings, courses "
                    stmt_str += "WHERE courses.courseid = classes.courseid AND courses.courseid = crosslistings.courseid"
                    cursor.execute(stmt_str)

                    table = cursor.fetchall()
                    print('ClsId Dept CrsNum Area Title')
                    print('----- ---- ------ ---- -----')
                    for i, row in enumerate(table):
                        print(str(i), str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]))




    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
