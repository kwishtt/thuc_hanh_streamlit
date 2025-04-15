import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Thiết lập cấu hình trang
st.set_page_config(page_title="Biểu đồ Hộp", layout="centered")

# Tiêu đề
st.title("Biểu đồ hộp phân tích dữ liệu Iris")
st.write("Biểu đồ hộp hiển thị phân phối dữ liệu của các đặc trưng hoa Iris theo từng loài.")

# Tải dữ liệu iris
iris = sns.load_dataset('iris')

# Hiển thị thông tin tùy chỉnh
st.sidebar.header("Tùy chỉnh biểu đồ")

feature_var = st.sidebar.selectbox(
    "Dữ liệu cần phân tích:",
    [('petal_length', 'Chiều dài cánh hoa'), 
     ('petal_width', 'Chiều rộng cánh hoa'),
     ('sepal_length', 'Chiều dài đài hoa'), 
     ('sepal_width', 'Chiều rộng đài hoa')],
    format_func=lambda x: x[1]
)

show_means = st.sidebar.checkbox("Hiển thị giá trị trung bình", value=True)
show_outliers = st.sidebar.checkbox("Hiển thị ngoại lệ", value=True)

# Thêm checkbox kiểm tra dữ liệu thiếu/sai
check_missing_data = st.sidebar.checkbox("Hiển thị dữ liệu thiếu", value=False)
if check_missing_data:
    st.sidebar.write("Kiểm tra dữ liệu thiếu:")
    missing_data = iris.isnull().sum()
    st.sidebar.dataframe(missing_data.rename("Số lượng"))


# Màu sắc cho hộp
box_color = st.sidebar.selectbox(
    "Chọn màu cho hộp:",
    ["lightblue", "lightgreen", "lightpink", "lightyellow", "lightcoral"],
    index=0
)

# Chuẩn bị dữ liệu
species = iris['species'].unique()
feature_data = []

for s in species:
    rows_of_current_species = iris[iris['species'] == s]
    feature_values = rows_of_current_species[feature_var[0]]
    feature_data.append(feature_values)
    
# Hiển thị thông tin dữ liệu với thanh kéo để chọn số dòng
with st.expander("Xem thông tin dữ liệu"):
    num_rows = st.slider("Số dòng hiển thị:", min_value=1, max_value=len(iris), value=5, step=1)
    st.write(f"{num_rows} dòng đầu tiên của dữ liệu:")
    st.dataframe(iris.head(num_rows))
    
    st.write(f"Thống kê về {feature_var[1]} theo loài:")
    stats_df = iris.groupby('species')[feature_var[0]].describe()
    st.dataframe(stats_df)

# Vẽ biểu đồ hộp
st.subheader(f"Biểu đồ hộp của {feature_var[1]}")
fig, ax = plt.subplots(figsize=(10, 6))
boxplot = plt.boxplot(feature_data, 
          vert=True, 
          patch_artist=True,
          boxprops=dict(facecolor=box_color, color='blue'),  
          tick_labels=species, 
          showmeans=show_means, 
          medianprops=dict(color='red', linewidth=2),
          showfliers=show_outliers,
          flierprops=dict(marker='x', markerfacecolor='red', markersize=8)
         )

plt.title(f'Biểu đồ hộp của {feature_var[1]}')
plt.xlabel('Loài hoa')
plt.ylabel(feature_var[1])
st.pyplot(fig)