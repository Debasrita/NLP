import os
import re
import pandas as pd
import shutil
import argparse
import aspose.words as aw
import fitz
from tqdm import tqdm


# install these things -- > texttract , PyMuPDF , antiword



os.makedirs('not_converted',exist_ok=True)

def read_pdf(path):
    text = ''
    doc = fitz.open(path)

    for i in range(doc.page_count):# Fixed: use range instead of enumerate to get page number

        page = doc.load_page(i)
        text += page.get_text("text")
        text = " ".join(text.split('\n')) # Fixed: use "text" parameter to get plain text from page

        text = clean_text(text)
    return text






def conv_to_pdf(source_path):
    output = "Data"

    if os.path.exists(output):
        shutil.rmtree(output)

    os.makedirs(output,exist_ok=True)
    for root, _, files in os.walk(source_path):
      for file in tqdm(files,total=len(files)):
          filename= os.path.join(root, file)
          name, ext = os.path.splitext(file)
          if ext in ['.docx', '.doc','.DOCX','.DOC']:
            try:
                doc = aw.Document(filename)
                doc.save(f'{output}/{name}.pdf')

            except:
                shutil.move(filename,'not_converted')
          elif ext in ['.pdf','.PDF']:
                new_name,ext = os.path.splitext(os.path.basename(filename))
                new_name = new_name +'_updated'+ext
                new_file_name=os.path.join(output,new_name)  
                shutil.move(filename, new_file_name)

              
            








def clean_text(text):
    # Remove non-alphanumeric characters except '.', ' ', and '\n'
    # text = re.sub(r'[^a-zA-Z0-9.\s\n]', '', text)
    text = re.sub(r"[^\w\s.@/:_\\()-,;%'+|–]", '', text)

    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)

    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    

    return text


def aspose_cleaner(text):
    text = text.replace('Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/','')
    text = text.replace('Evaluation Only. Created with Aspose.Words. Copyright 20032023 Aspose Pty Ltd.', '')
    text = text.replace('Evaluation Only. Created with Aspose.Words. Copyright 2003-2022 Aspose Pty Ltd.', '')
    text = text.replace('Created with an evaluation copy of Aspose.Words','')
    text = text.replace('To discover the full versions of our  APIs please visit: https://products.aspose.com/words/ Evaluation Only. Created with Aspose.Words. Copyright 2003-2022 Aspose Pty Ltd.','')
    return text

def read_pdf(path):
    text = ''
    doc = fitz.open(path)
    for i in range(doc.page_count):  # Fixed: use range instead of enumerate to get page number
        page = doc.load_page(i)
        text += page.get_text("text")
        text = " ".join(text.split('\n'))  # Fixed: use "text" parameter to get plain text from page
    text = clean_text(text)
  
    return text


def main(source_path,csv_path):

    dest_path = csv_path
    file_names = []
    texts = []
    for root, _, files in os.walk(source_path):
        for file in files:
          
            _, ext = os.path.splitext(file)
            if  ext in ['.pdf','.PDF']:

                file_names.append(file)
                text = read_pdf(os.path.join(root, file))
                text = aspose_cleaner(text)
                texts.append(text)
            else:
                pass


    df = pd.DataFrame({'File Name': file_names, 'Text': texts})  # Fixed: create DataFrame from file_names and texts
  
    df.to_csv(dest_path, index=False)







if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Perform CV Extraction on the folder')
    parser.add_argument('--folder', metavar='FOLDER', type=str,
                    help='name of the folder to operate on')

    args = parser.parse_args()

    folder_name = args.folder

    try:
        conv_to_pdf(folder_name)
        main('Data',f'text_dumb_{os.path.split(folder_name)[-1]}.csv')

    except Exception as e:
        print(e)





