import contextlib
import sqlite3
import argparse
import sys

DATABASE_URL = 'file:reg.sqlite?mode=rw'
# End of the escape clause -> '\'
ESCAPE = '\'\\\''

def printTable(table):
    for row in table:
        line = f"{row[0]:>5} {row[1]:>4} {row[2]:>6} {row[3]:>4} {row[4]:<}"
        while len(line) > 72:
            break_index = line.rfind(' ', 0, 73)
            print(line[:break_index])
            line = ' ' * 23 + line[break_index + 1:]
        print(line)

#-----------------------------------------------------------------------------------------------------------------------

def getEscapedTitle(title):
    new_title = ''
    for char in title:
        if char == '_' or char == '%':
            new_title += f'\\{char}'
        else:
            new_title += char
    return new_title

#-----------------------------------------------------------------------------------------------------------------------

def processArguments(stmt_str, cursor, dept=None, num=None, area=None, title=None):
    if dept and area and num and title:
        stmt_str += "AND dept LIKE ? AND area LIKE ? AND title LIKE ? AND coursenum LIKE ? "
        stmt_str += "ORDER BY dept ASC, coursenum ASC"

        parameters = [
            dept + '%',
            area + '%',
            '%' + title + '%',
            '%' + num + '%'
        ]

        cursor.execute(stmt_str, parameters)
    elif num and dept:
        stmt_str += "AND coursenum LIKE ? AND dept LIKE ? "
        stmt_str += "ORDER BY dept ASC, coursenum ASC"

        parameters = [
            '%' + num + '%',
            dept + '%'
        ]

        cursor.execute(stmt_str, parameters)
    elif dept:
        stmt_str += "AND dept LIKE ? "
        stmt_str += "ORDER BY dept ASC, coursenum ASC"
        cursor.execute(stmt_str, [dept + '%'])
    elif num:
        stmt_str += "AND coursenum LIKE ? "
        stmt_str += "ORDER BY dept ASC, coursenum ASC"
        cursor.execute(stmt_str, ['%' + num + '%'])
    elif area:
        stmt_str += "AND area LIKE ? "
        stmt_str += "ORDER BY dept ASC, coursenum ASC"
        cursor.execute(stmt_str, [area + '%'])
    elif title:
        stmt_str += f"AND title LIKE ? ESCAPE {ESCAPE} "
        stmt_str += "ORDER BY dept ASC, coursenum ASC"

        if '_' in title or '%' in title:
            new_title = getEscapedTitle(title)
            cursor.execute(stmt_str, ['%' + new_title + '%'])
        else:
            cursor.execute(stmt_str, ['%' + title + '%'])
    else:
        stmt_str += "ORDER BY dept ASC, coursenum ASC"
        cursor.execute(stmt_str)

#-----------------------------------------------------------------------------------------------------------------------

def main():
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                # Help menu
                parser = argparse.ArgumentParser(description='Registrar application: show overviews of classes')
                parser.add_argument('-d', type=str, metavar='dept',
                                    help='show only those classes whose department contains dept')
                parser.add_argument('-n', type=str, metavar='num',
                                    help='show only those classes whose course number contains num')
                parser.add_argument('-a', type=str, metavar='area',
                                    help='show only those classes whose distrib area contains area')
                parser.add_argument('-t', type=str, metavar='title',
                                    help='show only those classes whose course title contains title')
                args = parser.parse_args()

                # Header
                print(f"{'ClsId':<5} {'Dept':<4} {'CrsNum':<6} {'Area':<4} {'Title':<5}")
                print(f"{'-' * 5} {'-' * 4} {'-' * 6} {'-' * 4} {'-' * 5}")

                stmt_str = "SELECT classid, dept, coursenum, area, title "
                stmt_str += "FROM classes, crosslistings, courses "
                stmt_str += "WHERE courses.courseid = classes.courseid AND courses.courseid = crosslistings.courseid "

                processArguments(stmt_str, cursor, args.d, args.n, args.a, args.t)

                table = cursor.fetchall()
                printTable(table)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
