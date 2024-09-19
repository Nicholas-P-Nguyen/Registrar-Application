import contextlib
import sqlite3
import argparse
import sys
import textwrap

DATABASE_URL = 'file:reg.sqlite?mode=rw'

def main():
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                # Help menu
                parser = argparse.ArgumentParser(description='Registrar application: show details about a class')
                parser.add_argument('classid', type=str, help='the id of the class whose details should be shown')
                args = parser.parse_args()

                getClassDetails(args.classid, cursor)
                getCourseDetails(args.classid, cursor)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

def getClassDetails(classId, cursor):
    print('-------------')
    print('Class Details')
    print('-------------')

    stmt_str = "SELECT classid, days, starttime, endtime, bldg, roomnum "
    stmt_str += "FROM classes WHERE classid = ?"

    cursor.execute(stmt_str, [classId])
    table = cursor.fetchall()

    for row in table:
        print('Class Id:', row[0])
        print('Days:', row[1])
        print('Start time:', row[2])
        print('End time:', row[3])
        print('Building:', row[4])
        print('Room:', row[5])

def getCourseDetails(classId, cursor):
    print('-------------')
    print('Course Details')
    print('-------------')

    stmt_str = "SELECT classes.courseid, dept, coursenum, area, title, descrip, prereqs, profname "
    stmt_str += "FROM courses, crosslistings, profs, coursesprofs, classes "
    stmt_str += "WHERE classid = ? AND classes.courseid = courses.courseid "
    stmt_str += "AND classes.courseid = crosslistings.courseid AND classes.courseid = coursesprofs.courseid "
    stmt_str += "AND coursesprofs.profid = profs.profid "
    stmt_str += "ORDER BY dept ASC, coursenum ASC"

    cursor.execute(stmt_str, [classId])
    table = cursor.fetchall()

    details = ['Course Id:', 'Department and Number:', 'Area:', 'Title:', 'Description:', 'Prerequisites:' 'Professor:']

    for row in table:
        print('Course Id:', row[0])
        print(f'Department and Number: {row[1]} {row[2]}')
        print('Area:', row[3])
        print('Title:', row[4])
        printDetails('Description:' + row[5])
        print('Prerequisites:', row[6])
        print('Professor:', row[7])

def printDetails(description):
    while len(description) > 73:
        break_index = description.rfind(' ', 0, 74)
        print(description[:break_index])
        description = ' ' * 3 + description[break_index + 1:]
    print(description)



if __name__ == '__main__':
    main()