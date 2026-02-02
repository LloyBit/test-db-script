from datetime import datetime

# Декоратор для измерения времени выполнения функции
def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        print(f"Execution time for {func.__name__}: {end - start}")
        return result
    return wrapper

