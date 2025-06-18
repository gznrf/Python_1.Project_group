import tkinter as tk
import uuid
from tkinter import ttk, messagebox
from datetime import datetime
from src.logic import Logic
from src.storage import Storage

class Screen:

    logic_operations = Logic()
    storage_operations = Storage()
    root = tk.Tk()
    frame_left = tk.Frame(root, padx=10, pady=10)
    frame_right = tk.Frame(root, padx=10, pady=10)
    combo_function = ttk.Combobox(frame_left, values=["Простой процент", "Сложный процент", "Аннуитетный платеж"], state="readonly")

    entry_amount = tk.Entry(frame_left)
    entry_rate = tk.Entry(frame_left)
    entry_term = tk.Entry(frame_left)

    label_period = tk.Label(frame_left, text="Периодичность:")
    combo_period = ttk.Combobox(frame_left, values=["Ежемесячно", "Ежеквартально", "Ежегодно"], state="readonly")

    label_term_type = tk.Label(frame_left, text="Тип срока:")
    combo_term_type = ttk.Combobox(frame_left, values=["Месяцы", "Годы"], state="readonly")
    columns = ("Сумма", "Ставка", "Срок", "Результат", "Дата", "Тип", "Периодичность")
    history_table = ttk.Treeview(frame_right, columns=columns, show="headings")
    btn_calculate = tk.Button(frame_left, text="Рассчитать")
    result_label = tk.Label(frame_left, text="Результат: ")

    btn_show_schedule = tk.Button(frame_right, text="Показать график")
    btn_clear_history = tk.Button(frame_right, text="Очистить историю", command=storage_operations.clear)
    btn_save_result = tk.Button(frame_right, text="Сохранить результат")
    btn_exit = tk.Button(frame_right, text="Выйти")

    def add_record(self):
        new_uuid = uuid.uuid4()
        mode = self.combo_function.get()
        principal = float(self.entry_amount.get())
        rate = float(self.entry_rate.get())
        term = int(self.entry_term.get())
        period = self.combo_period.get() if mode == "Сложный процент" else "-"
        result = None
        record = {
            new_uuid : {
                principal,
                rate,
                term,
                round(result, 2),
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                mode,
                period
            }
        }
        self.storage_operations.add_record(record)


    def calculate(self):
        try:
            mode = self.combo_function.get()
            principal = float(self.entry_amount.get())
            rate = float(self.entry_rate.get())
            term = int(self.entry_term.get())
            period = self.combo_period.get() if mode == "Сложный процент" else "-"
            result = None

            if mode == "Простой процент":
                result = self.logic_operations.simple_interest(principal, rate, period)
            elif mode == "Сложный процент":
                periods_per_year = {"Ежемесячно": 12, "Ежеквартально": 4, "Ежегодно": 1}[period]
                result = self.logic_operations.compound_interest(principal, rate, period, periods_per_year)
            elif mode == "Аннуитетный платеж":
                result = self.logic_operations.annuity_payment(principal, rate, period)

            self.result_label.config(text=f"Результат: {round(result, 2)}")

            # Добавить в историю
            self.history_table.insert("", "end", values=[
                principal,
                rate,
                term,
                round(result, 2),
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                mode,
                period
            ])

        except Exception as e:
            self.result_label.config(text=f"Ошибка: {e}")

    def on_function_change(self, event=None):
        selected = self.combo_function.get()

        self.label_period.grid_remove()
        self.combo_period.grid_remove()

        if selected == "Простой процент":
            self.combo_term_type.set("Годы")
            self.combo_term_type.config(state="disabled")

        elif selected == "Сложный процент":
            self.combo_term_type.set("Годы")
            self.combo_term_type.config(state="disabled")
            self.label_period.grid(row=5, column=0, sticky="w", pady=2)
            self.combo_period.grid(row=5, column=1, pady=2)

        elif selected == "Аннуитетный платеж":
            self.combo_term_type.set("Месяцы")
            self.combo_term_type.config(state="disabled")

        self.label_term_type.grid(row=4, column=0, sticky="w", pady=2)
        self.combo_term_type.grid(row=4, column=1, pady=2)

    def exit_app(self):
        self.root.destroy()

    def show_schedule_window(self):
        selected = self.history_table.focus()
        if not selected:
            messagebox.showwarning("График", "Выберите запись в истории для просмотра графика.")
            return

        values = self.history_table.item(selected, "values")
        try:
            principal = float(values[0])
            rate = float(values[1])
            term = int(values[2])
            mode = values[5]

            if mode != "Аннуитетный платеж":
                messagebox.showinfo("График", "График доступен только для аннуитетных платежей.")
                return

            monthly_rate = rate / 12
            payment = self.logic_operations.annuity_payment(principal, monthly_rate, term)

            window = tk.Toplevel(self.root)
            window.title("График платежей")
            window.geometry("600x400")

            tree = ttk.Treeview(window, columns=("Месяц", "Платеж", "Проценты", "Основной долг", "Остаток"), show="headings")
            for col in ("Месяц", "Платеж", "Проценты", "Основной долг", "Остаток"):
                tree.heading(col, text=col)
                tree.column(col, anchor="center")
            tree.pack(fill=tk.BOTH, expand=True)

            balance = principal
            for month in range(1, term + 1):
                interest = balance * monthly_rate
                principal_payment = payment - interest
                balance -= principal_payment
                tree.insert("", "end", values=(
                    month,
                    round(payment, 2),
                    round(interest, 2),
                    round(principal_payment, 2),
                    round(max(balance, 0), 2)
                ))

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график: {e}")

    def set_button_commands(self):
        self.btn_calculate.command=self.calculate
        self.btn_show_schedule.command=self.show_schedule_window
        self.btn_exit.command=self.exit_app
        self.btn_save_result.command=self.add_record

    def draw(self):
        # --- GUI ---
        self.root.title("Финансовый калькулятор")
        self.root.geometry("950x500")

        # Левый фрейм — ввод
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y)

        # Правый фрейм — таблица + кнопки
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Функция
        tk.Label(self.frame_left, text="Функция:").grid(row=0, column=0, sticky="w", pady=2)
        self.combo_function.set("Простой процент")
        self.combo_function.grid(row=0, column=1, pady=2)
        self.combo_function.bind("<<ComboboxSelected>>", self.on_function_change)

        # Сумма
        tk.Label(self.frame_left, text="Сумма:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_amount.grid(row=1, column=1, pady=2)

        # Ставка
        tk.Label(self.frame_left, text="Ставка (в долях):").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_rate.grid(row=2, column=1, pady=2)

        # Срок
        tk.Label(self.frame_left, text="Срок:").grid(row=3, column=0, sticky="w", pady=2)
        self.entry_term.grid(row=3, column=1, pady=2)

        # Тип срока
        self.combo_term_type.set("Годы")

        # Периодичность (только для сложного процента)
        self.combo_period.set("Ежемесячно")

        # Кнопка расчета
        self.btn_calculate.grid(row=6, column=0, columnspan=2, pady=10)

        # Результат
        self.result_label.grid(row=7, column=0, columnspan=2)

        # Таблица истории
        for col in self.columns:
            self.history_table.heading(col, text=col)
            self.history_table.column(col, width=100, anchor="center")
        self.history_table.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Кнопки под таблицей (в одну строку)
        self.frame_right.grid_rowconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure((0,1,2,3), weight=1)
        self.btn_show_schedule.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        self.btn_clear_history.grid(row=1, column=1, sticky="ew", padx=5, pady=10)
        self.btn_save_result.grid(row=1, column=2, sticky="ew", padx=5, pady=10)
        self.btn_exit.grid(row=1, column=3, sticky="ew", padx=5, pady=10)
        self.set_button_commands()
        # Запускаем начальное состояние
        self.on_function_change()
        self.root.mainloop()

    
