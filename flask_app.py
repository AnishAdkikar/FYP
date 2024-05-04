from flask import Flask
import random
import requests
import threading
import utils.preprocessing as preprocessing
from utils.helper import multi_thread
from config import API_TOKEN

app = Flask(__name__)

@app.route('/test')
def testing():
    length = 50
    if length<10000:
        M = 10
        efconstruction = 2*M
    else:
        M = random.randint(50, 100)
        efconstruction = 2*M
    userData = {
        'userID':'w',
        'M':str(M),
        'efConstruction':str(efconstruction)
    }
    res2 = requests.post(url='http://127.0.0.1:8080/connection', json=userData)

    if res2.status_code != 200:
        return "Connection Error"
    
    df = preprocessing.load_dataset()
    texts = preprocessing.rows_to_text(df)
    # texts = preprocessing.extract_text_from_pdf()
    print(len(texts))
    vectors = {}
    batch_size = len(texts)//100
    batches = [texts[i:i+batch_size] for i in range(0,len(texts),batch_size)]
    thread_list = []
    for i in batches:
        t = threading.Thread(target=multi_thread,args=(i,vectors))
        thread_list.append(t)
    for j in thread_list:
        j.start()
    for j in thread_list:
        j.join()
    
    print(len(vectors))
    # return vectors

    addData = {
        'userID':'naya',
        'data':vectors
    }
    res3 = requests.post(url='http://127.0.0.1:8080/add-data', json=addData)
    if res3.status_code != 200:
        return "Error while adding"

    return "Addition of data success"

@app.route('/test_search')
def test_search():
    length = 50
    if length<10000:
        M = 10
        efsearch = M
    else:
        M = random.randint(50, 100)
        efsearch = M
    header={'Content-Type': 'application/json','Authorization': API_TOKEN}
    query = '''Human papillomavirus in women with vulvar intraepithelial neoplasia III. Untreated cases of vulvar intraepithelial neoplasia (VIN) III may progress to invasive vulvar carcinoma. Tissues from 29 New Zealand women with VIN III were examined for the presence of human papillomavirus (HPV) types 6, 11, 16 and 18 by in situ hybridization and polymerase chain reaction. HPV 16, the only HPV type detected in the lesions, was identified in about half the cases. HPV-positive women were younger than HPV-negative women, and their lesions displayed koilocytosis more often. In four of five cases in which there was a progression to invasive cancer, HPV 16 was detected in both the VIN III and invasive cancer tissue.'''
    payload1 = {   
        "model":"text-embedding-3-large",
        "input":query
    }
    res4 = requests.post(url='https://api.openai.com/v1/embeddings', json=payload1,headers=header)
    searchData = {
        'userID':'naya',
        'K':3,
        'ef': efsearch,
        'data':res4.json()["data"][0]["embedding"] 
    }
    res5 = requests.post(url='http://127.0.0.1:8080/search', json=searchData)
    ans = []
    for i in res5.json():
        ans.append(i.split('||||')[0])
    return ans


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7900,debug=True)