import json
import pandas as pd
import re
from transformers import pipeline

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)

df = pd.read_json('/home/yassine/python_works/banque_info.json')
df['nom'] = df['nom'].str.lower()

agences = ['barid','populaire','cih','africa','assafa','omnia','agricole','bmce','générale']  
pattern = '('+'|'.join(agences)+')'
df['nom_banque'] = df['nom'].apply(lambda x: re.findall(pattern,x)[0] if re.findall(pattern,x) else 'unknown')

def calcul_score(list_avis):
    weight = 0
    feedback = []
    for avis in list_avis:
        result = sentiment_task(avis)[0]
        if result['label'] == 'negative':
            weight -= result['score']
        else:
            weight += result['score']
    return 0 if len(list_avis) == 0 else weight/len(list_avis)

df['score'] = df['avis'].apply(calcul_score)

df.to_json('/home/yassine/python_works/processData.json', orient = 'split', compression = 'infer', index = 'true')
