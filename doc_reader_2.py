import os
import re
import pandas as pd
import fitz
# import docx
# import textract
import shutil
import subprocess
import argparse



# install these things -- > texttract , PyMuPDF , antiword

os.makedirs('not_converted',exist_ok=True)


def conv_to_pdf(source_path):
    output = "Data"
    os.makedirs(output,exist_ok=True)
    for root, _, files in os.walk(source_path):
      for file in files:
          filename= os.path.join(root, file)
          _, ext = os.path.splitext(file)
          if ext in ['.docx', '.doc']:
            try:
                subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', filename, '--outdir', output_path],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=None)            
            
            
            
            except:
                shutil.move(filename,'not_converted')
          elif ext in ['.pdf','.PDF']:
                new_name,ext = os.path.splitext(os.path.basename(filename))
                new_name = new_name +'_updated'+ext
                new_file_name=os.path.join(output,new_name)  
                shutil.move(filename, new_file_name)

              
            








def clean_text(text):
    # Remove non-alphanumeric characters except '.', ' ', and '\n'
    text = re.sub(r'[^a-zA-Z0-9.\s\n]', '', text)

    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)

    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)

    return text





# def read_doc(path):
#     text = textract.process(path)
#     text = clean_text(text.decode('utf-8'))
   
#     return text


def read_pdf(path):
    text = ''
    doc = fitz.open(path)
    for i in range(doc.page_count):  # Fixed: use range instead of enumerate to get page number
        page = doc.load_page(i)
        text += page.get_text("text")  # Fixed: use "text" parameter to get plain text from page
    text = clean_text(text)
  
    return text


def main(source_path):

    dest_path = 'TextDump.csv'
    file_names = []
    texts = []
    for root, _, files in os.walk(source_path):
        for file in files:

            _, ext = os.path.splitext(file)
            if  ext in ['.pdf','.PDF']:
            #     text = ''

            #     try:
            #         text = read_doc(os.path.join(root, file))
            #     except:
            #         shutil.move(os.path.join(root, file),'not_converted')
            #     if text != '':
            #         file_names.append(file)
            #         texts.append(text)
            # elif ext == '.pdf':
                file_names.append(file)
                text = read_pdf(os.path.join(root, file))
                texts.append(text)
            else:
                pass
                # raise NotImplementedError("This code can read '.doc', '.docx', or '.pdf' files only")

    df = pd.DataFrame({'File Name': file_names, 'Text': texts})  # Fixed: create DataFrame from file_names and texts
    print(df.head())
    df.to_csv(dest_path, index=False)







if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Perform CV Extraction on the folder')
    parser.add_argument('--folder', metavar='FOLDER', type=str,
                    help='name of the folder to operate on')

    args = parser.parse_args()

    folder_name = args.folder

    try:
        conv_to_pdf(folder_name)
        main('Data')

    except Exception as e:
        print(e)
