import streamlit as st
from datetime import datetime, timedelta, date
import json
import os

SAVE_FILE = "products.json"

# --- Hàm xử lý lưu / tải dữ liệu ---
def load_products():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_products(products):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

# --- Load dữ liệu ---
products = load_products()

st.title("📦 Theo dõi hạn sử dụng sản phẩm")

# --- Nhập sản phẩm ---
with st.form("add_product_form"):
    name = st.text_input("Tên sản phẩm")
    buy_date = st.date_input("Ngày mua", value=date.today())
    auto_expire = st.checkbox("Hết hạn sau 1 tháng")
    expiry_date = None
    if not auto_expire:
        expiry_date = st.date_input("Hạn sử dụng", min_value=buy_date)
    submit = st.form_submit_button("➕ Thêm sản phẩm")

    if submit and name:
        expiry = (buy_date + timedelta(days=30)) if auto_expire else expiry_date
        products.append({
            "name": name,
            "buy_date": buy_date.isoformat(),
            "expiry_date": expiry.isoformat()
        })
        save_products(products)
        st.success(f"Đã thêm sản phẩm: {name}")
        st.experimental_rerun()

# --- Hiển thị danh sách ---
st.subheader("📋 Danh sách sản phẩm")
today = date.today()

if products:
    for i, p in enumerate(products):
        expiry = datetime.strptime(p["expiry_date"], "%Y-%m-%d").date()
        days_left = (expiry - today).days
        status = f"⏳ Còn {days_left} ngày" if days_left >= 0 else "❌ Đã hết hạn"
        st.markdown(f"**{p['name']}** - {status} (hết hạn: {p['expiry_date']})")
        if st.button(f"🗑️ Xóa {p['name']}", key=f"delete_{i}"):
            products.pop(i)
            save_products(products)
            st.experimental_rerun()
else:
    st.info("Chưa có sản phẩm nào.")
