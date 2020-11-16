import MeCab

sentence = '私は長田研究室の領域生です．'
wakati = MeCab.Tagger("-Ochasen")
print(wakati.parse(sentence))