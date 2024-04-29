import numpy as np
import matplotlib.pyplot as plt

# Nastavujeme počet vzorků, které chceme generovat
num_samples = 100000

# Generujeme uniformně rozdělené vzorky Y v intervalu od 0 do 1
samples_Y = np.random.uniform(0, 1, num_samples)

# Spočítáme průměr a směrodatnou odchylku našich vzorků Y
average_Y = np.mean(samples_Y)
std_deviation_Y = np.std(samples_Y)

# Zjistíme, jak často jsou hodnoty Y menší nebo rovné 0.4
prob_Y_less_equal_0_4 = np.mean(samples_Y <= 0.4)

# Provedeme transformaci Y na X vzorcem 1/Y
values_X = 1 / samples_Y

# Vypočítáme průměrnou hodnotu a směrodatnou odchylku pro X
average_X = np.mean(values_X)
std_deviation_X = np.std(values_X)

# Zjišťujeme, jaká je pravděpodobnost, že X leží mezi 2 a 3
prob_X_2_to_3 = np.mean((values_X >= 2) & (values_X <= 3))

# Výpis získaných hodnot na konzoli
print(f"Průměrná hodnota Y: {average_Y}")
print(f"Směrodatná odchylka Y: {std_deviation_Y}")
print(f"Pravděpodobnost, že Y ≤ 0.4: {prob_Y_less_equal_0_4}")
print(f"Průměrná hodnota X: {average_X}")
print(f"Směrodatná odchylka X: {std_deviation_X}")
print(f"Pravděpodobnost, že 2 ≤ X ≤ 3: {prob_X_2_to_3}")

# Nakreslíme histogram
plt.figure(figsize=(10, 6))
plt.hist(values_X, bins=100, range=(0, 100), color='blue', alpha=0.7)
plt.title('Rozložení hodnot X')
plt.xlabel('X')
plt.ylabel('Počet výskytů')
plt.grid(True)
plt.show()
