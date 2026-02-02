# Лабораторная работа №3
# Задание 1 - Объектно-ориентированное программирование
# Создание дженерика для вычисления площади фигур

# Создание дженерика get_area
get_area <- function(x, ...) {
  UseMethod("get_area")
}

# Метод по умолчанию
get_area.default <- function(x, ...) {
  return("Невозможно обработать данные. Неизвестный тип фигуры.")
}

# Класс для треугольника
# Вектор должен содержать: [основание, высота]
triangle_area <- function(x) {
  if (length(x) != 2) {
    stop("Для треугольника требуется 2 параметра: основание и высота")
  }
  return(0.5 * x[1] * x[2])
}

# Класс для квадрата
# Вектор должен содержать: [сторона]
square_area <- function(x) {
  if (length(x) != 1) {
    stop("Для квадрата требуется 1 параметр: сторона")
  }
  return(x[1] * x[1])
}

# Класс для прямоугольника
# Вектор должен содержать: [длина, ширина]
rectangle_area <- function(x) {
  if (length(x) != 2) {
    stop("Для прямоугольника требуется 2 параметра: длина и ширина")
  }
  return(x[1] * x[2])
}

# Класс для круга
# Вектор должен содержать: [радиус]
circle_area <- function(x) {
  if (length(x) != 1) {
    stop("Для круга требуется 1 параметр: радиус")
  }
  return(pi * x[1] * x[1])
}

# Присвоение классов векторам и создание методов для дженерика
# Треугольник
triangle_vec <- c(10, 5)
class(triangle_vec) <- "triangle"
get_area.triangle <- function(x, ...) {
  return(triangle_area(x))
}

# Квадрат
square_vec <- c(5)
class(square_vec) <- "square"
get_area.square <- function(x, ...) {
  return(square_area(x))
}

# Прямоугольник
rectangle_vec <- c(8, 6)
class(rectangle_vec) <- "rectangle"
get_area.rectangle <- function(x, ...) {
  return(rectangle_area(x))
}

# Круг
circle_vec <- c(4)
class(circle_vec) <- "circle"
get_area.circle <- function(x, ...) {
  return(circle_area(x))
}

# Демонстрация работы
cat("=== Демонстрация работы дженерика get_area ===\n\n")

cat("Треугольник (основание=10, высота=5):\n")
cat("Площадь =", get_area(triangle_vec), "\n\n")

cat("Квадрат (сторона=5):\n")
cat("Площадь =", get_area(square_vec), "\n\n")

cat("Прямоугольник (длина=8, ширина=6):\n")
cat("Площадь =", get_area(rectangle_vec), "\n\n")

cat("Круг (радиус=4):\n")
cat("Площадь =", get_area(circle_vec), "\n\n")

# Проверка метода по умолчанию
unknown_vec <- c(1, 2, 3)
cat("Неизвестная фигура:\n")
cat(get_area(unknown_vec), "\n")

