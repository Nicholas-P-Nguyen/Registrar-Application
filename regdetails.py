import contextlib
import sqlite3
import argparse
import sys
import textwrap

DATABASE_URL = 'file:reg.sqlite?mode=rw'

def printCourseDetails(description):
    description_arr = textwrap.wrap(description, width = 72, subsequent_indent= f'{' ' * 3}')
    for d in description_arr:
        print(d)

#-----------------------------------------------------------------------

def getCourseDeptAndNum(classId, cursor):
    stmt_str_dept = "SELECT dept, coursenum "
    stmt_str_dept += "FROM classes, crosslistings "
    stmt_str_dept += "WHERE classid = ? "
    stmt_str_dept += "AND classes.courseid = crosslistings.courseid "
    stmt_str_dept += "ORDER BY dept ASC, coursenum ASC"

    cursor.execute(stmt_str_dept, [classId])
    table = cursor.fetchall()
    for row in table:
        print(f'Dept and Number: {row[0]} {row[1]}')

#-----------------------------------------------------------------------

def getCourseDetails(classId, cursor):
    stmt_str_course = "SELECT area, title, descrip, prereqs "
    stmt_str_course += "FROM classes, courses "
    stmt_str_course += "WHERE classid = ? "
    stmt_str_course += "AND classes.courseid = courses.courseid "

    course_fields = ['Area: ', 'Title: ', 'Description: ', 'Prerequisites: ']
    course_fields_no_space = ['Area:', 'Title:', 'Description:', 'Prerequisites:']
    cursor.execute(stmt_str_course, [classId])
    row = cursor.fetchone()

    for i in range(len(row)):
        if row[i] == "":
            print(course_fields_no_space[i])
        elif len(course_fields[i] + row[i]) > 72:
            printCourseDetails(course_fields[i] + row[i])
        else:
            print(course_fields[i] + row[i]) #maybe comma?

#-----------------------------------------------------------------------

def getCourseProfs(classId, cursor):
    stmt_str_prof = "SELECT profname "
    stmt_str_prof += "FROM classes, coursesprofs, profs "
    stmt_str_prof += "WHERE classid = ? "
    stmt_str_prof += "AND classes.courseid = coursesprofs.courseid "
    stmt_str_prof += "AND coursesprofs.profid = profs.profid "

    cursor.execute(stmt_str_prof, [classId])
    table = cursor.fetchall()

    for row in table:
        print(f'Professor: {row[0]}')

#-----------------------------------------------------------------------

def getClassDetails(classId, cursor):
    stmt_str = "SELECT classid, days, starttime, endtime, bldg, roomnum, courseid "
    stmt_str += "FROM classes WHERE classid = ?"

    cursor.execute(stmt_str, [classId])
    row = cursor.fetchone()

    if row is None:
        print(f"{sys.argv[0]}: no class with classid {classId} exists", file=sys.stderr)
        sys.exit(1)

    print('-------------')
    print('Class Details')
    print('-------------')

    class_fields = ['Class Id:', 'Days:', 'Start time:', 'End time:', 'Building:', 'Room:']
    for i in range(len(class_fields)):
        print(class_fields[i], row[i])

    print('--------------')
    print('Course Details')
    print('--------------')
    print('Course Id:', row[6])

#-----------------------------------------------------------------------

def main():
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                # Help menu
                parser = argparse.ArgumentParser(description='Registrar application: show details about a class')
                parser.add_argument('classid', type=int, help='the id of the class whose details should be shown')
                args = parser.parse_args()

                getClassDetails(args.classid, cursor)
                getCourseDeptAndNum(args.classid, cursor)
                getCourseDetails(args.classid, cursor)
                getCourseProfs(args.classid, cursor)

    except sqlite3.OperationalError as op_ex:
        print(sys.argv[0] + ":", op_ex, file=sys.stderr)
        sys.exit(1)
    except sqlite3.DatabaseError as db_ex:
        print(sys.argv[0] + ":", db_ex, file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()