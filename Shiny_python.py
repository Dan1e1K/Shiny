from shiny import App, render, ui, reactive
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os
import time
import socket

# Сортировка пузырьком
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# Сортировка с помощью бинарного поиска (реализация вставки)
def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# Генерация графиков
def generate_histogram(x, y1, y2, labels):
    fig, ax = plt.subplots()
    ax.bar([1, 2], [y1, y2], tick_label=labels)  # Используем bar для гистограммы
    ax.set_ylabel('Время (сек)')
    ax.set_title('Время сортировки')

    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmpfile.name, format='png')
    tmpfile.close()

    plt.close(fig)
    return tmpfile.name

#находим свободный порт
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


# APP
app_ui = ui.page_fluid(
    ui.h2("Сравнение сортировок"),
    ui.input_slider("n_elements", "Количество элементов", min=100, max=5000, value=1000),
    ui.input_action_button("calculate", "Рассчитать"),
    ui.output_text("progress_message"),
    ui.output_text("bubble_time"),  # Добавляем вывод времени для пузырька
    ui.output_text("binary_time"),  # Добавляем вывод времени для бинарной вставки
    ui.output_image("histogram")  # Изменяем название на histogram
)

# SERVER
def server(input, output, session):
    @reactive.Calc
    def data():
        n = input.n_elements()
        arr = np.random.randint(1, 1000, size=n)
        return arr

    @output
    @render.text
    def progress_message():
        if input.calculate() > 0:
            return "Выполняется расчет..."
        return ""

    @reactive.Effect
    def calculate_with_progress():
        if input.calculate() > 0:
            with ui.Progress(min=1, max=100) as p:
                for i in range(1, 101):
                    p.set(i)
                    time.sleep(0.02)

    @output
    @render.text
    def bubble_time():
        if input.calculate() > 0:
            arr = data()
            start_time = time.time()
            bubble_sort(arr.copy())
            time_bubble = time.time() - start_time
            return f"Время сортировки пузырьком: {time_bubble:.4f} сек"
        return ""

    @output
    @render.text
    def binary_time():
        if input.calculate() > 0:
            arr = data()
            start_time = time.time()
            binary_insertion_sort(arr.copy())
            time_binary = time.time() - start_time
            return f"Время сортировки бинарной вставкой: {time_binary:.4f} сек"
        return ""

    @output
    @render.image
    def histogram():
        if input.calculate() > 0:
            arr = data()

            # Сортировка пузырьком
            start_time = time.time()
            bubble_sort(arr.copy())
            time_bubble = time.time() - start_time

            # Сортировка с помощью бинарного поиска (вставка)
            start_time = time.time()
            binary_insertion_sort(arr.copy())
            time_binary = time.time() - start_time

            # Гистограмма
            labels = ["Сортировка пузырьком", "Сортировка бинарной вставкой"]
            plot_path = generate_histogram(None, time_bubble, time_binary, labels)
            return {"src": plot_path, "alt": "Гистограмма сравнения"}

app = App(app_ui, server)

if __name__ == "__main__":
    port = find_free_port()
    app = App(app_ui, server)
    app.run(port=port)
