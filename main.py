import sqlite3
import pickle

# Load the dictionary from the file


def load_courses():
    with open('courses.pkl', 'rb') as f:
        return pickle.load(f)

# Create a SQLite database connection


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Create a table for the courses


def create_table(conn):
    try:
        sql_create_courses_table = """CREATE TABLE IF NOT EXISTS courses (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name TEXT NOT NULL,
                                        link TEXT NOT NULL
                                    );"""
        cursor = conn.cursor()
        cursor.execute(sql_create_courses_table)
    except sqlite3.Error as e:
        print(e)

# Insert data into the table


def insert_courses(conn, courses):
    sql_insert_course = """INSERT INTO courses (name, link) VALUES (?, ?)"""
    cursor = conn.cursor()
    for course, link in courses.items():
        cursor.execute(sql_insert_course, (course, link))
    conn.commit()


def main():
    database = "courses.db"

    # Load courses dictionary
    courses = load_courses()

    # Create a database connection
    conn = create_connection(database)

    # Create table and insert data
    if conn:
        create_table(conn)
        insert_courses(conn, courses)
        conn.close()
        print("Courses have been successfully inserted into the database.")


if __name__ == '__main__':
    main()


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def search_courses(conn, keyword):
    keyword = f"%{keyword.lower()}%"
    sql_search = """SELECT name, link FROM courses WHERE LOWER(name) LIKE ?"""
    cursor = conn.cursor()
    cursor.execute(sql_search, (keyword,))
    return cursor.fetchall()


def search_keyword(keyword):
    database = "courses.db"
    conn = create_connection(database)
    results = search_courses(conn, keyword)
    conn.close()
    if results:
        response = "\n\n".join(
            [f"**{name}**: [{link}]({link})" for name, link in results])
        return f'**Found the following courses for "{keyword}":**\n\n{response}'
    else:
        return f'No courses found for "{keyword}".'


# Example usage:
print(search_keyword("python"))
