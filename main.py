import MeCab
import re
import csv
import os
import pandas as pd

from gensim.models import LdaModel
from gensim.corpora.dictionary import Dictionary

from tqdm import tqdm

"""
Livedoorコーパスのトピック分析を行う
"""

if __name__ == '__main__':

    df = pd.read_csv('livedoor.tsv', delimiter='\t')
    texts = df['article'].values.tolist()
    new_sentences = []

    if os.path.isfile('output_sentences.csv'):
        with open('output_sentences.csv','r',encoding='utf-8') as f:
            line = f.readlines()
            for l in line:
                if l != '\n':
                    new_sentences.append(l.split(','))

    else:
        with open('output_sentences.csv', 'w',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for text in tqdm(texts,desc='形態素解析中'):
                new_sentence = []
                sentences = re.split('。|\.|．|\!|\?|！|？|\(|\)|（|）|【|】|☆|…|♪|&|#|;|:|◎|※', text)  # 文ごとにレビューをカット
                for sentence in sentences:
                    wakati = MeCab.Tagger("-Ochasen")
                    line_info = re.split('[,\n]', wakati.parse(sentence))
                    for line in line_info:
                        try:
                            info = re.split('[,\t]', line)
                            hinshi = info[3]
                            represent_word = info[2]
                            if hinshi == '名詞-一般':
                                new_sentence.append(represent_word)
                        except:
                            continue
                writer.writerow(new_sentence)
                new_sentences.append(new_sentence)


    # 単語と単語IDを対応させる辞書の作成
    dictionary = Dictionary(new_sentences)
    # LdaModelが読み込めるBoW形式に変換
    corpus = [dictionary.doc2bow(text) for text in new_sentences]

    # トピック数を指定してモデルを学習
    lda = LdaModel(corpus=corpus,
                   id2word=dictionary,
                   num_topics=9,
                   minimum_probability=0.001,
                   passes=20,
                   update_every=0,
                   chunksize=10000)

    with open('output_topics.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(9):
            writer.writerow([f'topic{i}'])
            print("\n")
            print("=" * 80)
            print("TOPIC {0}\n".format(i))
            topic = lda.show_topic(i, topn=20)
            for t in topic:
                print("{0:20s}{1}".format(t[0], t[1]))
                writer.writerow([t[0], t[1]])
