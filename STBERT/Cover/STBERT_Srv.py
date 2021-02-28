import socket
import numpy as np
import pandas as pd
import jieba.posseg as pseg
from sentence_transformers import SentenceTransformer
from program.albert.LSCBS.STBERT.Cover import util
import time
import json


class Data(object):
    def __init__(self):
        self.id = id
        self.no = "0"
        self.reason = ""
        self.Situation = ""

    def __jsonencode__(self):
        return {'id': self.id, 'no': self.no, 'reason': self.reason, 'Situation':self.Situation}

class Data2(object):
    def __init__(self):
        self.id = id
        self.court = ""
        self.date = ""
        self.no = "0"
        self.reason = ""
        self.mainText = ""
        self.judgement = ""

    def __jsonencode__(self):
        return {'id': self.id, 'court': self.court, 'date': self.date, 'no': self.no, 'reason': self.reason, 'mainText': self.mainText, 'judgement': self.judgement}

class AdvancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__jsonencode__'):
            return obj.__jsonencode__()

        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class model(object):
    def __init__(self):
        self.debug = 'debug'
        self.corpus = []
        self.corpusList = []

        my_regex = r"○"
        p_upper = 4.0
        p_upperT = "40"
        filedir = 'data_tfidf2'
        filenum = '100000X'
        filename = 'Result_' + filenum
        print(filenum , '-', p_upper)

        berttype = 'bert-base-chinese'
        testtype = 0
        tmpSpecial = ''
        max = 20
        self.top_k = 5
        self.dt_idf = pd.read_csv("..//TFIDF//" + filedir +"//Result_TFIDF_" + filenum +".csv", encoding='utf8')
        self.dt_idf = self.dt_idf[self.dt_idf["P"] > p_upper].drop(columns=['詞性']).set_index('詞').T.to_dict('list')

        #df1=pd.read_csv("..//TFIDF//" + filedir +"/result_Sbert_" + filenum +"_TFIDF_" + p_upperT +"X.csv")
        df1=pd.read_csv("..//TFIDF//" + filedir +"/result_100000_4XF.csv")
        df1 = df1.dropna()
        df1['reason'] = df1['reason'].str.replace('等','')
        df1['reason'] = df1['reason'].str.replace('罪','')
        df1['reason'] = df1['reason'].str.replace("條例","")
        df1['reason'] = df1['reason'].str.replace("防制","")
        df1['reason'] = df1['reason'].str.replace("管制","")
        df1['reason'] = df1['reason'].str.replace("違反","")
        df1['Situation'] = df1['Situation'].str.replace(my_regex, "")
        self.dtmain = df1
        tStart = time.time()



        #embedder  SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

        # Corpus with example sentences
        #corpus  ['A man is eating food.',
        #          'A man is eating a piece of bread.',
        #          'The girl is carrying a baby.',
        #          'A man is riding a horse.',
        #          'A woman is playing violin.',
        #          'Two men pushed carts through the woods.',
        #          'A man is riding a white horse on an enclosed ground.',
        #          'A monkey is playing drums.',
        #          'A cheetah is running behind its prey.'
        #          ]

        for index, row in df1.iterrows():
            if (row.Situation == None):
                continue
            if (isinstance(row.Situation, float)):
                continue
            if (len(row.Situation) == 0):
                continue
            if (index == 5):
                print()
            d = Data()
            d.id = index
            d.no = row.no
            d.reason = row.reason
            d.Situation = row.Situation
            self.corpusList.append(d)
            self.corpus.append(row.Situation)


        print(len(self.corpus))

        #列印結果

        self.embedder = SentenceTransformer(berttype)
        # embedder=SentenceTransformer('model_bert_4000X')

        self.corpus_embeddings = self.embedder.encode(self.corpus, convert_to_tensor=True)

        tEnd = time.time()#計時結束
        print("轉向量時間", "%f sec" % (tEnd - tStart))

    def GetSimilar(self, ljtext = '', simtype = 'COS'):
        def doRule(Situation):
            my_regex = r"[\(\（]([^一二三四五六七八九零十1234567890]{1}[^\)\）]+|[一二三四五六七八九零十1234567890]{1}[^\)\）]{1,})[\)\）]"
            Situation = Situation.replace(my_regex, "")
            # /○{2,}/
            regex1 = r"○"
            Situation = Situation.replace(regex1, "")

            # /\d{10}/
            regex2 = r"\d{10}"
            Situation = Situation.replace(regex2, "")

            # /[A-Z0-9]{2,3}\-[A-Z0-9]{3,4}/ 車牌
            regex3 = r"[A-Z0-9]{2,3}\-[A-Z0-9]{3,4}"
            Situation = Situation.replace(regex3, "")
            Source = Situation
            try:
                words = pseg.cut(Situation)
                seq = ''
                for w, l in words:
                    if (w in self.dt_idf):
                        continue
                    elif (l in ('m', 't', 'c')):
                        continue
                    else:
                        seq += w
                Situation = seq
            except:
                Situation = Source
            return Situation

        # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
        i = -1
        tmpSpecial = ''
        show = 0
        queries_ori = ljtext
        query = doRule(ljtext)
        top_k = self.top_k

        tStart2 = time.time()
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        if (simtype == 'COS'):
            cos_scores = util.pytorch_cos_sim(query_embedding, self.corpus_embeddings)[0]
            cos_scores = cos_scores.cpu()
            # We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
        elif (simtype == 'DIS'):
            cos_scores = util.pytorch_Dis(query_embedding, self.corpus_embeddings)
            cos_scores = cos_scores.cpu()
            # We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(cos_scores, range(top_k))[0:top_k]
        elif (simtype == 'DPS'):
            cos_scores = util.pytorch_DPS(query_embedding, self.corpus_embeddings)
            cos_scores = cos_scores.cpu()
            # We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
        elif (simtype == 'BS'):
            cos_scores = util.pytorch_BS(query_embedding, self.corpus_embeddings)
            cos_scores = cos_scores.cpu()
            # We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
        elif (simtype == 'MD'):
            cos_scores = util.pytorch_Manhattan_Dis(query_embedding, self.corpus_embeddings)
            cos_scores = cos_scores.cpu()
            # We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
        elif (simtype == 'JS'):
            cos_scores = util.pytorch_Jaccard_Sim(query_embedding, self.corpus_embeddings)
            cos_scores = cos_scores.cpu()
            # We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
        else:
            return ljtext

        print("\n\n\n\n")
        for qlen in range(0, len(queries_ori), 50):
            print(show + 1 if qlen == 0 else '', "Query:" if qlen == 0 else '\t', queries_ori[qlen: qlen + 50])
        # print("\nTop 5 most similar sentences in corpus:")
        print('')
        no = 1

        SimilarList = []
        for idx in top_results[0:top_k]:
            SimilarList.append(self.corpusList[idx])
            print(no, "  "
                  , self.corpusList[idx].id
                  , self.corpusList[idx].no, "\t"
                  , self.corpusList[idx].reason
                  , "\t(Score: %.4f)" % (cos_scores[idx]))
            for qlen in range(0, len(self.corpusList[idx].Situation.strip()), 50):
                print(self.corpusList[idx].Situation.strip()[qlen: qlen + 50])

            print('\n')
            no = no + 1
            if (no > 5):
                break

        show += 1
        tEnd2 = time.time()  # 計時結束
        print("COS相似計算時間", "%f sec" % (tEnd2 - tStart2))

        return SimilarList

