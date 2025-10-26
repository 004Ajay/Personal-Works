import io
import time
import streamlit as st
import qrcode

st.set_page_config(page_title="Personal Info QR Generator", layout="wide")
st.title("Personal Info QR Generator")

side = st.sidebar
side.header("Your Information")
side.markdown("Enter your details — the QR code updates automatically.")

name = side.text_input(label="Name", placeholder="Ajay T Shaju")
portfolio = side.text_input(label="Portfolio", placeholder="https://portfolio.example.com")
website = side.text_input(label="Website", placeholder="https://website.example.com")
email = side.text_input(label="Email", placeholder="ajay@example.com")
github = side.text_input(label="GitHub", placeholder="https://github.com/username")
linkedin = side.text_input(label="LinkedIn", placeholder="https://linkedin.com/in/username")
extra_note = side.text_area(label="Extra Note (optional)", placeholder="")

qr_text = (
    f"{name}\r\n"
    f"Portfolio: {portfolio}\r\n"
    f"Website: {website}\r\n"
    f"Email: {email}\r\n"
    f"GitHub: {github}\r\n"
    f"LinkedIn: {linkedin}\r\n"
)
if extra_note.strip():
    qr_text += f"\r\nNote: {extra_note.strip()}"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=8,
    border=2,
)
qr.add_data(qr_text)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

buffer = io.BytesIO()
img.save(buffer, format="PNG")
qr_bytes = buffer.getvalue()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Encoded Information")
    st.text_area("Preview", qr_text, height=230)

with col2:
    st.subheader("QR Preview")
    st.image(img, caption="Scan to view info", width=300)


if st.download_button(
    label="Download QR Code",
    data=qr_bytes,
    file_name=f"personal_info_qr_{name.replace(' ', '_')}.png",
    mime="image/png",
    use_container_width=True
):
    message = st.empty()
    message.success("Downloading QR code")
    time.sleep(2)
    message.empty()
