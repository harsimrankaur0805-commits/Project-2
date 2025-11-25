import tkinter as tk
from tkinter import ttk, messagebox
import math

# ---------- SCIENTIFIC CALCULATOR ----------
class Calculator(tk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master, bg="#E8F0FE")
        self.pack(fill="both", expand=True)
        self.go_back = go_back
        self.expr = tk.StringVar()
        self.deg_mode = True

        # Display
        tk.Entry(self, textvariable=self.expr, font=("Consolas", 22),
                 bg="#FFFFFF", fg="#000000", justify="right",
                 relief="solid", bd=2).pack(fill="x", padx=10, pady=15)

        # Buttons
        buttons = [
            ["7", "8", "9", "/", "sin"],
            ["4", "5", "6", "*", "cos"],
            ["1", "2", "3", "-", "tan"],
            ["0", ".", "^", "+", "log"],
            ["√", "x²", "x³", "ln", "π"],
            ["abs", "exp", "!", "Deg", "="],
            ["C", "(", ")", "Back", ""]
        ]

        for row in buttons:
            f = tk.Frame(self, bg="#E8F0FE"); f.pack(expand=True, fill="both")
            for b in row:
                if not b: continue
                color = "#87CEFA" if b not in ["C", "Back", "="] else "#FF7F7F"
                tk.Button(f, text=b, font=("Consolas", 15, "bold"),
                          bg=color, fg="#000000", relief="flat",
                          command=lambda ch=b: self.click(ch)).pack(
                    side="left", expand=True, fill="both", padx=2, pady=2
                )

    def click(self, ch):
        e = self.expr.get()
        if ch == "C": self.expr.set("")
        elif ch == "Back": self.go_back()
        elif ch == "=": self.calculate()
        elif ch == "√": self.expr.set(e + "math.sqrt(")
        elif ch == "π": self.expr.set(e + "math.pi")
        elif ch == "x²": self.expr.set(e + "**2")
        elif ch == "x³": self.expr.set(e + "**3")
        elif ch == "^": self.expr.set(e + "**")
        elif ch == "Deg": self.deg_mode = not self.deg_mode
        elif ch == "sin": self.expr.set(e + ("math.sin(math.radians(" if self.deg_mode else "math.sin("))
        elif ch == "cos": self.expr.set(e + ("math.cos(math.radians(" if self.deg_mode else "math.cos("))
        elif ch == "tan": self.expr.set(e + ("math.tan(math.radians(" if self.deg_mode else "math.tan("))
        elif ch == "log": self.expr.set(e + "math.log10(")
        elif ch == "ln": self.expr.set(e + "math.log(")
        elif ch == "abs": self.expr.set(e + "abs(")
        elif ch == "exp": self.expr.set(e + "math.exp(")
        elif ch == "!": self.expr.set(e + "math.factorial(")
        else: self.expr.set(e + ch)

    def calculate(self):
        try:
            res = eval(self.expr.get())
            self.expr.set(res)
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")


