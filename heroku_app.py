import pandas as pd
import numpy as np
import pickle
import streamlit as st

file = open('body_fat_model.pkl', 'rb')
dct = pickle.load(file)
file.close()


data = pd.read_csv('trained_data.csv')

st.title('Ứng Dụng Dự Đoán Phần Trăm Mỡ Trong Cơ Thể')

# Nhập vào chỉ số Mật độ cơ thể ( Density ) xác định bằng cách lấy KL/Thể Tích cơ thể
Density = float(st.number_input('Nhập vào chỉ số Mật độ cơ thể (Density)', format='%.4f'))

# Nhập số đo bụng 

Abdomen = float(st.number_input('Nhập vào số đo bụng (Abdomen) '))

# Nhập số đo ngực

Chest = float(st.number_input('Nhập vào số đo ngực (Chest) '))

# Nhập số đo hông

Hip = float(st.number_input('Nhập vào số đo hông (Hip) '))

# Nhập cân nặng

Weight = float(st.number_input('Nhập vào số cân nặng (Weight) '))

# Chọn giới tính của bạn 
Sex = st.selectbox('Giới Tính', ['Nam', 'Nữ'])

# Đánh giá cơ thể theo giới tính
def Boy(fat):
    if fat < 6:
        st.title('Bạn Bị Gầy (Thiếu Mỡ)')
    elif fat < 14 :
        st.title('Bạn Có Cơ Thể Chuẩn Của Một Vận Động Viên')
    elif fat < 18:
        st.title('Bạn Có Một Cơ Thể Đẹp,Cân Đối')
    elif fat < 25:
        st.title('Cơ Thể Của Bạn Ở Mức Bình Thường')
    else:
        st.title('Cơ Thể Của Bạn Đang Bị Béo Phì')

def Girl(fat):
    if fat < 16:
        st.title('Bạn Bị Gầy (Thiếu Mỡ)')
    elif fat < 21 :
        st.title('Bạn Có Cơ Thể Chuẩn Của Một Vận Động Viên')
    elif fat < 25:
        st.title('Bạn Có Một Cơ Thể Đẹp,Cân Đối')
    elif fat < 32:
        st.title('Cơ Thể Của Bạn Ở Mức Bình Thường')
    else:
        st.title('Cơ Thể Của Bạn Đang Bị Béo Phì')

# Button dự đoán
if st.button('Dự Đoán Phần Trăm Mỡ Cơ Thể'):

    query = np.array([Density, Abdomen, Chest, Hip, Weight])

    query = query.reshape(1,5)

    predict = round(float(dct.predict(query)[0]),2)

    st.title("Khối Lượng Mỡ Trong Cơ Thể Bạn Chiếm " + str(predict) +"%")

    if Sex == 'Nam':
        Boy(predict)
    else:
        Girl(predict)


