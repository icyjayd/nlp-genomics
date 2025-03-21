import sys
import sentencepiece as spm
import pandas as pd
import nltk

if __name__ == '__main__':
    nltk.download('punkt')
    with open('NoteTextSentences.txt', 'w') as f:
        for chunk in pd.read_csv('mimic/NOTEEVENTS.csv.gz', compression='gzip', header=0, sep=',', quotechar='"',low_memory=False, encoding='utf-8', chunksize=10000):
            for doc in chunk['TEXT']:
                sentences = nltk.sent_tokenize(doc)
                for sentence in sentences:
                    if(len(sentence)>1):
                        f.write(sentence)
    f.close()
