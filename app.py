import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 1. Đọc dữ liệu từ file Excel
file_path = "O.F China lane Analysis.xlsx"
df = pd.read_excel(file_path, sheet_name="OF")

# Làm sạch tên cột (loại bỏ khoảng trắng thừa ở tên cột)
df.columns = df.columns.str.strip()

# 2. Xử lý cột ETD (Định dạng kiểu 21-Sep-26)
# Dùng errors='coerce' để nếu ô nào lỗi thì chuyển thành NaT thay vì sập app
# Dùng format='mixed' giúp pandas tự linh hoạt đọc các kiểu chuỗi ngày tháng
df["ETD"] = pd.to_datetime(df["ETD"], errors="coerce", format="mixed")

# Kiểm tra số lượng dòng trước và sau khi lọc ngày để debug trên màn hình
total_rows_before = len(df)
df = df.dropna(subset=["ETD"])
total_rows_after = len(df)

st.write(
    f"📊 Kiểm tra dữ liệu: Tổng số dòng ban đầu là {total_rows_before}, số dòng sau khi lọc ngày hợp lệ là {total_rows_after}"
)

# Sắp xếp lại theo thời gian ETD
df = df.sort_values("ETD")

# 3. Tính toán các khoảng gap theo yêu cầu
# Gap 1: Tổng chi phí (TOTAL COST) vs Tổng SR (Total SR)
df["Gap_Cost_SR_20"] = df["Total SR 20'"] - df["TOTAL COST 20'"]
df["Gap_Cost_SR_40"] = df["Total SR 40'"] - df["TOTAL COST 40'"]

# Gap 2: Total BR Surcharge vs Total SR Surcharge
df["Gap_Surcharge_20"] = df["Total SR Surcharge 20'"] - df["Total BR surcharge 20'"]
df["Gap_Surcharge_40"] = df["Total SR Surcharge 40'"] - df["Total BR surcharge 40'"]

# Gap 3: OF BR vs SR (Base Rate)
df["Gap_BaseRate_20"] = df["SR 20'"] - df["OF BR 20'"]
df["Gap_BaseRate_40"] = df["SR 40'"] - df["OF BR 40'"]

# 4. Thiết lập và vẽ biểu đồ
filter_lane = None  # Hoặc tên lane bạn muốn lọc

fig, axes = plt.subplots(3, 1, figsize=(12, 14), sharex=True)
sns.set_theme(style="whitegrid")

title_suffix = f" (Lane: {filter_lane})" if filter_lane else " (All Lanes)"

# Biểu đồ 1: TOTAL COST vs Total SR
axes[0].plot(
    df["ETD"],
    df["Gap_Cost_SR_20"],
    marker="o",
    label="Gap Total SR vs Cost 20'",
    color="blue",
)
axes[0].plot(
    df["ETD"],
    df["Gap_Cost_SR_40"],
    marker="s",
    label="Gap Total SR vs Cost 40'",
    color="darkblue",
    linestyle="--",
)
axes[0].axhline(0, color="red", linestyle=":", linewidth=1)
axes[0].set_title(f"1. Gap giữa TOTAL COST và Total SR (20' & 40'){title_suffix}")
axes[0].set_ylabel("Chênh lệch")
axes[0].legend(loc="upper left")

# Biểu đồ 2: Surcharge Gap
axes[1].plot(
    df["ETD"],
    df["Gap_Surcharge_20"],
    marker="o",
    label="Gap Surcharge 20'",
    color="green",
)
axes[1].plot(
    df["ETD"],
    df["Gap_Surcharge_40"],
    marker="s",
    label="Gap Surcharge 40'",
    color="darkgreen",
    linestyle="--",
)
axes[1].axhline(0, color="red", linestyle=":", linewidth=1)
axes[1].set_title(
    f"2. Gap giữa Total BR Surcharge và Total SR Surcharge (20' & 40'){title_suffix}"
)
axes[1].set_ylabel("Chênh lệch")
axes[1].legend(loc="upper left")

# Biểu đồ 3: Base Rate Gap (OF BR vs SR)
axes[2].plot(
    df["ETD"],
    df["Gap_BaseRate_20"],
    marker="o",
    label="Gap OF BR vs SR 20'",
    color="orange",
)
axes[2].plot(
    df["ETD"],
    df["Gap_BaseRate_40"],
    marker="s",
    label="Gap OF BR vs SR 40'",
    color="darkorange",
    linestyle="--",
)
axes[2].axhline(0, color="red", linestyle=":", linewidth=1)
axes[2].set_title(
    f"3. Gap giữa OF BR và SR (Base Rate 20' & 40'){title_suffix}"
)
axes[2].set_xlabel("ETD (Thời gian)")
axes[2].set_ylabel("Chênh lệch")
axes[2].legend(loc="upper left")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
