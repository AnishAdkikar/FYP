import pandas as pd
from PyPDF2 import PdfReader 
# import sys
# sys.path.append("..")
from utils.helper import multi_thread
def load_dataset(file_path='./resources/medical_tc_test.csv'):
    # df = pd.read_csv(file_path,usecols=[1])
    # df = pd.DataFrame({
    #     'Date': ['12.10', '13.10'],
    #     'Time': ['09.00', '19.00'],
    #     'Pressure': ['120-80', '120-80'],
    #     'State by voice': ['good', 'bad'],
    #     'Quality of sleep': ['good', 'bad'],
    #     'State by video': ['nice', 'tired'],
    #     'Final state': ['good working', 'tiered working']
    # })
    df = pd.read_csv(file_path)
    # df = pd.read_csv(r"k:/FYP/backup/sql/strings.csv")
    df = pd.DataFrame(df, columns=['condition_label', 'medical_abstract'])

    df.replace(to_replace =1,  
                 value = "Neoplasms $$$$",  
                  inplace = True) 
    df.replace(to_replace =2,  
                 value = "Digestive system diseases $$$$",  
                  inplace = True) 
    df.replace(to_replace =3,  
                 value = "Nervous system diseases $$$$",  
                  inplace = True) 
    df.replace(to_replace =4,  
                 value = "Cardiovascular diseases $$$$",  
                  inplace = True) 
    df.replace(to_replace =5,  
                 value = "General pathological conditions $$$$",  
                  inplace = True) 
    
    return df
    

def rows_to_text(dataframe):
    return [" ".join(str(x) for x in row) for row in dataframe.values]

def extract_text_from_pdf(path='./resources/CRYPTO-MODULE-2.pdf'):
    reader = PdfReader(path)
    pages = len(reader.pages)
    texts = []
    for i in range(pages):
        data = reader.pages[i].extract_text().strip().split('\n')
        data = [x.strip().replace('\n','') for x in data if x not in (' ','',""," ") ]
        # texts.add(data)
        texts.extend(data)
    return texts



