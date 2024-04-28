from flask import Flask, jsonify
import requests
import threading
# from flask_mysqldb import MySQL
import utils.preprocessing as preprocessing
from helper import multi_thread
from config import API_TOKEN
app = Flask(__name__)

@app.route('/test')
def testing():
    length = 50
    if length<10000:
        M = 10
        efconstruction = 2*M
        efsearch = M
    else:
        M = random.randint(50, 100)
        efconstruction = 2*M
        efsearch = M
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
    batch_size = len(texts)//10
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
        'userID':'w',
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
        efconstruction = 2*M
        efsearch = M
    else:
        M = random.randint(50, 100)
        efconstruction = 2*M
        efsearch = M
    header={'Content-Type': 'application/json','Authorization': API_TOKEN}
    query = 'common high-affinity IL-3/GM-CSF binding sites'
    payload1 = {   
        "model":"text-embedding-3-large",
        "input":query
    }
    res4 = requests.post(url='https://api.openai.com/v1/embeddings', json=payload1,headers=header)
    searchData = {
        'userID':'w',
        'K':10,
        'ef': efsearch,
        'data':res4.json()["data"][0]["embedding"] 
    }
    res5 = requests.post(url='http://127.0.0.1:8080/search', json=searchData)
    return res5.json()


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7900,debug=True)