# ---------- UNIT CONVERTER ----------
class Converter(tk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master, bg="#E8F0FE")
        self.pack(fill="both", expand=True)
        self.go_back = go_back

        tk.Label(self, text="Unit Converter", font=("Consolas", 20, "bold"),
                 fg="#000000", bg="#E8F0FE").pack(pady=10)

        self.type_cb = ttk.Combobox(self, values=[
            "Temperature", "Length", "Weight", "Volume",
            "Area", "Speed", "Time", "Angle"
        ])
        self.type_cb.set("Temperature")
        self.type_cb.pack(pady=5)
        self.type_cb.bind("<<ComboboxSelected>>", lambda e: self.set_units())

        self.entry = tk.Entry(self, font=("Consolas", 16))
        self.entry.pack(pady=5)
        self.from_cb = ttk.Combobox(self, width=10)
        self.to_cb = ttk.Combobox(self, width=10)
        self.from_cb.pack(pady=5)
        self.to_cb.pack(pady=5)
        self.set_units()

        # Buttons row (Convert + Back side-by-side)
        btn_frame = tk.Frame(self, bg="#E8F0FE")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Convert", bg="#87CEFA", fg="#000000",
                  font=("Consolas", 13), width=10, command=self.convert).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Back", bg="#FF7F7F", fg="#000000",
                  font=("Consolas", 13), width=10, command=self.go_back).pack(side="left", padx=10)

        self.result = tk.Label(self, text="", font=("Consolas", 16),
                               fg="#000000", bg="#E8F0FE")
        self.result.pack(pady=5)

    def set_units(self):
        t = self.type_cb.get()
        if t == "Temperature":
            u = ["Celsius", "Fahrenheit", "Kelvin"]
        elif t == "Length":
            u = ["cm", "m", "km", "inch", "foot", "mile"]
        elif t == "Weight":
            u = ["g", "kg", "lb", "oz"]
        elif t == "Volume":
            u = ["mL", "L", "gallon"]
        elif t == "Area":
            u = ["m²", "cm²", "km²", "ft²", "acre", "hectare"]
        elif t == "Speed":
            u = ["m/s", "km/h", "mph", "knot"]
        elif t == "Time":
            u = ["sec", "min", "hour", "day"]
        elif t == "Angle":
            u = ["degree", "radian", "grad"]
        else:
            u = []
        self.from_cb["values"], self.to_cb["values"] = u, u
        if u: self.from_cb.set(u[0]); self.to_cb.set(u[1])

    def convert(self):
        try:
            v = float(self.entry.get())
            f, t, cat = self.from_cb.get(), self.to_cb.get(), self.type_cb.get()

            if cat == "Temperature": r = self.temp(v, f, t)
            elif cat == "Angle": r = v * {"degree": 1, "radian": 57.2958, "grad": 0.9}[f] / {"degree": 1, "radian": 57.2958, "grad": 0.9}[t]
            else:
                data = {
                    "Length": {"cm": 0.01, "m": 1, "km": 1000, "inch": 0.0254, "foot": 0.3048, "mile": 1609.34},
                    "Weight": {"g": 0.001, "kg": 1, "lb": 0.453592, "oz": 0.0283495},
                    "Volume": {"mL": 0.001, "L": 1, "gallon": 3.78541},
                    "Area": {"cm²": 0.0001, "m²": 1, "km²": 1e6, "ft²": 0.092903, "acre": 4046.86, "hectare": 10000},
                    "Speed": {"m/s": 1, "km/h": 0.277778, "mph": 0.44704, "knot": 0.514444},
                    "Time": {"sec": 1, "min": 60, "hour": 3600, "day": 86400}
                }
                r = v * data[cat][f] / data[cat][t]
            self.result.config(text=f"{r:.6g}")
        except Exception:
            messagebox.showerror("Error", "Invalid conversion")

    def temp(self, v, f, t):
        if f == t: return v
        if f == "Celsius":
            return v * 9/5 + 32 if t == "Fahrenheit" else v + 273.15
        if f == "Fahrenheit":
            return (v - 32) * 5/9 if t == "Celsius" else (v - 32) * 5/9 + 273.15
        if f == "Kelvin":
            return v - 273.15 if t == "Celsius" else (v - 273.15) * 9/5 + 32


# ---------- MAIN MENU ----------
class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Calculator Suite")
        self.geometry("360x300")
        self.config(bg="#E8F0FE")

        self.menu = tk.Frame(self, bg="#E8F0FE")
        self.menu.pack(fill="both", expand=True)

        tk.Label(self.menu, text="Select Mode", bg="#E8F0FE", fg="#000000",
                 font=("Consolas", 18, "bold")).pack(pady=20)
        tk.Button(self.menu, text="Scientific Calculator", bg="#87CEFA", fg="#000000",
                  font=("Consolas", 14), command=self.open_calc).pack(fill="x", padx=40, pady=10)
        tk.Button(self.menu, text="Unit Converter", bg="#87CEFA", fg="#000000",
                  font=("Consolas", 14), command=self.open_conv).pack(fill="x", padx=40, pady=10)
        tk.Button(self.menu, text="Exit", bg="#FF7F7F", fg="#000000",
                  font=("Consolas", 14), command=self.destroy).pack(fill="x", padx=40, pady=20)

    def open_calc(self):
        self.clear(); Calculator(self, self.show_menu)

    def open_conv(self):
        self.clear(); Converter(self, self.show_menu)

    def show_menu(self):
        self.clear(); self.menu.pack(fill="both", expand=True)

    def clear(self):
        for w in self.winfo_children(): w.pack_forget()


if __name__ == "__main__":
    MainMenu().mainloop()
