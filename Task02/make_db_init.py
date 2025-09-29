import csv
import re
import os

def escape_sql_string(value):
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"

def extract_year_from_title(title):
    match = re.search(r"\((\d{4})\)$", title.strip())
    if match:
        year = int(match.group(1))
        clean_title = title[: match.start()].strip()
        return clean_title, year
    else:
        return title, None

def create_tables_sql():
    sql = []
    tables = ["users", "movies", "ratings", "tags"]
    for table in tables:
        sql.append(f"DROP TABLE IF EXISTS {table};")
    sql.append("")

    sql.append("""CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER,
    genres TEXT
);""")

    sql.append("")

    sql.append("""CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    rating REAL,
    timestamp INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);""")

    sql.append("")

    sql.append("""CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    tag TEXT,
    timestamp INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);""")

    sql.append("")

    sql.append("""CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    gender TEXT,
    register_date DATE,
    occupation TEXT
);""")

    sql.append("")

    return "\n".join(sql)

def read_movies_csv():
    movies = []
    with open("movies.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) >= 3:
                movie_id, title_with_year, genres = row[0], row[1], row[2]
                title, year = extract_year_from_title(title_with_year)
                movies.append((movie_id, title, year, genres))
    return movies

def read_ratings_csv():
    ratings = []
    with open("ratings.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) >= 4:
                userId, movieId, rating, timestamp = row[0], row[1], row[2], row[3]
                ratings.append((userId, movieId, rating, timestamp))
    return ratings

def read_tags_csv():
    tags = []
    with open("tags.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) >= 4:
                userId, movieId, tag, timestamp = row[0], row[1], row[2], row[3]
                tags.append((userId, movieId, tag, timestamp))
    return tags

def read_users_txt():
    users = []
    with open("users.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("|")
                if len(parts) >= 6:
                    user_id, name, email, gender, register_date, occupation = parts[:6]
                    users.append(
                        (user_id, name, email, gender, register_date, occupation)
                    )
    return users

def generate_insert_statements(table_name, data, columns):
    if not data:
        return ""

    sql = []

    batch_size = 100
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]

        values_list = []
        for row in batch:
            escaped_values = []
            for value in row:
                if value == "" or value is None:
                    escaped_values.append("NULL")
                elif isinstance(value, (int, float)) or (
                    isinstance(value, str)
                    and value.replace(".", "").replace("-", "").isdigit()
                ):
                    escaped_values.append(str(value))
                else:
                    escaped_values.append(escape_sql_string(value))
            values_list.append(f"({', '.join(escaped_values)})")

        column_names = ", ".join(columns)
        values_str = ",\n    ".join(values_list)
        sql.append(f"INSERT INTO {table_name} ({column_names}) VALUES")
        sql.append(f"    {values_str};")
        sql.append("")

    return "\n".join(sql)

def main():
    movies_data = read_movies_csv()
    ratings_data = read_ratings_csv()
    tags_data = read_tags_csv()
    users_data = read_users_txt()

    sql_content = []

    sql_content.append(create_tables_sql())

    sql_content.append(
        generate_insert_statements(
            "movies", movies_data, ["id", "title", "year", "genres"]
        )
    )
    sql_content.append(
        generate_insert_statements(
            "users",
            users_data,
            ["id", "name", "email", "gender", "register_date", "occupation"],
        )
    )
    sql_content.append(
        generate_insert_statements(
            "ratings", ratings_data, ["user_id", "movie_id", "rating", "timestamp"]
        )
    )
    sql_content.append(
        generate_insert_statements(
            "tags", tags_data, ["user_id", "movie_id", "tag", "timestamp"]
        )
    )

    output_file = "db_init.sql"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_content))

    file_size = os.path.getsize(output_file)

if __name__ == "__main__":
    main()
