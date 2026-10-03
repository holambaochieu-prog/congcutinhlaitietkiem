import streamlit as st
st.image("LOGO.jpg")
# Cấu hình trang
st.set_page_config(page_title="Tính Lãi Tiết Kiệm", page_icon="🏦", layout="centered")

st.title("🏦 Ứng Dụng Tính Lãi Gửi Tiết Kiệm_HỒ LÂM BẢO CHIÊU🤲🤟")
st.markdown("📝 **Nhập các thông tin bên dưới để tính toán số tiền lãi bạn sẽ nhận được.**")

# Tạo form nhập liệu
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        so_tien_gui = st.number_input("💵 Số tiền gửi (VNĐ):", min_value=0, value=100000000, step=1000000)
        ky_han = st.number_input("⏳ Kỳ hạn gửi (tháng):", min_value=1, value=12, step=1)
        
    with col2:
        lai_suat = st.number_input("📈 Lãi suất (%/năm):", min_value=0.0, value=6.0, step=0.1, format="%.2f")
        hinh_thuc = st.selectbox(
            "📋 Hình thức nhận lãi:", 
            ("Cuối kỳ", "Hàng tháng", "Hàng quý")
        )

# Hàm định dạng tiền tệ (hiển thị dấu chấm ngăn cách hàng nghìn)
def format_vnd(amount):
    return f"{amount:,.0f}".replace(",", ".") + " ₫"

# Tính toán
if st.button("🧮 Tính Toán Ngay", type="primary"):
    # Lãi suất mỗi tháng
    lai_suat_thang = (lai_suat / 100) / 12
    
    # Tổng tiền lãi
    tong_tien_lai = so_tien_gui * lai_suat_thang * ky_han
    
    # Tổng gốc và lãi
    tong_goc_lai = so_tien_gui + tong_tien_lai
    
    # Tính tiền lãi định kỳ dựa trên hình thức
    if hinh_thuc == "Hàng tháng":
        tien_lai_dinh_ky = so_tien_gui * lai_suat_thang
        nhan_dinh_ky_label = "📅 Lãi nhận hàng tháng"
    elif hinh_thuc == "Hàng quý":
        tien_lai_dinh_ky = so_tien_gui * lai_suat_thang * 3
        nhan_dinh_ky_label = "📆 Lãi nhận hàng quý"
    else:
        tien_lai_dinh_ky = tong_tien_lai
        nhan_dinh_ky_label = "🎯 Lãi nhận cuối kỳ"

    # Hiển thị kết quả
    st.divider()
    st.subheader("📊 Kết Quả Chi Tiết")
    
    # Dùng columns để hiển thị các chỉ số (metrics)
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.metric(label=nhan_dinh_ky_label, value=format_vnd(tien_lai_dinh_ky))
        
    with res_col2:
        st.metric(label="💸 Tổng tiền lãi", value=format_vnd(tong_tien_lai))
        
    with res_col3:
        st.metric(label="💰 Tổng gốc + lãi", value=format_vnd(tong_goc_lai))
        
    # Lưu ý nhỏ nếu chọn hàng quý nhưng kỳ hạn không chia hết cho 3
    if hinh_thuc == "Hàng quý" and ky_han % 3 != 0:
        st.info(f"⚠️ **Lưu ý:** Kỳ hạn {ky_han} tháng không chia hết cho một quý (3 tháng). Số tiền lãi hàng quý hiển thị là mức nhận cố định mỗi 3 tháng. Kỳ trả lãi cuối cùng sẽ được tính theo số tháng lẻ còn lại.")
