# Структура файлов данных

## ratings.csv

- `user_id` (int) - идентификатор пользователя
- `movie_id` (int) - идентификатор фильма
- `rating` (float) - рейтинг фильма
- `timestamp` (int) - время создания записи в формате Unix

## movies.csv

- `movieId` (integer) - идентификатор фильма
- `title` (string) - название фильма с годом выпуска в скобках
- `genres` (string) - жанры фильма, разделенные символом `|`

## tags.csv

- `userId` (integer) - идентификатор пользователя
- `movieId` (integer) - идентификатор фильма
- `tag` (string) - тег фильма, поставленный пользователем
- `timestamp` (int) - время создания записи в формате Unix

## users.txt

- `userId` (integer) - идентификатор пользователя
- `name` (string) - полное имя пользователя
- `email` (string) - электронная почта
- `gender` (string) - пол
- `registration_date` (date) - дата регистрации в формате YYYY-MM-DD
- `occupation` (string) - профессия пользователя