bind_ip = "127.0.0.1"
bind_port = 1025

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))
print('Start model')
m = model()
print('Build model complete')
server.listen(5)

print("[*] Listening on %s:%d " % (bind_ip,bind_port))

while True:
    client,addr = server.accept()
    print('Connected by ', addr)

    try:
        data = client.recv(32768)
        query = data.decode()
        print("Client recv data : %s " % (query))
        TranData = json.loads(query)

        if (TranData['type'] == 0):
            s =m.GetSimilar(TranData['msg'], 'COS')
            print('Similar Done')
            request = json.dumps(s, cls=AdvancedJSONEncoder)
            print('GetSimilar ', request)
            client.send(request.encode())
        elif (TranData['type'] == 1):
            s = m.dtmain.loc[TranData['id']]
            d = Data2()
            d.id = TranData['id']
            d.court = s.court
            d.date = s.date
            d.no = s.no
            d.reason = s.reason
            d.mainText = s.mainText
            d.judgement = s.judgement


            print('Get judgement Done')
            request = json.dumps(d, cls=AdvancedJSONEncoder)
            #request = json.dumps(s, cls=AdvancedJSONEncoder)
            print('judgement ', request)
            client.send(request.encode())

    except Exception as e:
        print(e)
        s = 'Fail'
        client.send(s)



