# Лабораторная работа №7
# Задание 2 - Параллельное программирование
# Распараллеливание кода с использованием вычислительного кластера

# Установка и подключение пакета parallel
if (!require("parallel", quietly = TRUE)) {
  install.packages("parallel")
}
library(parallel)

# Функция mean_of_rnorm
mean_of_rnorm <- function(n) {
  random_numbers <- rnorm(n)
  mean(random_numbers)
}

# Исходный код (последовательное выполнение)
cat("=== Последовательное выполнение ===\n")
start_time_seq <- Sys.time()
result_seq <- numeric(50)
for(iter in seq_len(50)) {
  result_seq[iter] <- mean_of_rnorm(10000)
}
end_time_seq <- Sys.time()
time_seq <- end_time_seq - start_time_seq
cat("Время выполнения (последовательно):", time_seq, "\n")
cat("Среднее значение результатов:", mean(result_seq), "\n\n")

# Параллельное выполнение
cat("=== Параллельное выполнение ===\n")

# Определение количества ядер
ncores <- detectCores(logical = FALSE)
cat("Количество физических ядер:", ncores, "\n")

# Создание кластера
cl <- makeCluster(ncores)
cat("Кластер создан\n")

# Экспорт функции в кластер
clusterExport(cl, "mean_of_rnorm")

# Параллельное выполнение
start_time_par <- Sys.time()
# Создаем вектор итераций для параллельной обработки
iterations <- seq_len(50)
result_par <- parSapply(cl, iterations, function(iter) {
  mean_of_rnorm(10000)
})
end_time_par <- Sys.time()
time_par <- end_time_par - start_time_par

# Остановка кластера
stopCluster(cl)
cat("Кластер остановлен\n\n")

# Результаты
cat("Время выполнения (параллельно):", time_par, "\n")
cat("Среднее значение результатов:", mean(result_par), "\n\n")

# Сравнение результатов
cat("=== Сравнение результатов ===\n")
cat("Ускорение:", as.numeric(time_seq) / as.numeric(time_par), "x\n")
cat("Разница в средних значениях:", abs(mean(result_seq) - mean(result_par)), "\n")

# Визуализация результатов
cat("\n=== Визуализация результатов ===\n")
par(mfrow = c(1, 2))
hist(result_seq, main = "Последовательное выполнение", 
     xlab = "Среднее значение", col = "lightblue", border = "black")
hist(result_par, main = "Параллельное выполнение", 
     xlab = "Среднее значение", col = "lightgreen", border = "black")
par(mfrow = c(1, 1))

