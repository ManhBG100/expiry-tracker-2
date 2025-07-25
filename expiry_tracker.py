import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta, date
import json
import os

SAVE_FILE = "products.json"

class ProductTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Theo dõi hạn sử dụng sản phẩm")
        self.products = []

        self.load_products()  # ✅ Tải từ file nếu có

        # --- Giao diện nhập sản phẩm ---
        tk.Label(root, text="Tên sản phẩm").grid(row=0, column=0)
        tk.Label(root, text="Ngày mua (YYYY-MM-DD)").grid(row=0, column=1)
        tk.Label(root, text="Hạn sử dụng (YYYY-MM-DD)").grid(row=0, column=2)

        self.name_entry = tk.Entry(root)
        self.buy_entry = tk.Entry(root)
        self.expiry_entry = tk.Entry(root)

        self.name_entry.grid(row=1, column=0)
        self.buy_entry.grid(row=1, column=1)
        self.expiry_entry.grid(row=1, column=2)

        self.auto_expiry_var = tk.IntVar()
        self.auto_expiry_checkbox = tk.Checkbutton(root, text="Hết hạn sau 1 tháng", variable=self.auto_expiry_var, command=self.toggle_expiry_entry)
        self.auto_expiry_checkbox.grid(row=2, column=2)

        self.add_button = tk.Button(root, text="➕ Thêm sản phẩm", command=self.add_product)
        self.add_button.grid(row=1, column=3, rowspan=2, sticky="ns")

        self.list_frame = tk.Frame(root)
        self.list_frame.grid(row=3, column=0, columnspan=4, pady=10)

        self.update_ui()

    def toggle_expiry_entry(self):
        if self.auto_expiry_var.get():
            self.expiry_entry.config(state='disabled')
        else:
            self.expiry_entry.config(state='normal')

    def add_product(self):
        name = self.name_entry.get().strip()
        buy = self.buy_entry.get().strip()
        use_auto = self.auto_expiry_var.get()

        try:
            buy_date = datetime.strptime(buy, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày mua không đúng định dạng YYYY-MM-DD")
            return

        if use_auto:
            expiry_date = buy_date + timedelta(days=30)
        else:
            expiry = self.expiry_entry.get().strip()
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Lỗi", "Ngày hết hạn không đúng định dạng YYYY-MM-DD")
                return

        self.products.append({
            "name": name,
            "buy_date": buy_date.isoformat(),
            "expiry_date": expiry_date.isoformat()
        })
        self.save_products()
        self.clear_entries()
        self.update_ui()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.buy_entry.delete(0, tk.END)
        self.expiry_entry.delete(0, tk.END)
        self.auto_expiry_var.set(0)
        self.expiry_entry.config(state='normal')

    def delete_product(self, index):
        del self.products[index]
        self.save_products()
        self.update_ui()

    def update_ui(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        today = date.today()

        for i, product in enumerate(self.products):
            name = product["name"]
            expiry = datetime.strptime(product["expiry_date"], "%Y-%m-%d").date()
            days_left = (expiry - today).days
            days_text = f"{days_left} ngày còn lại" if days_left >= 0 else "Đã hết hạn"

            tk.Label(self.list_frame, text=f"{name} - {days_text}").grid(row=i, column=0, sticky="w")
            tk.Button(self.list_frame, text="❌ Xóa", command=lambda i=i: self.delete_product(i)).grid(row=i, column=1)

        self.root.after(60 * 1000, self.update_ui)  # Cập nhật mỗi phút

    def save_products(self):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.products, f, indent=2, ensure_ascii=False)

    def load_products(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                self.products = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductTracker(root)
    root.mainloop()
