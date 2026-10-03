import streamlit as st

# Cấu hình trang (Lệnh này bắt buộc phải nằm trên cùng của Streamlit)
st.set_page_config(page_title="Tính Lãi Tiết Kiệm", page_icon="🏦", layout="centered")

st.image("LOGO.jpg")

st.title("🏦 Ứng Dụng Tính Lãi Gửi Tiết Kiệm_HỒ LÂM BẢO CHIÊU🤲🤟")
st.markdown("📝 **Chọn kỳ hạn và nhập số tiền gửi, hệ thống sẽ tự động tham chiếu lãi suất và so sánh Lãi Đơn & Lãi Kép.**")

# BẢNG LÃI SUẤT CỐ ĐỊNH (Kỳ hạn theo tháng -> Lãi suất %/năm)
BANG_LAI_SUAT = {
    1: 3.0,
    3: 3.5,
    6: 4.5,
    9: 5.0,
    12: 6.0,
    18: 6.5,
    24: 7.0,
    36: 7.2
}

# TẠO FORM NHẬP LIỆU
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        so_tien_gui = st.number_input("💵 Số tiền gửi (VNĐ):", min_value=0, value=100000000, step=1000000)
        
        # Dropdown chọn kỳ hạn (lấy các số tháng từ bảng lãi suất ở trên)
        ky_han = st.selectbox(
            "⏳ Chọn kỳ hạn gửi (tháng):", 
            options=list(BANG_LAI_SUAT.keys()),
            format_func=lambda x: f"{x} tháng"
        )
        
    with col2:
        # Tự động lấy lãi suất từ bảng dựa trên kỳ hạn đã chọn
        lai_suat = BANG_LAI_SUAT[ky_han]
        
        # Hiển thị lãi suất dạng đọc (không cho người dùng sửa)
        st.text_input("📈 Lãi suất tự tham chiếu (%/năm):", value=f"{lai_suat}%", disabled=True)
        
        # Chọn chu kỳ ghép lãi (dùng để tính lãi kép)
        chu_ky_ghep_lai = st.selectbox(
            "🔄 Chu kỳ nhập gốc (Cho Lãi Kép):", 
            ("Hàng tháng", "Hàng quý", "Hàng năm")
        )

# Hàm định dạng tiền tệ
def format_vnd(amount):
    return f"{amount:,.0f}".replace(",", ".") + " ₫"

# XỬ LÝ TÍNH TOÁN
if st.button("🧮 Tính Toán Ngay", type="primary"):
    
    # Chuẩn bị dữ liệu để tính toán
    t_nam = ky_han / 12           # Đổi kỳ hạn tháng ra năm
    r = lai_suat / 100            # Lãi suất dạng thập phân
    
    # --- TÍNH LÃI ĐƠN ---
    lai_don = so_tien_gui * r * t_nam
    tong_don = so_tien_gui + lai_don
    
    # --- TÍNH LÃI KÉP ---
    if chu_ky_ghep_lai == "Hàng tháng":
        n = 12
    elif chu_ky_ghep_lai == "Hàng quý":
        n = 4
    else: # Hàng năm
        n = 1
        
    tong_kep = so_tien_gui * ((1 + r/n)**(n * t_nam))
    lai_kep = tong_kep - so_tien_gui

    # HIỂN THỊ KẾT QUẢ SO SÁNH
    st.divider()
    st.subheader("📊 Bảng So Sánh Chi Tiết")
    
    col_don, col_kep = st.columns(2)
    
    with col_don:
        st.info("### 🟢 Lãi Đơn")
        st.markdown("*(Tiền lãi không nhập vào gốc)*")
        st.metric(label="💸 Tiền lãi nhận được", value=format_vnd(lai_don))
        st.metric(label="💰 Tổng tiền (Gốc + Lãi)", value=format_vnd(tong_don))
        
    with col_kep:
        st.success("### 🚀 Lãi Kép")
        st.markdown(f"*(Lãi sinh lãi - Ghép lãi **{chu_ky_ghep_lai.lower()}**)*")
        st.metric(label="💸 Tiền lãi nhận được", value=format_vnd(lai_kep))
        st.metric(label="💰 Tổng tiền (Gốc + Lãi)", value=format_vnd(tong_kep))
        
    # Hiển thị độ chênh lệch
    chenh_lech = lai_kep - lai_don
    if chenh_lech > 0:
        st.divider()
        st.write(f"💡 **Phân tích:** Nhờ sức mạnh của lãi kép, bạn sẽ nhận được nhiều hơn **{format_vnd(chenh_lech)}** so với lãi đơn thông thường sau {ky_han} tháng.")
