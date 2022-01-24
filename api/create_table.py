import sqlite3


def main():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, unique_name text, name text, first_name text, is_admin bool, password text)"
    )

    connection.commit()
    connection.close()

    return


if __name__ == "__main__":
    main()
