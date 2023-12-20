import streamlit as st
import numpy as np
import os
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import cv2

import qrcode
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10,border=14)

from PIL import Image
def load_image(img):
    im = Image.open(img)
    return im


def main():
    menu = ["Home", "DecodeQR", "About"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home Page")

        with st.form(key='myqr_form'):
            raw_text = st.text_area("Text Here")
            submit_button = st.form_submit_button("Generate")
        
        if submit_button:
            col1, col2 = st.columns(2)
            with col1:
                qr.add_data(raw_text)
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color="white")
                img_filename = 'generate_image_{}.png'.format(timestr)
                path_for_image = os.path.join('image_folder', img_filename)
                img.save(path_for_image)

                final_img = load_image(path_for_image)
                st.image(final_img)


            with col2:
                st.info("Original Text")
                



    elif choice == "DecodeQR":
        st.subheader("Decode QRCode")
        image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        if image_file is not None:
                    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
                    opencv_image = cv2.imdecode(file_bytes,1)

                    c1,c2 = st.columns(2)

                    with c1:
                        st.image(opencv_image)
                    
                    with c2:
                        st.info("Decoded QR code")
                        det = cv2.QRCodeDetector()
                        retval, points, straight_qrcode = det.detectAndDecode(opencv_image)
                        st.write(retval)
                        st.write(points)
                        st.write(straight_qrcode)
    else:
        st.subheader("About QRCode App")


if __name__ == '__main__':
    main()