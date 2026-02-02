# Лабораторная работа №7
# Задание 1 - Параллельное программирование
# Визуализация наиболее часто встречающихся слов из книг Джейн Остин

# Установка и подключение необходимых пакетов
if (!require("janeaustenr", quietly = TRUE)) {
  install.packages("janeaustenr")
}
if (!require("stringr", quietly = TRUE)) {
  install.packages("stringr")
}
if (!require("purrr", quietly = TRUE)) {
  install.packages("purrr")
}

library(janeaustenr)
library(stringr)
library(purrr)

# Функции из задания
extract_words <- function(book_name) {
  text <- subset(austen_books(), book == book_name)$text
  str_extract_all(text, boundary("word")) %>% unlist %>% tolower
}

janeausten_words <- function() {
  books <- austen_books()$book %>% unique %>% as.character
  words <- sapply(books, extract_words) %>% unlist
  words
}

max_frequency <- function(letter, words, min_length = 1) {
  w <- select_words(letter, words = words, min_length = min_length)
  frequency <- table(w)
  frequency[which.max(frequency)]
}

select_words <- function(letter, words, min_length = 1) {
  min_length_words <- words[nchar(words) >= min_length]
  grep(paste0("^", letter), min_length_words, value = TRUE)
}

# Создание вектора слов из книг Джейн Остин
words_vector <- janeausten_words()

# Создание именованного вектора с максимальной частотой слов для каждой буквы
# Используем sapply для применения функции max_frequency к каждой букве алфавита
# Минимальная длина слова: 5 букв
max_freq_words <- sapply(letters, function(letter) {
  max_frequency(letter, words = words_vector, min_length = 5)
})

# Визуализация результатов
cat("=== Наиболее часто встречающиеся слова (минимум 5 букв) ===\n")
print(max_freq_words)
cat("\n")

# Создание графика
barplot(max_freq_words, 
        main = "Наиболее часто встречающиеся слова из книг Джейн Остин\n(по буквам английского алфавита, минимум 5 букв)",
        xlab = "Буква алфавита",
        ylab = "Частота",
        las = 2,  # Вертикальные подписи для оси X
        col = "steelblue",
        border = "darkblue",
        cex.names = 0.8)

