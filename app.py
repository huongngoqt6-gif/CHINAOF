import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = "O.F China lane Analysis.xlsx"

# Tự động dò tìm tên sheet an toàn
xls = pd.ExcelFile(file_path)
sheet_to_use = None

for s in xls.sheet_names:
  # So sánh không phân biệt hoa thường và loại bỏ khoảng trắng thừa
  if s.strip().upper() == "OF":
    sheet_to_use = s
    break

# Nếu tìm thấy thì dùng, nếu không thì lấy sheet đầu tiên (index = 0)
if sheet_to_use:
  df = pd.read_excel(file_path, sheet_name=sheet_to_use)
else:
  df = pd.read_excel(file_path, sheet_name=0)

# 2. Tùy chọn lọc theo Lane (Tuyến)
# Thay đổi giá trị bên dưới thành tên Lane bạn muốn lọc, hoặc để None nếu muốn xem toàn bộ
filter_lane = None  # Ví dụ: filter_lane = "CN-SGN"

if filter_lane:
  df = df[df["Lane"] == filter_lane]

# Chuyển đổi cột ETD sang định dạng datetime và sắp xếp theo thời gian
df["ETD"] = pd.to_datetime(df["ETD"])
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
