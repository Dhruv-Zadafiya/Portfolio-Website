import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk
import re


class RealTimeCurrencyConverter:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data["rates"]

    def convert(self, from_currency, to_currency, amount):
        if from_currency != "USD":
            amount = amount / self.currencies[from_currency]
        return round(amount * self.currencies[to_currency], 4)


class App(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("600x350")
        self.resizable(False, False)

        self.currency_converter = converter

        title = Label(
            self,
            text="💱 Real-Time Currency Converter 💱",
            fg="white",
            bg="#1e3c72",
            font=("Arial", 18, "bold"),
            pady=8
        )
        title.pack(fill=X)

        info = Label(
            self,
            text=f"1 INR = {self.currency_converter.convert('INR','USD',1)} USD | Date: {self.currency_converter.data['date']}",
            fg="black",
            bg="#a8e6ff",
            font=("Arial", 12, "bold")
        )
        info.pack(fill=X)

        frame = Frame(self, bg="#ffffff", bd=5, relief=RIDGE)
        frame.place(x=80, y=100, width=440, height=200)

        valid = (self.register(self.restrictNumberOnly), "%d", "%P")

        Label(frame, text="Amount", bg="white", font=("Arial", 12, "bold")).place(x=20, y=30)
        self.amount = Entry(frame, font=("Arial", 12), justify=CENTER,
                            validate="key", validatecommand=valid, bd=3)
        self.amount.place(x=20, y=60, width=150)

        Label(frame, text="From Currency", bg="white", font=("Arial", 12, "bold")).place(x=240, y=10)
        Label(frame, text="To Currency", bg="white", font=("Arial", 12, "bold")).place(x=240, y=95)

        font = ("Arial", 11, "bold")

        self.from_currency = StringVar(value="INR")
        self.to_currency = StringVar(value="USD")

        self.from_dropdown = ttk.Combobox(
            frame, values=list(self.currency_converter.currencies.keys()),
            textvariable=self.from_currency, state="readonly",
            font=font, width=10, justify=CENTER
        )
        self.from_dropdown.place(x=240, y=40)

        self.to_dropdown = ttk.Combobox(
            frame, values=list(self.currency_converter.currencies.keys()),
            textvariable=self.to_currency, state="readonly",
            font=font, width=10, justify=CENTER
        )
        self.to_dropdown.place(x=240, y=125)

        self.result_label = Label(
            frame, text="Converted Amount", fg="black", bg="white",
            font=("Arial", 14, "bold"), relief=SUNKEN, bd=3
        )
        self.result_label.place(x=20, y=130, width=200)

        self.convert_button = Button(
            frame,
            text="Convert",
            font=("Arial", 12, "bold"),
            bg="#00c4ff",
            fg="black",
            activebackground="#0088cc",
            command=self.perform
        )
        self.convert_button.place(x=170, y=95, width=70, height=30)

        self.convert_button.bind("<Enter>", lambda e: self.convert_button.config(bg="#0099cc"))
        self.convert_button.bind("<Leave>", lambda e: self.convert_button.config(bg="#00c4ff"))

    def perform(self):
        try:
            amount = float(self.amount.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            converted = self.currency_converter.convert(from_curr, to_curr, amount)
            self.result_label.config(text=f"{converted} {to_curr}")

        except:
            self.result_label.config(text="Invalid Input")

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return string == "" or (string.count(".") <= 1 and result is not None)


if __name__ == "__main__":
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    converter = RealTimeCurrencyConverter(url)

    app = App(converter)
    app.mainloop()
