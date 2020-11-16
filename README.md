# livedoor-topic

## はじめに
- 環境構築をしていきましょう。

### MeCabとは

日本生まれの形態素解析エンジンです。

http://taku910.github.io/mecab/

### 形態素解析とは

形態素解析とは、言語学においてある言葉が変化・活用しない部分を最小単位の「素」と捉え、その素ごとに言葉を分解してゆく手法のことである。

``` 
例：私は長田研究室の領域生です
→　私　は　長田　研究　室　の　領域　生　です
``` 
### インストールの前提

- OS: Windows10 Home 64bit
- Python: Python 3.6.5 (Anacondaによるインストール）

### MeCabをインストールする

64bit向けのインストーラーを作成した方がいるようなのでありがたく使用させてもらいます。
ダウンロード完了後、インストールを実行します。
https://github.com/ikegami-yukino/mecab/releases/tag/v0.996

＞mecab-0.996-64.exe

### PythonにMeCabを取り込む
``` 
pip install mecab-python-windows
```

続いて、MeCabのインストール先/binにある「libmecab.dll」をコピー＆ペーストします。
コピー元例：C:\Program Files\MeCab\bin
コピー先例：C:\ProgramData\Anaconda3\Lib\site-packages

## Livedoorのデータを整形
日本語文書分類タスクのための代表的なコーパスの1つ、Livedoorニュースコーパス。
Livedoorニュースのニュース記事を収集して生成されており、9種類のニュース記事が計7367本収載されています。

### livedoorニュースコーパス

NHN Japan株式会社が運営する「livedoor ニュース」のうち、下記のクリエイティブ・コモンズライセンスが適用されるニュース記事を収集し、可能な限りHTMLタグを取り除いて作成したものです。
- トピックニュース http://news.livedoor.com/category/vender/news/
- Sports Watch http://news.livedoor.com/category/vender/208/
- ITライフハック http://news.livedoor.com/category/vender/223/
- 家電チャンネル http://news.livedoor.com/category/vender/kadench/
- MOVIE ENTER http://news.livedoor.com/category/vender/movie_enter/
- 独女通信 http://news.livedoor.com/category/vender/90/
- エスマックス http://news.livedoor.com/category/vender/smax/
- livedoor HOMME http://news.livedoor.com/category/vender/homme/
- Peachy http://news.livedoor.com/category/vender/ldgirls/

収集時期：2012年9月上旬 ダウンロード（通常テキスト）：ldcc-20140209.tar.gz ダウンロード（Apache Solr向き）
コーパスは事前に入手しています。(``` dataset``` の中にありますが、一応入手方法は以下のような感じ。)

``` 
mkdir dataset
cd dataset
wget https://www.rondhuit.com/download/ldcc-20140209.tar.gz
tar zxvf ldcc-20140209.tar.gz
``` 

各カテゴリのニュース記事は``` dataset/text```内の```dokujo-tsushin```から```topic-news```までの該当するディレクトリに格納されています。
ファイル名はいずれも ``` <ディレクトリ名>-xxxxxxx.txt```  という形式です。

### tsvファイルの作成
ここから、各ニュース記事の ①ファイル名，②本文，③カテゴリのone-hot encoding を格納したtsvファイルを作っていきましょう。
``` 
for filename in `basename -a ./text/dokujo-tsushin/dokujo-tsushin-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/dokujo-tsushin/$filename`; echo -e "\t1\t0\t0\t0\t0\t0\t0\t0\t0"; done >> ./text/livedoor.tsv
for filename in `basename -a ./text/it-life-hack/it-life-hack-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/it-life-hack/$filename`; echo -e "\t0\t1\t0\t0\t0\t0\t0\t0\t0"; done >> ./text/livedoor.tsv
for filename in `basename -a ./text/kaden-channel/kaden-channel-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/kaden-channel/$filename`; echo -e "\t0\t0\t1\t0\t0\t0\t0\t0\t0"; done >> ./text/livedoor.tsv
for filename in `basename -a ./text/livedoor-homme/livedoor-homme-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/livedoor-homme/$filename`; echo -e "\t0\t0\t0\t1\t0\t0\t0\t0\t0"; done >> ./text/livedoor.tsv
for filename in `basename -a ./text/movie-enter/movie-enter-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/movie-enter/$filename`; echo -e "\t0\t0\t0\t0\t1\t0\t0\t0\t0"; done >> ./text/livedoor.tsv
for filename in `basename -a ./text/peachy/peachy-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/peachy/$filename`; echo -e "\t0\t0\t0\t0\t0\t1\t0\t0\t0"; done >> ./text/livedoor.tsv
for filename in `basename -a ./text/smax/smax-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/smax/$filename`; echo -e "\t0\t0\t0\t0\t0\t0\t1\t0\t0"; done >> ./text/livedoor.tsv
for filename in `basename -a ./text/sports-watch/sports-watch-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/sports-watch/$filename`; echo -e "\t0\t0\t0\t0\t0\t0\t0\t1\t0"; done >> ./text/livedoor.tsv
for filename in `basename -a ./text/topic-news/topic-news-*`; do echo -n "$filename"; echo -ne "\t"; echo -n `sed -e '1,3d' ./text/topic-news/$filename`; echo -e "\t0\t0\t0\t0\t0\t0\t0\t0\t1"; done >> ./text/livedoor.tsv
``` 

## トピック分析

②本文　を使ってトピック分析をしてみよう！

1.本文を分かち書きに変換します。(今回は名詞一般のみを使います。)

2.``` gensim``` を用いてトピック分析します。
以下のコマンドでパッケージをインストールしてください。

```
pip install gensim
(なければ以下もインストール)
pip install pandas
pip install re
pip install tqdm
```

トピック数は，Livedoorのカテゴリ数と同じ9個に設定してみよう！


```
python main.py
```

各トピックの出力結果はこんな感じ。カテゴリと対応できてるか確認してみよう！
```
topic0
人,0.022903683
自分,0.016474457
会社,0.014194324
情報,0.012465477
年収,0.00995398
企業,0.008524116
...
```