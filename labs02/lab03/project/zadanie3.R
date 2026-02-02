# Лабораторная работа №3
# Задание 3 - Объектно-ориентированное программирование
# Создание класса Копилка с использованием R6

# Установка и подключение пакета R6 (если не установлен)
if (!require("R6", quietly = TRUE)) {
  install.packages("R6")
}
library(R6)

# Создание генератора класса Копилка
PiggyBank <- R6Class(
  "PiggyBank",
  private = list(
    balance = 0,  # Текущий баланс (количество денег в копилке)
    capacity = 1000,  # Максимальная вместимость копилки
    is_broken = FALSE  # Состояние копилки (целая или разбита)
  ),
  public = list(
    # Метод инициализации
    initialize = function(initial_balance = 0, capacity = 1000) {
      if (initial_balance < 0) {
        stop("Начальный баланс не может быть отрицательным")
      }
      if (capacity <= 0) {
        stop("Вместимость должна быть положительной")
      }
      private$balance <- initial_balance
      private$capacity <- capacity
      cat("Копилка создана. Вместимость:", private$capacity, "единиц\n")
      if (private$balance > 0) {
        cat("Начальный баланс:", private$balance, "единиц\n")
      }
    },
    
    # Метод добавления денег в копилку
    deposit = function(amount) {
      if (private$is_broken) {
        cat("ОШИБКА: Копилка разбита! Невозможно добавить деньги.\n")
        return(invisible(NULL))
      }
      
      if (amount <= 0) {
        cat("ОШИБКА: Сумма должна быть положительной.\n")
        return(invisible(NULL))
      }
      
      if (private$balance + amount > private$capacity) {
        overflow <- (private$balance + amount) - private$capacity
        cat("ОШИБКА: Копилка переполнена! Превышение:", overflow, "единиц\n")
        cat("Можно добавить максимум:", private$capacity - private$balance, "единиц\n")
        return(invisible(NULL))
      }
      
      private$balance <- private$balance + amount
      cat("Добавлено", amount, "единиц. Текущий баланс:", private$balance, "единиц\n")
    },
    
    # Метод разбития копилки (извлечение всех денег)
    break_bank = function() {
      if (private$is_broken) {
        cat("Копилка уже разбита. Денег в ней нет.\n")
        return(0)
      }
      
      withdrawn <- private$balance
      private$balance <- 0
      private$is_broken <- TRUE
      cat("Копилка разбита! Извлечено", withdrawn, "единиц\n")
      return(withdrawn)
    },
    
    # Метод проверки баланса (без разбития)
    check_balance = function() {
      cat("Текущий баланс:", private$balance, "единиц\n")
      cat("Свободное место:", private$capacity - private$balance, "единиц\n")
      cat("Состояние:", ifelse(private$is_broken, "разбита", "целая"), "\n")
      return(private$balance)
    },
    
    # Метод получения информации о копилке
    get_info = function() {
      cat("=== Информация о копилке ===\n")
      cat("Вместимость:", private$capacity, "единиц\n")
      cat("Текущий баланс:", private$balance, "единиц\n")
      cat("Свободное место:", private$capacity - private$balance, "единиц\n")
      cat("Состояние:", ifelse(private$is_broken, "разбита", "целая"), "\n")
    }
  )
)

# Демонстрация работы класса Копилка
cat("=== Создание копилки ===\n")
piggy_bank <- PiggyBank$new(initial_balance = 0, capacity = 1000)
cat("\n")

cat("=== Проверка баланса ===\n")
piggy_bank$check_balance()
cat("\n")

cat("=== Добавление денег ===\n")
piggy_bank$deposit(100)
piggy_bank$deposit(250)
piggy_bank$deposit(50)
cat("\n")

cat("=== Проверка баланса после добавления ===\n")
piggy_bank$check_balance()
cat("\n")

cat("=== Попытка переполнения ===\n")
piggy_bank$deposit(700)  # Это должно вызвать ошибку переполнения
cat("\n")

cat("=== Добавление допустимой суммы ===\n")
piggy_bank$deposit(600)  # Это должно пройти успешно
cat("\n")

cat("=== Информация о копилке ===\n")
piggy_bank$get_info()
cat("\n")

cat("=== Разбитие копилки ===\n")
withdrawn <- piggy_bank$break_bank()
cat("Извлечено денег:", withdrawn, "единиц\n")
cat("\n")

cat("=== Попытка добавить деньги в разбитую копилку ===\n")
piggy_bank$deposit(100)
cat("\n")

cat("=== Финальная информация ===\n")
piggy_bank$get_info()

