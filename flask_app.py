from flask import Flask, jsonify
import requests
import threading
# from flask_mysqldb import MySQL
import utils.preprocessing as preprocessing
from config import API_TOKEN
app = Flask(__name__)


def send_req(url,json_data,result):
    res = requests.post(url=url, json=json_data)
    # print(res.json())
    result.update(res.json())
    # return res

def threading_batch(data,url,results):
    threads = []
    batch_size = len(data)//5
    batches = [data[i:i+batch_size] for i in range(0,len(data),batch_size)]
    print(batches)
    t1 = threading.Thread(target=send_req,args=(url,{"data":batches[0]},results))
    t2 = threading.Thread(target=send_req,args=(url,{"data":batches[1]},results))
    t3 = threading.Thread(target=send_req,args=(url,{"data":batches[2]},results))
    t4 = threading.Thread(target=send_req,args=(url,{"data":batches[3]},results))
    t5 = threading.Thread(target=send_req,args=(url,{"data":batches[4]},results))
    print("threading started")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    return results
@app.route('/pdf')
def pdf():
    userData = {
        'userID':'lkj',
        'M':'16',
        'efConstruction':'7'
    }
    res2 = requests.post(url='http://127.0.0.1:8080/connection', json=userData)
    if res2.status_code != 200:
        return "Connection Error"

    df = preprocessing.load_dataset()
    texts = preprocessing.rows_to_text(df)
    results = {}
    vectors = threading_batch(texts,'http://127.0.0.1:5000',results)
    print(results) 
    addData = {
        'userID':'lkj',
        'data':results
    }
    res3 = requests.post(url='http://127.0.0.1:8080/add-data', json=addData)
    if res3.status_code != 200:
        return "Error while adding"
    query = "educational info"
    payload2 = {
        "data":[query]
    }
    res4 = requests.post(url='http://127.0.0.1:5000', json=payload2)
    vector = res4.json()
    searchData = {
        'userID':'lkj',
        'K':5,
        'ef':7,
        'data':res4.json()[query]
    }
    res5 = requests.post(url='http://127.0.0.1:8080/search', json=searchData)
    return res5.json()

@app.route('/pdfsearch')
def pdfsearch():
    userData = {
        'userID':'lkj',
        'M':'16',
        'efConstruction':'7'
    }
    res2 = requests.post(url='http://127.0.0.1:8080/connection', json=userData)
    if res2.status_code != 200:
        return "Connection Error"
    query = "Cipher"
    payload2 = {
        "data":[query]
    }
    res4 = requests.post(url='http://127.0.0.1:5000', json=payload2)
    vector = res4.json()
    # print(vector[query])
    searchData = {
        'userID':'lkj',
        'K':2,
        'ef':7,
        'data':res4.json()[query]
    }
    res5 = requests.post(url='http://127.0.0.1:8080/search', json=searchData)
    # print(res5.json())
    return res5.json()

@app.route('/csv1')
def csv1():
    # length = preprocessing.len_of_df()
    length = 36
    if length<10000:
        M = 10
        efconstruction = 2*M
        efsearch = M
    else:
        M = random.randint(50, 100)
        efconstruction = 2*M
        efsearch = M
    userData = {
        'userID':'pdf1',
        'M': str(M),
        'efConstruction': str(efconstruction)
    }
    print(M)
    print(efconstruction)
    res2 = requests.post(url='http://127.0.0.1:8080/connection', json=userData)
    if res2.status_code != 200:
        return "Connection Error"
    # df = preprocessing.load_dataset()
    # texts = preprocessing.rows_to_text(df)
    texts = preprocessing.extract_text_from_pdf()
    results = {}
    vectors = threading_batch(texts,'http://127.0.0.1:5000',results)
    # print(results) 
    addData = {
        'userID':'pdf1',
        'data':results
    }
    res3 = requests.post(url='http://127.0.0.1:8080/add-data', json=addData)
    if res3.status_code != 200:
        return "Error while adding"
    return "Addition Complte"


def multi_thread(texts,vectors):
    header={'Content-Type': 'application/json','Authorization': API_TOKEN}
    # vectors={}
    for i in texts:
        payload1 = {   # takes more time here
            "model":"text-embedding-3-large",
            "input":i
        }
        res1 = requests.post(url='https://api.openai.com/v1/embeddings', json=payload1,headers=header)
        # print(res1.json())
        if res1.status_code != 200:
            continue
        vector= res1.json()["data"][0]["embedding"]  
        vectors[i]=vector



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
        'userID':'r',
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
        'userID':'r',
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
        'userID':'r',
        'K':10,
        'ef': efsearch,
        'data':res4.json()["data"][0]["embedding"] 
    }
    res5 = requests.post(url='http://127.0.0.1:8080/search', json=searchData)
    return res5.json()


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7900,debug=True)