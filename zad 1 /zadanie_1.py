import math

list_a = [21, -20, 9, 4]
list_b = [9, 25, 16, -5]

# łączenie list za pomocą zip(), czyli iteratora z parami elementów
# dokumentacja zip(): https://docs.python.org/3/library/functions.html#zip

polaczone = zip(list_a, list_b)

print("Przetwarzanie par liczb:")
for x, y in polaczone:
    suma = x + y
    try:
        # obliczanie pierwiastka kwadratowego z sumy za pomocą math.sqrt()
        # dokumentacja o tu - https://docs.python.org/3/library/math.html#math.sqrt
        pierwiastek = math.sqrt(suma)
        print(f"Pierwiastek z sumy {x} + {y} = {suma} to {pierwiastek:.2f}")
    except ValueError as e:
        # except dla liczb ujemnych
        print(f"o nie, tu jest błąd dla sumy {x} + {y} = {suma}!", "Nie można obliczyć pierwiastka z liczby ujemnej")