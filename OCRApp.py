import streamlit as st
import os
import fitz
from PIL import Image
import pandas as pd
import csv
st.header("Automatic CV Parser")
os.makedirs('static',exist_ok=True)
st.text("Only PDF files supported")
uploadedfile = st.file_uploader("Choose a file",type=['pdf'])
if st.button("Submit"):
    if uploadedfile is not None:
        fname, file_extension = os.path.splitext(uploadedfile.name)
        with open(f"static/{fname}{file_extension}", "wb") as f:
            f.write(uploadedfile.read())
    st.success("File has been uploaded and saved successfully.")
    doc = fitz.open(f'static/{uploadedfile.name}')
    num_pages = doc.page_count
    page_number = st.selectbox("Select page to save as image", range(1, num_pages + 1))
    page = doc.load_page(page_number - 1)
    pixmap = page.get_pixmap()
    image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    st.image(image)
    text = ""
    zoom_x = 2.0# horizontal zoom
    zoom_y = 2.0# vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)
    for page in doc:

        text = text + str(page.get_text())
        txx = " ".join(text.split('\n'))
        string_encode = txx.encode("ascii", "ignore")
        tx = string_encode.decode()
    st.markdown(tx)
    ff="C:/Users/Codelogic/OneDrive - CODELOGICX TECHNOLOGIES PVT LTD/CV Dump/TextDump.csv"
    filenn=open(ff)
    df=pd.read_csv(filenn)
    filenn.close()
    with open(ff, 'a', newline='') as csvfile:
        nm=uploadedfile.name
        if nm not in df['Filename'].values:
            my_writer = csv.writer(csvfile, delimiter = ',')
            aa=[nm,tx]
            my_writer.writerow(aa)
            
            st.text("Written to file")
        else:
            st.text("Already exists in file")
            csvfile.close()
    
    