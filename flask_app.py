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
        efsearch = M
    else:
        M = random.randint(50, 100)
        efsearch = M
    header={'Content-Type': 'application/json','Authorization': API_TOKEN}
    query = '''A useful technique for measurement of back strength in osteoporotic and elderly patients. Improvement of back extensor strength (BES) can be used as a therapeutic method for patients with chronic back pain and osteoporosis. The method of evaluation must be reliable and accurate without compromising the condition of the patient. We report the development of a back isometric dynamometer (BID-2000) designed specifically by two of us to address these concerns in elderly patients with osteopenia or osteoporosis. As the demographics of the general population change, increasing numbers of patients will need the type of monitoring that the BID-2000 provides. Aging has been shown to cause a reduction in the number of functional muscle motor units. To examine this effect on BES, we tested 50 normal, healthy women who were 30 to 79 years old. Proper testing of BES in patients with fragile vertebrae should include isometric measurement in the prone position, maneuverability of the device to allow comfortable positioning of the patient, and simplicity of technique to minimize repetitious performance of maximal contraction. The BID-2000 incorporates each of these features and also provides meaningful results inexpensively. The device offers a safe, reliable (coefficient of variation = 2.33%), and valid (P = 0.001) method of evaluation. The results of our study demonstrated moderate, steady reduction of BES with increasing age and with each successive decade. '''
    payload1 = {   
        "model":"text-embedding-3-large",
        "input":query
    }
    res4 = requests.post(url='https://api.openai.com/v1/embeddings', json=payload1,headers=header)
    searchData = {
        'userID':'w',
        'K':3,
        'ef': efsearch,
        'data':res4.json()["data"][0]["embedding"] 
    }
    res5 = requests.post(url='http://127.0.0.1:8080/search', json=searchData)
    ans = []
    for i in res5.json():
        ans.append(i.split()[0])
    return ans


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7900,debug=True)