import pandas as pd
import sys
import MeCab
from gensim.corpora.dictionary import Dictionary

# https://analytics-note.xyz/machine-learning/gensim-lda/

df = pd.read_csv('dataset/text/livedoor.tsv', delimiter='\t')
texts = df['article'].values.tolist()
sentences = []

for text in texts:
    m = MeCab.Tagger("-Ochasen")
    sentences.append(m.parse(text))
    print(m.parse(text))
    exit()

# 単語と単語IDを対応させる辞書の作成
dictionary = Dictionary(sentences)
# LdaModelが読み込めるBoW形式に変換
corpus = [dictionary.doc2bow(text) for text in sentences]

# 5000番目のテキストを変換した結果。(長いので10単語で打ち切って表示)
print(corpus[5000][:10])

# idから単語を取得
print(dictionary[119])
# print(dictionary.id2token[119]) # これも同じ結果
# 復帰

# 単語からidを取得
print(dictionary.token2id["復帰"])
# 119

from gensim.models import LdaModel
# トピック数を指定してモデルを学習
lda = LdaModel(corpus, num_topics=9)