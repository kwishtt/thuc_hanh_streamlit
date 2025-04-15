# Đinh Ngọc Khuê - 2321050065

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Thiết lập cấu hình trang
st.set_page_config(page_title="Phân tích dữ liệu phim", layout="wide")

# Tiêu đề
st.title("Phân tích dữ liệu phim")
st.markdown("### Đinh Ngọc Khuê - 2321050065")

# Thiết lập sidebar
st.sidebar.title("Tùy chọn Phân tích")

# Đọc dữ liệu trực tiếp không sử dụng cache
url = "https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv"
movies_data = pd.read_csv(url)

# Bước loại bỏ dữ liệu thiếu
cleaned_data = movies_data.dropna()

# Sidebar - Tùy chọn chế độ hiển thị dữ liệu
data_mode = st.sidebar.radio(
    "Chọn dữ liệu để phân tích:",
    ["Dữ liệu gốc", "Dữ liệu đã làm sạch"]
)

# Sidebar - Chọn cột để hiển thị
if data_mode == "Dữ liệu gốc":
    current_data = movies_data
else:
    current_data = cleaned_data

# Hiển thị thông tin tóm tắt về dữ liệu
st.write("### Thông tin về tập dữ liệu")
st.write(f"Số dòng ban đầu: {len(movies_data)}, Số dòng sau khi loại bỏ dữ liệu thiếu: {len(cleaned_data)}")

# Thanh kéo để hiển thị số dòng dữ liệu
num_rows = st.slider("Số dòng dữ liệu hiển thị:", min_value=1, max_value=min(50, len(current_data)), value=5)
st.dataframe(current_data.head(num_rows))

# Sidebar - Chọn loại phân tích
analysis_type = st.sidebar.selectbox(
    "Chọn loại phân tích:",
    ["Ngân sách theo thể loại", "Phân tích theo năm", "Top phim", "Thống kê"]
)

# Tùy chọn màu sắc biểu đồ
chart_color = st.sidebar.color_picker("Chọn màu cho biểu đồ:", "#800000")  # Màu mặc định là maroon

# Phân tích dựa trên lựa chọn
if analysis_type == "Ngân sách theo thể loại":
    st.write("## Ngân sách trung bình của phim theo thể loại")
    
    # Sidebar - Sắp xếp theo
    sort_option = st.sidebar.radio(
        "Sắp xếp theo:",
        ["Không sắp xếp", "Tăng dần", "Giảm dần"]
    )
    
    # Tính toán ngân sách trung bình theo thể loại
    avg_budget = current_data.groupby('genre')['budget'].mean().round()
    
    # Sắp xếp nếu được chọn
    if sort_option == "Tăng dần":
        avg_budget = avg_budget.sort_values()
    elif sort_option == "Giảm dần":
        avg_budget = avg_budget.sort_values(ascending=False)
        
    avg_budget = avg_budget.reset_index()
    genre = avg_budget['genre']
    avg_bud = avg_budget['budget']
    
    # Vẽ biểu đồ cột
    fig = plt.figure(figsize=(19, 10))
    plt.bar(genre, avg_bud, color=chart_color)
    plt.xlabel('genre')
    plt.ylabel('budget')
    plt.title('Matplotlib Bar Chart Showing the Average Budget of Movies in Each Genre')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Hiển thị biểu đồ
    st.pyplot(fig)
    
    # Hiển thị dữ liệu dạng bảng
    st.write("### Bảng dữ liệu ngân sách trung bình theo thể loại")
    st.dataframe(avg_budget)

