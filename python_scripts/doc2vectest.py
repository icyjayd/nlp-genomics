import smart_open
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim
from gensim.test.utils import get_tmpfile
import pandas as pd
import os

def read_corpus(strings, tokens_only=False):
    for i, line in enumerate(strings):
        tokens = gensim.utils.simple_preprocess(line)
        if tokens_only:
            yield tokens
        else:
            # For training data, add tags
            yield gensim.models.doc2vec.TaggedDocument(tokens, [i])
if __name__ == "__main__":
    print(os.getcwd())
    notes = pd.read_csv('mimic/NOTEEVENTS.csv.gz', compression='gzip', header=0, sep=',', quotechar='"',low_memory=False, encoding='utf-8')

    train_corpus = list(read_corpus(notes['TEXT'].values))
    #test_corpus = list(read_corpus(notes['TEXT'][:100].values, tokens_only=True))
    model = Doc2Vec(vector_size=100, min_count=2, epochs=40)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    fname = "doc2vec-MIMIC-notes-100"
    model.save(os.path.join(os.getcwd(), fname))
#gensim.utils.simple_preprocess("testing one two")
