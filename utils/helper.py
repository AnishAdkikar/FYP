from config import API_TOKEN
import requests

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
        if vectors.get(i,False):
            continue  
        vectors[i]=vector