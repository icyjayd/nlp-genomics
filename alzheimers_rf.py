from datetime import datetime
import youtokentome as yttm
import os
import pandas as pd
from functools import partial
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, accuracy_score
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
import numpy as np
import time
import joblib
import argparse
from tables import *
def analyze(clf):
    #Predicting
    y_pred = clf.predict(X_test)
    yt_pred = clf.predict(X_train)
    #Analyzing
    cm = confusion_matrix(y_test,y_pred)
    print(f'Confusion Matrix :\n {cm}\n')
    print(f'Test Set Accuracy Score :\n {accuracy_score(y_test,y_pred)}\n')
    print(f'Train Set Accuracy Score :\n {accuracy_score(y_train,yt_pred)}\n')
    print(f'Classification Report :\n {classification_report(y_test,y_pred)}')

def retrieve_genomes(path, gzipped=False):
    if(gzipped):
        with gzip.open(path, 'r') as f:
            file_content = f.readlines()
            file_content = [content.strip() for content in file_content]

    else:
        with open(path, 'r') as f:
            file_content = f.readlines()
            file_content = [content.strip() for content in file_content]
    if isinstance(file_content[0], bytes):
        file_content = [line.decode('utf') for line in file_content]
    genomes = {}
    bases = ""
    header = file_content[0]

    for i in range(1, len(file_content)):
        if(">") in file_content[i]:
            genomes[header] = bases
            header = file_content[i]
            bases=""
        else:
            bases+= file_content[i]
            if(i==len(file_content)-1):
                genomes[header] = bases
                header = file_content[i]
                bases=""
    return genomes

def tokenize(sample_title, folder, path='/gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023'):
#     print("tokenizing", sample_title)
    # file = os.path.join(path, str(sample_title), folder, 'final.contigs.fa')
    tokens = data['Tknz%d' %sample_title].read()
    # genomes = retrieve_genomes(file).values()
    # tokens = []
    # for genome in genomes:
    #     tokens += bpe.encode(genome, output_type =yttm.OutputType.SUBWORD)
    return tokens
if __name__=="__main__":
    parser =argparse.ArgumentParser(description="Perform SVD random forest on TF-IDF metagenomes")
    parser.add_argument("svd_components",type=int)
    parser.add_argument("--contigs", choices = ['raw', 'kneaded'], default='kneaded')
    parser.add_argument("--bpe_model", default="/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_8192k.model")
    parser.add_argument("--save_path", default = "/gpfs/scratch/jic286/JohnsonLab/alzheimers_rf_model_data")
    args = parser.parse_args()
    svd_components = args.svd_components
    contigs = args.contigs
    print("svd components:", svd_components, "contigs:", contigs)
    model_path = args.bpe_model
    data_path = args.save_path

    path = '/gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023'
    h5file = open_file(os.path.join(path, contigs + "_tokenizations_8192k.h5"), 'r')
    data = h5file.root.data

    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    if len(month) <2:
        month = "0" + month
    day = str(now.day)
    if len(day) <2:
        day = "0" + day
    day = "-".join([year, month, day])
    print(day, flush=True)
    bpe = yttm.BPE(model=model_path)

    path = '/gpfs/data/johnsonslab/nlp-genomics/alzheimers/ferreiro-2023'
    key_df = pd.read_csv(os.path.join(path, 'key_df.csv'))
    if contigs == "raw":
        ##need to remove the last entry due to the operation taking a long time
        key_df = key_df.iloc[:-1]
        #need to remove missing index too
        idx = key_df[key_df['sample_title']==61707].index[0]
        key_df = pd.concat([key_df.iloc[:idx], key_df.iloc[idx + 1:]])
    elif contigs == "kneaded":
        idx = key_df[key_df['sample_title']==25632].index[0]
        key_df = pd.concat([key_df.iloc[:idx], key_df.iloc[idx + 1:]])
    tokenize_raw = partial(tokenize, folder='megahit_raw_out')
    tokenize_kneaded = partial(tokenize, folder='megahit_kneaded_out')
    key_df
    if contigs == "raw":
        tokenize_contigs = tokenize_raw
    elif contigs == "kneaded":
        tokenize_contigs = tokenize_kneaded

    np.random.seed(42)

    X_train, X_test, y_train, y_test = train_test_split(key_df['sample_title'], key_df['disease_state'])
    tf_idf_vectorizer = TfidfVectorizer(tokenizer=tokenize_contigs, lowercase=False)
    classifier_rf = Pipeline([('tfidf',tf_idf_vectorizer),
    ('svd', TruncatedSVD(n_components=svd_components, n_iter=7, random_state=42)),
    ('clf',RandomForestClassifier(bootstrap= False, criterion= 'entropy', n_estimators= 150, ))])
    start = time.time()
    classifier_rf.fit(X_train, y_train)
    print(time.time()-start, "seconds to fit")
    analyze(classifier_rf)
    print(time.time()-start, "seconds to fit and analyze")

    joblib.dump(classifier_rf, os.path.join(data_path, "rf_model_svd_{}_{}_{}.pkl".format(contigs,svd_components,day)))
    joblib.dump(X_train, os.path.join(data_path, "X_train_svd_{}_{}_{}.pkl".format(contigs, svd_components, day)))
    joblib.dump(X_test, os.path.join(data_path, "X_test_svd_{}_{}_{}.pkl".format(contigs, svd_components, day)))
    joblib.dump(y_train, os.path.join(data_path, "y_train_svd_{}_{}_{}.pkl".format(contigs, svd_components, day)))
    joblib.dump(y_test, os.path.join(data_path, "y_test_{}_{}_{}.pkl".format(contigs, svd_components, day)))
