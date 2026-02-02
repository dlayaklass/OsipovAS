# Лабораторная работа №3
# Задание 2 - Объектно-ориентированное программирование
# Создание класса Микроволновая печь с использованием R6

# Установка и подключение пакета R6 (если не установлен)
if (!require("R6", quietly = TRUE)) {
  install.packages("R6")
}
library(R6)

# Создание генератора класса Микроволновая печь
MicrowaveOven <- R6Class(
  "MicrowaveOven",
  private = list(
    power = 800,  # Мощность в ваттах (по умолчанию)
    door_open = FALSE  # Состояние дверцы (FALSE - закрыта, TRUE - открыта)
  ),
  public = list(
    # Метод инициализации
    initialize = function(power = 800, door_open = FALSE) {
      private$power <- power
      private$door_open <- door_open
      cat("Микроволновая печь создана. Мощность:", private$power, "Вт\n")
    },
    
    # Метод открытия дверцы
    open_door = function() {
      if (private$door_open) {
        cat("Дверца уже открыта.\n")
      } else {
        private$door_open <- TRUE
        cat("Дверца открыта.\n")
      }
    },
    
    # Метод закрытия дверцы
    close_door = function() {
      if (!private$door_open) {
        cat("Дверца уже закрыта.\n")
      } else {
        private$door_open <- FALSE
        cat("Дверца закрыта.\n")
      }
    },
    
    # Метод приготовления пищи
    cook = function() {
      if (private$door_open) {
        cat("ОШИБКА: Невозможно начать приготовление. Дверца открыта!\n")
        return(invisible(NULL))
      }
      
      # Время приготовления зависит от мощности (чем больше мощность, тем меньше время)
      # Формула: время = 60 секунд * (базовая мощность / текущая мощность)
      base_power <- 800
      cooking_time <- 60 * (base_power / private$power)
      
      cat("Начато приготовление пищи...\n")
      cat("Мощность:", private$power, "Вт\n")
      cat("Время приготовления:", round(cooking_time, 2), "секунд\n")
      
      # Система в бездействии на время приготовления
      Sys.sleep(cooking_time)
      
      cat("Пища готова!\n")
    },
    
    # Метод для получения информации о состоянии
    get_status = function() {
      cat("=== Состояние микроволновой печи ===\n")
      cat("Мощность:", private$power, "Вт\n")
      cat("Дверца:", ifelse(private$door_open, "открыта", "закрыта"), "\n")
    }
  )
)

# Создание объекта со значениями по умолчанию
cat("=== Создание микроволновой печи №1 (значения по умолчанию) ===\n")
microwave1 <- MicrowaveOven$new()
microwave1$get_status()
cat("\n")

# Создание объекта с передаваемыми значениями
cat("=== Создание микроволновой печи №2 (мощность 1200 Вт) ===\n")
microwave2 <- MicrowaveOven$new(power = 1200, door_open = FALSE)
microwave2$get_status()
cat("\n")

# Демонстрация работы первого объекта
cat("=== Демонстрация работы микроволновой печи №1 ===\n")
microwave1$close_door()
cat("Попытка приготовления с открытой дверцей:\n")
microwave1$open_door()
microwave1$cook()
cat("\n")

microwave1$close_door()
cat("Приготовление с закрытой дверцей:\n")
# Для демонстрации уменьшим время ожидания (в реальности будет полное время)
# microwave1$cook()  # Раскомментировать для полного выполнения
cat("(В реальном выполнении здесь будет ожидание", round(60 * (800 / 800), 2), "секунд)\n")
cat("\n")

# Демонстрация работы второго объекта
cat("=== Демонстрация работы микроволновой печи №2 ===\n")
microwave2$close_door()
cat("Приготовление на мощности 1200 Вт:\n")
# microwave2$cook()  # Раскомментировать для полного выполнения
cat("(В реальном выполнении здесь будет ожидание", round(60 * (800 / 1200), 2), "секунд)\n")

