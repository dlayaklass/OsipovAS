# Лабораторная работа №5
# Задание 1 - Функциональное программирование
# Работа с данными пакета repurrrsive

# Установка и подключение необходимых пакетов
if (!require("purrr", quietly = TRUE)) {
  install.packages("purrr")
}
if (!require("repurrrsive", quietly = TRUE)) {
  install.packages("repurrrsive")
}

library(purrr)
library(repurrrsive)

# Получение данных sw_films
data(sw_films, package = "repurrrsive")

# Создание именованного списка аналогичного по структуре списку sw_films
# Имена элементов списка - названия фильмов
# Используем функциональный стиль с map и set_names

# Извлечение названий фильмов из sw_films
film_names <- map_chr(sw_films, ~ .x$title)

# Создание именованного списка с использованием set_names
# Структура аналогична sw_films, но с именами из названий фильмов
named_films_list <- sw_films %>%
  set_names(film_names)

# Демонстрация работы
cat("=== Исходный список sw_films ===\n")
cat("Количество элементов:", length(sw_films), "\n")
cat("Первые 3 названия фильмов:\n")
print(film_names[1:3])
cat("\n")

cat("=== Созданный именованный список ===\n")
cat("Количество элементов:", length(named_films_list), "\n")
cat("Имена элементов:\n")
print(names(named_films_list))
cat("\n")

# Демонстрация доступа к элементам по имени
cat("=== Доступ к элементам по имени ===\n")
cat("Доступ к фильму 'A New Hope':\n")
if ("A New Hope" %in% names(named_films_list)) {
  a_new_hope <- named_films_list[["A New Hope"]]
  cat("Режиссер:", a_new_hope$director, "\n")
  cat("Дата выхода:", a_new_hope$release_date, "\n")
}

cat("\n=== Доступ к элементам по индексу ===\n")
cat("Первый элемент (по индексу):\n")
first_film <- named_films_list[[1]]
cat("Название:", first_film$title, "\n")
cat("Режиссер:", first_film$director, "\n")

