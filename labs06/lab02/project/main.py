from functions_as_objects import *
from lambda_closures import *
from higher_order import *
from comprehensions_generators import *
from decorators import *
from practice import *

def main():
    print("=== Демонстрация функционального программирования в Python ===\n")
    
    print("1. Функции как объекты:")
    print(f"apply_function(square, 5) = {apply_function(square, 5)}\n")
    
    print("2. Lambda и замыкания:")
    counter = create_counter()
    print(f"Счетчик: {counter()}, {counter()}, {counter()}\n")
    
    print("3. Функции высшего порядка:")
    print(f"Произведение чисел: {product}\n")
    
    print("4. Генераторы и включения:")
    print(f"Четные квадраты: {even_squares}\n")
    
    print("5. Декораторы:")
    greet("Мария")

if __name__ == "__main__":
    main()

