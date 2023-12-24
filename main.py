import json
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import chi2_contingency
from itertools import combinations

json_file_path = 'data.json'

# Чтение данных из JSON-файла
with open(json_file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Преобразование в DataFrame
columns = [item[0] for item in json_data[0]]
data = [[item[1] for item in row] for row in json_data[1:]]
df = pd.DataFrame(data, columns=columns)

# Вывод DataFrame
# print(df)

# Функция для построения столбчатого графика
def plot_bar_chart(column_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    value_counts = df[column_name].value_counts()
    df[column_name].value_counts().plot(kind='bar', color='m', ax=ax, rot =0)
    plt.xlabel(column_name)
    plt.ylabel('Количество проголосовавших')
    for i, v in enumerate(value_counts):
        ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=10)

    plt.show()

# Построение графика для каждой оценки
# for column in df.columns[2:]:
#     plot_bar_chart(column)

# Преобразование категориальных переменных в числовые для анализа
df_numeric = df.copy()
df_numeric.replace({"Baggins Coffee": 1, "Etlon Coffee": 2, "Stars Coffee": 3, "Surf Coffee": 4}, inplace=True)

# Создание всех возможных комбинаций переменных
variable_combinations = list(combinations(df_numeric.columns[2:], 2))

# Проведение анализа для каждой пары переменных
for variable1, variable2 in variable_combinations:
    # Создание таблицы сопряжённости
    contingency_table = pd.crosstab(df_numeric[variable1], df_numeric[variable2])
    
    # Проведение хи-квадрат теста
    chi2, _, _, _ = chi2_contingency(contingency_table)
    
    # Расчет коэффициента V Крамера
    n = contingency_table.sum().sum()
    v_cramer = (chi2 / (n * (min(contingency_table.shape) - 1))) ** 0.5
    
    # Вывод результатов для каждой пары переменных
    print(f"Коэффициент V Крамера для '{variable1}' и '{variable2}': {v_cramer:.3f}\n")

