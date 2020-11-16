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
## Livedoorのデータを整形
日本語文書分類タスクのための代表的なコーパスの1つ、Livedoorニュースコーパス。
Livedoorニュースのニュース記事を収集して生成されており、9種類のニュース記事が計7367本収載されています。

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

1.本文を分かち書きに変換します。

2.``` gensim``` を用いてトピック分析します。
以下のコマンドでパッケージをインストールしてください。

``` 
pip install pandas
pip install gensim
``` 