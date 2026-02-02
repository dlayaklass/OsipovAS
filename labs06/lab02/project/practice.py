from functools import reduce

students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 92, 'age': 22},
    {'name': 'Charlie', 'grade': 78, 'age': 19},
    {'name': 'Diana', 'grade': 95, 'age': 21},
    {'name': 'Eve', 'grade': 88, 'age': 20}
]

def analyze_students(students):
    if not students:
        return {'avg_grade': 0, 'excellent': [], 'total': 0}
    
    grades = [s['grade'] for s in students]
    avg_grade = reduce(lambda x, y: x + y, grades) / len(grades)
    excellent = [s for s in students if s['grade'] >= 90]
    total = len(students)
    
    return {
        'avg_grade': avg_grade,
        'excellent': excellent,
        'total': total
    }

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__} с аргументами: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Результат: {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

def prime_generator():
    num = 2
    while True:
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            yield num
        num += 1

print("=== Практические задания ===")
result = analyze_students(students)
print(f"Анализ студентов: {result}")

print("\nДекоратор логирования:")
add(5, 3)

print("\nГенератор простых чисел (первые 10):")
prime_gen = prime_generator()
for i in range(10):
    print(next(prime_gen), end=" ")
print()

