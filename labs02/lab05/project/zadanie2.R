# Лабораторная работа №5
# Задание 2 - Функциональное программирование
# Описание функций семейства map_* пакета purrr

# Установка и подключение пакета purrr
if (!require("purrr", quietly = TRUE)) {
  install.packages("purrr")
}
library(purrr)

cat("=== ОПИСАНИЕ ФУНКЦИЙ СЕМЕЙСТВА map_* ===\n\n")

# 1. map() - базовая функция, возвращает список
cat("1. map(.x, .f, ...)\n")
cat("   Описание: Применяет функцию .f к каждому элементу .x, возвращает список\n")
cat("   Пример:\n")
test_list <- list(1:5, 6:10, 11:15)
result_map <- map(test_list, ~ mean(.x))
print(result_map)
cat("\n")

# 2. map_lgl() - возвращает логический вектор
cat("2. map_lgl(.x, .f, ...)\n")
cat("   Описание: Применяет функцию .f к каждому элементу .x, возвращает логический вектор\n")
cat("   Пример:\n")
result_map_lgl <- map_lgl(test_list, ~ mean(.x) > 5)
print(result_map_lgl)
cat("\n")

# 3. map_int() - возвращает целочисленный вектор
cat("3. map_int(.x, .f, ...)\n")
cat("   Описание: Применяет функцию .f к каждому элементу .x, возвращает целочисленный вектор\n")
cat("   Пример:\n")
result_map_int <- map_int(test_list, ~ length(.x))
print(result_map_int)
cat("\n")

# 4. map_dbl() - возвращает числовой вектор (double)
cat("4. map_dbl(.x, .f, ...)\n")
cat("   Описание: Применяет функцию .f к каждому элементу .x, возвращает числовой вектор (double)\n")
cat("   Пример:\n")
result_map_dbl <- map_dbl(test_list, ~ mean(.x))
print(result_map_dbl)
cat("\n")

# 5. map_chr() - возвращает символьный вектор
cat("5. map_chr(.x, .f, ...)\n")
cat("   Описание: Применяет функцию .f к каждому элементу .x, возвращает символьный вектор\n")
cat("   Пример:\n")
test_chr_list <- list("apple", "banana", "cherry")
result_map_chr <- map_chr(test_chr_list, ~ toupper(.x))
print(result_map_chr)
cat("\n")

# 6. map_dfr() - возвращает data.frame, объединяя строки
cat("6. map_dfr(.x, .f, ..., .id = NULL)\n")
cat("   Описание: Применяет функцию .f к каждому элементу .x, возвращает data.frame, объединяя результаты по строкам\n")
cat("   Пример:\n")
test_df_list <- list(
  data.frame(x = 1:3, y = 4:6),
  data.frame(x = 7:9, y = 10:12)
)
result_map_dfr <- map_dfr(test_df_list, ~ .x)
print(result_map_dfr)
cat("\n")

# 7. map_dfc() - возвращает data.frame, объединяя столбцы
cat("7. map_dfc(.x, .f, ...)\n")
cat("   Описание: Применяет функцию .f к каждому элементу .x, возвращает data.frame, объединяя результаты по столбцам\n")
cat("   Пример:\n")
test_col_list <- list(a = 1:3, b = 4:6, c = 7:9)
result_map_dfc <- map_dfc(test_col_list, ~ data.frame(.x))
print(result_map_dfc)
cat("\n")

# 8. map_if() - применяет функцию только к элементам, удовлетворяющим условию
cat("8. map_if(.x, .p, .f, ...)\n")
cat("   Описание: Применяет функцию .f только к элементам .x, которые удовлетворяют предикату .p\n")
cat("   Пример:\n")
mixed_list <- list(1:3, "text", 4:6, "another")
result_map_if <- map_if(mixed_list, is.numeric, ~ sum(.x))
print(result_map_if)
cat("\n")

# 9. map_at() - применяет функцию только к элементам по указанным индексам
cat("9. map_at(.x, .at, .f, ...)\n")
cat("   Описание: Применяет функцию .f только к элементам .x по указанным индексам .at\n")
cat("   Пример:\n")
named_list <- list(a = 1:3, b = 4:6, c = 7:9, d = 10:12)
result_map_at <- map_at(named_list, c("a", "c"), ~ sum(.x))
print(result_map_at)
cat("\n")

# 10. walk() - применяет функцию для побочных эффектов, возвращает исходный объект
cat("10. walk(.x, .f, ...)\n")
cat("    Описание: Применяет функцию .f к каждому элементу .x для побочных эффектов (например, печать), возвращает исходный .x\n")
cat("    Пример:\n")
walk(test_list, ~ cat("Сумма:", sum(.x), "\n"))
cat("\n")

# Примеры с данными из пакета datasets
cat("=== ПРИМЕРЫ С ДАННЫМИ ИЗ ПАКЕТА datasets ===\n\n")

# Использование данных mtcars
cat("Пример с данными mtcars:\n")
mtcars_list <- as.list(mtcars[1:5, 1:3])
cat("Средние значения столбцов:\n")
mtcars_means <- map_dbl(mtcars_list, ~ mean(.x))
print(mtcars_means)
cat("\n")

# Использование данных iris
cat("Пример с данными iris:\n")
iris_list <- as.list(iris[1:4])
cat("Средние значения столбцов:\n")
iris_means <- map_dbl(iris_list, ~ mean(.x))
print(iris_means)
cat("\n")

cat("Максимальные значения столбцов:\n")
iris_max <- map_dbl(iris_list, ~ max(.x))
print(iris_max)