elif analysis_type == "Phân tích theo năm":
    st.write("## Xu hướng phim theo năm")
    
    # Trích xuất năm từ cột released nếu chưa có
    if 'year' not in current_data.columns:
        current_data['year'] = pd.to_datetime(current_data['released'], errors='coerce').dt.year
    
    # Sidebar - Chọn năm bắt đầu và kết thúc
    min_year = int(current_data['year'].min()) if not pd.isna(current_data['year'].min()) else 1986
    max_year = int(current_data['year'].max()) if not pd.isna(current_data['year'].max()) else 2016
    
    year_range = st.sidebar.slider(
        "Chọn khoảng năm:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Lọc dữ liệu theo năm
    filtered_data = current_data[(current_data['year'] >= year_range[0]) & 
                                (current_data['year'] <= year_range[1])]
    
    # Đếm số phim theo năm
    films_per_year = filtered_data.groupby('year').size().reset_index(name='count')
    
    # Vẽ biểu đồ đường
    fig = plt.figure(figsize=(19, 10))
    plt.plot(films_per_year['year'], films_per_year['count'], marker='o', color=chart_color)
    plt.xlabel('Năm phát hành')
    plt.ylabel('Số lượng phim')
    plt.title('Số lượng phim phát hành theo năm')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Hiển thị biểu đồ
    st.pyplot(fig)

elif analysis_type == "Top phim":
    st.write("## Top phim theo tiêu chí")
    
    # Sidebar - Chọn tiêu chí
    criteria = st.sidebar.selectbox(
        "Chọn tiêu chí:",
        ['score', 'budget', 'gross', 'runtime']
    )
    
    # Sidebar - Chọn số lượng hiển thị
    top_n = st.sidebar.slider("Số lượng phim hiển thị:", 5, 20, 10)
    
    # Lọc dữ liệu không null cho tiêu chí đã chọn
    valid_data = current_data.dropna(subset=[criteria])
    
    # Top phim theo tiêu chí
    if st.sidebar.checkbox("Lấy phim có giá trị cao nhất", True):
        top_films = valid_data.nlargest(top_n, criteria)
    else:
        top_films = valid_data.nsmallest(top_n, criteria)
    
    # Hiển thị danh sách
    st.write(f"### Top {top_n} phim theo {criteria}")
    st.dataframe(top_films[['name', 'genre', 'year', criteria]])
    
    # Vẽ biểu đồ
    fig = plt.figure(figsize=(19, 10))
    plt.barh(top_films['name'], top_films[criteria], color=chart_color)
    plt.xlabel(criteria)
    plt.ylabel('Tên phim')
    plt.title(f'Top {top_n} phim theo {criteria}')
    plt.tight_layout()
    
    # Hiển thị biểu đồ
    st.pyplot(fig)

elif analysis_type == "Thống kê":
    st.write("## Thống kê dữ liệu phim")
    
    # Sidebar - Chọn cột thống kê
    columns_for_stats = st.sidebar.multiselect(
        "Chọn các cột để xem thống kê:",
        options=[col for col in current_data.columns if current_data[col].dtype in ['int64', 'float64']],
        default=['budget', 'score', 'gross']
    )
    
    if columns_for_stats:
        # Hiển thị thống kê
        st.write("### Thống kê mô tả")
        st.dataframe(current_data[columns_for_stats].describe())
        
        # Tùy chọn biểu đồ phân phối
        if st.sidebar.checkbox("Hiển thị biểu đồ phân phối"):
            col_for_hist = st.sidebar.selectbox("Chọn cột để hiển thị phân phối:", columns_for_stats)
            
            # Vẽ histogram
            fig = plt.figure(figsize=(12, 6))
            plt.hist(current_data[col_for_hist].dropna(), bins=30, color=chart_color, alpha=0.7)
            plt.xlabel(col_for_hist)
            plt.ylabel('Tần suất')
            plt.title(f'Phân phối của {col_for_hist}')
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            
            # Hiển thị biểu đồ
            st.pyplot(fig)

# Thêm thông tin tác giả vào sidebar
st.sidebar.markdown("---")
st.sidebar.info("Thành Viên: \nĐinh Ngọc Khuê - 2321050065 \nPhan Văn Huy -")
