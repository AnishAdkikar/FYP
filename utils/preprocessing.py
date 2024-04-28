import pandas as pd
from PyPDF2 import PdfReader 
def load_dataset(file_path='./train.csv'):
    df = pd.read_csv(file_path,usecols=[1])
    # df = pd.DataFrame({
    #     'Date': ['12.10', '13.10'],
    #     'Time': ['09.00', '19.00'],
    #     'Pressure': ['120-80', '120-80'],
    #     'State by voice': ['good', 'bad'],
    #     'Quality of sleep': ['good', 'bad'],
    #     'State by video': ['nice', 'tired'],
    #     'Final state': ['good working', 'tiered working']
    # })
    return df.head(1000)

def rows_to_text(dataframe):
    return [" ".join(str(x) for x in row) for row in dataframe.values]

def extract_text_from_pdf(path='./CRYPTO-MODULE-2.pdf'):
    reader = PdfReader(path)
    pages = len(reader.pages)
    texts = []
    for i in range(pages):
        data = reader.pages[i].extract_text().strip().split('\n')
        data = [x.strip().replace('\n','') for x in data if x not in (' ','',""," ") ]
        # texts.add(data)
        texts.extend(data)
    return texts



