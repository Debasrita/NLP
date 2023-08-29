#pip install streamlit
#pip install PyMuPDF


import streamlit as st
import os
import fitz
from PIL import Image
import pandas as pd
import csv

st.header("Automatic CV Parser")
os.makedirs('static',exist_ok=True)

csv_path = 'TextDump.csv'
# read_csv here
df = pd.read_csv('TextDump.csv')

st.subheader(":red[Only PDF files supported]")
agree = st.checkbox('View Image?')
uploadedfile = st.file_uploader("Choose a file",type=['pdf'],accept_multiple_files=True)
if st.button("Submit"): 
    if uploadedfile:
        for uploads in uploadedfile:
            st.subheader(f':blue[Pdf name] : {uploads.name}')
            fname, file_extension = os.path.splitext(uploads.name)
            with open(f"static/{fname}{file_extension}", "wb") as f:
                f.write(uploads.read())
            doc = fitz.open(f'static/{uploads.name}')

            text = ""
            zoom_x = 2.0  # horizontal zoom
            zoom_y = 2.0  # vertical zoom
            mat = fitz.Matrix(zoom_x, zoom_y)
            for i , page in enumerate(doc):

                page = doc.load_page(i)
                
                pixmap = page.get_pixmap()
                image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
                if agree:
                    st.text(f'Page number : {i+1}')
                    st.image(image)
                text += str(page.get_text())
                tx = " ".join(text.split('\n'))
                string_encode = tx.encode("ascii", "ignore")
                tx = string_encode.decode()
            
                st.subheader(":green[Pdf Text] :")
                st.markdown(tx)

            with open(csv_path, 'a', newline='') as csvfile:
                nm=uploads.name
                if nm not in df['Filename'].values:
                    my_writer = csv.writer(csvfile, delimiter = ',')
                    aa=[nm,tx]
                    my_writer.writerow(aa)
                    
                    st.text("Written to file")
                else:
                    st.text("Already exists in file")
                    csvfile.close()
          

    

        

