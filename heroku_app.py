import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Load model với caching để tránh load lại nhiều lần
@st.cache_resource
def load_model():
    with open('body_fat_model_update.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# Sidebar nhập dữ liệu
st.sidebar.header("Nhập các thông số cơ thể")
Density = st.sidebar.number_input("Mật độ cơ thể (Density)", format='%.4f', min_value=0.5, max_value=1.5)
Abdomen = st.sidebar.number_input("Số đo bụng (cm)", min_value=40.0, max_value=150.0)
Chest = st.sidebar.number_input("Số đo ngực (cm)", min_value=50.0, max_value=150.0)
Hip = st.sidebar.number_input("Số đo hông (cm)", min_value=50.0, max_value=150.0)
Weight = st.sidebar.number_input("Cân nặng (kg)", min_value=20.0, max_value=200.0)
Sex = st.sidebar.selectbox("Giới tính", ['Nam', 'Nữ'])

# Xử lý khi nhấn nút dự đoán
if st.sidebar.button("Dự đoán"):
    # Kiểm tra input hợp lệ
    if any(x <= 0 for x in [Density, Abdomen, Chest, Hip, Weight]):
        st.error("⚠ Lỗi: Vui lòng nhập giá trị lớn hơn 0!")
    else:
        query = np.array([[Density, Abdomen, Chest, Hip, Weight]])
        predict = round(float(model.predict(query)[0]), 2)
        st.subheader(f"Phần trăm mỡ cơ thể ước tính: {predict}%")

        # Phân loại cơ thể
        def categorize_fat(fat, gender):
            if gender == "Nam":
                if fat < 6:
                    return "Thiếu mỡ"
                elif fat < 14:
                    return "Vận động viên"
                elif fat < 18:
                    return "Cân đối"
                elif fat < 25:
                    return "Bình thường"
                else:
                    return "Béo phì"
            else:
                if fat < 16:
                    return "Thiếu mỡ"
                elif fat < 21:
                    return "Vận động viên"
                elif fat < 25:
                    return "Cân đối"
                elif fat < 32:
                    return "Bình thường"
                else:
                    return "Béo phì"
        
        category = categorize_fat(predict, Sex)
        st.subheader(f"Phân loại cơ thể: {category}")
        
        # Vẽ biểu đồ
        labels = ["Chỉ Số Mỡ","Thiếu mỡ", "Vận động viên", "Cân đối", "Bình thường", "Béo phì"]
        ranges = [[0, 5], [5, 13], [13, 17], [17, 24], [24, 50]] if Sex == "Nam" else [[0, 15], [16, 20], [21, 24], [25, 31], [32, 50]]
        colors = ['blue', 'green', 'yellow', 'orange', 'red']
        
        fig, ax = plt.subplots(figsize=(6, 3))
        for i, (low, high) in enumerate(ranges):
            ax.barh([""], [high - low], left=low, color=colors[i])
        ax.axvline(predict, color='black', linestyle='dashed', linewidth=2)
        ax.set_xlabel("Phần trăm mỡ cơ thể")
        
        # Điều chỉnh vị trí legend
        fig.legend(labels, 
                loc='upper left', 
                bbox_to_anchor=(0.05, 1.15),  # Di chuyển legend lên cao hơn
                ncol=3,  # Có thể chia thành nhiều cột nếu cần
                frameon=False)  # Bỏ khung để trông gọn hơn

        # Thêm padding phía trên để tránh legend che mất đồ thị
        plt.tight_layout(rect=[0, 0, 1, 0.9])  # Giảm không gian phía trên

        st.pyplot(fig)