# Лабораторная работа №4
# Задание 2 - Векторное программирование
# Функция get_negative_values для поиска отрицательных значений в dataframe

get_negative_values <- function(df) {
  # Проверка входных данных
  if (!is.data.frame(df)) {
    stop("Входные данные должны быть dataframe")
  }
  
  # Список для хранения отрицательных значений по переменным
  negative_list <- list()
  
  # Перебор всех столбцов dataframe
  for (col_name in names(df)) {
    # Получение столбца
    column <- df[[col_name]]
    
    # Поиск отрицательных значений (игнорируя NA)
    negative_values <- column[!is.na(column) & column < 0]
    
    # Если есть отрицательные значения, добавляем их в список
    if (length(negative_values) > 0) {
      negative_list[[col_name]] <- negative_values
    }
  }
  
  # Если список пуст, возвращаем NULL
  if (length(negative_list) == 0) {
    return(NULL)
  }
  
  # Проверка: можно ли преобразовать в матрицу
  # (если все векторы имеют одинаковую длину)
  lengths <- sapply(negative_list, length)
  
  if (length(unique(lengths)) == 1 && length(negative_list) > 1) {
    # Все векторы имеют одинаковую длину - преобразуем в матрицу
    return(as.matrix(as.data.frame(negative_list)))
  } else {
    # Векторы разной длины - возвращаем список
    return(negative_list)
  }
}

# Тестирование функции

cat("=== Тест 1 ===\n")
test_data1 <- as.data.frame(list(
  V1 = c(-9.7, -10, -10.5, -7.8, -8.9),
  V2 = c(NA, -10.2, -10.1, -9.3, -12.2),
  V3 = c(NA, NA, -9.3, -10.9, -9.8)
))
result1 <- get_negative_values(test_data1)
print(result1)
cat("\n")

cat("=== Тест 2 ===\n")
test_data2 <- as.data.frame(list(
  V1 = c(NA, 0.5, 0.7, 8),
  V2 = c(-0.3, NA, 2, 1.2),
  V3 = c(2, -1, -5, -1.2)
))
result2 <- get_negative_values(test_data2)
print(result2)
cat("\n")

cat("=== Тест 3 ===\n")
test_data3 <- as.data.frame(list(
  V1 = c(NA, -0.5, -0.7, -8),
  V2 = c(-0.3, NA, -2, -1.2),
  V3 = c(1, 2, 3, NA)
))
result3 <- get_negative_values(test_data3)
print(result3)
cat("\n")

cat("=== Тест 4 (нет отрицательных значений) ===\n")
test_data4 <- as.data.frame(list(
  V1 = c(1, 2, 3),
  V2 = c(4, 5, 6),
  V3 = c(7, 8, 9)
))
result4 <- get_negative_values(test_data4)
print(result4)

