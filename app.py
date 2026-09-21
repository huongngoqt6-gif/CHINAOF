import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(page_title="China Lane Gap Analysis", layout="wide")
st.title("📊 Biểu đồ phân tích Gap - O.F China Lane")

# 1. Đọc dữ liệu từ file Excel
file_path = "O.F China lane Analysis.xlsx"


@st.cache_data
def load_data():
  df = pd.read_excel(file_path, sheet_name="OF")
  # Làm sạch tên cột (loại bỏ khoảng trắng thừa)
  df.columns = df.columns.str.strip()
  # Chuyển đổi cột ETD sang datetime (hỗ trợ định dạng kiểu 21-Sep-26)
  df["ETD"] = pd.to_datetime(df["ETD"], errors="coerce", format="mixed")
  # Lọc bỏ các dòng lỗi ngày tháng
  df = df.dropna(subset=["ETD"])
  # Sắp xếp theo thời gian
  df = df.sort_values("ETD")
  return df


try:
  df = load_data()
except Exception as e:
  st.error(
      f"Lỗi khi đọc file Excel: {e}. Vui lòng kiểm tra lại tên file và sheet"
      " 'OF'."
  )
  st.stop()

# 2. Tạo bộ lọc theo Lane trên giao diện Streamlit
lanes = ["Tất cả"] + list(df["Lane"].unique())
selected_lane = st.selectbox("📌 Chọn Lane để lọc:", lanes)

if selected_lane != "Tất cả":
  df_filtered = df[df["Lane"] == selected_lane]
  title_suffix = f" (Lane: {selected_lane})"
else:
  df_filtered = df
  title_suffix = " (Tất cả Lanes)"

if df_filtered.empty:
  st.warning("Không có dữ liệu cho tuyến này.")
  st.stop()

# 3. Tính toán các khoảng gap theo yêu cầu
# Gap 1: TOTAL COST vs Total SR (20' & 40')
df_filtered["Gap_Cost_SR_20"] = (
    df_filtered["Total SR 20'"] - df_filtered["TOTAL COST 20'"]
)
df_filtered["Gap_Cost_SR_40"] = (
    df_filtered["Total SR 40'"] - df_filtered["TOTAL COST 40'"]
)

# Gap 2: Total BR Surcharge vs Total SR Surcharge (20' & 40')
df_filtered["Gap_Surcharge_20"] = (
    df_filtered["Total SR Surcharge 20'"] - df_filtered["Total BR surcharge 20'"]
)
df_filtered["Gap_Surcharge_40"] = (
    df_filtered["Total SR Surcharge 40'"] - df_filtered["Total BR surcharge 40'"]
)

# Gap 3: OF BR vs SR - Base Rate (20' & 40')
df_filtered["Gap_BaseRate_20"] = (
    df_filtered["SR 20'"] - df_filtered["OF BR 20'"]
)
df_filtered["Gap_BaseRate_40"] = (
    df_filtered["SR 40'"] - df_filtered["OF BR 40'"]
)

# 4. Thiết lập và vẽ biểu đồ
fig, axes = plt.subplots(3, 1, figsize=(12, 14), sharex=True)
sns.set_theme(style="whitegrid")

# Biểu đồ 1: TOTAL COST vs Total SR
axes[0].plot(
    df_filtered["ETD"],
    df_filtered["Gap_Cost_SR_20"],
    marker="o",
    label="Gap Total SR vs Cost 20'",
    color="blue",
)
axes[0].plot(
    df_filtered["ETD"],
    df_filtered["Gap_Cost_SR_40"],
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
    df_filtered["ETD"],
    df_filtered["Gap_Surcharge_20"],
    marker="o",
    label="Gap Surcharge 20'",
    color="green",
)
axes[1].plot(
    df_filtered["ETD"],
    df_filtered["Gap_Surcharge_40"],
    marker="s",
    label="Gap Surcharge 40'",
    color="darkgreen",
    linestyle="--",
)
axes[1].axhline(0, color="red", linestyle=":", linewidth=1)
axes[1].set_title(
    f"2. Gap giữa Total BR Surcharge và Total SR Surcharge (20' &"
    f" 40'){title_suffix}"
)
axes[1].set_ylabel("Chênh lệch")
axes[1].legend(loc="upper left")

# Biểu đồ 3: Base Rate Gap (OF BR vs SR)
axes[2].plot(
    df_filtered["ETD"],
    df_filtered["Gap_BaseRate_20"],
    marker="o",
    label="Gap OF BR vs SR 20'",
    color="orange",
)
axes[2].plot(
    df_filtered["ETD"],
    df_filtered["Gap_BaseRate_40"],
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

# Hiển thị biểu đồ lên ứng dụng Streamlit
st.pyplot(fig)
