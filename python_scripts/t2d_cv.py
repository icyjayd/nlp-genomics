from datetime import datetime
import youtokentome as yttm
import os
import pandas as pd
from functools import partial
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, accuracy_score
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


import numpy as np
import time
import joblib
import argparse
from tables import *
import xgboost as xgb
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

def tokenize(sample_title):
#     print("tokenizing", sample_title)
    # file = os.path.join(path, str(sample_title), folder, 'final.contigs.fa')
    tokens = data[f'Tknz{sample_title}'].read()
    # genomes = retrieve_genomes(file).values()
    # tokens = []
    # for genome in genomes:
    #     tokens += bpe.encode(genome, output_type =yttm.OutputType.SUBWORD)
    return tokens
if __name__=="__main__":
    parser =argparse.ArgumentParser(description="Perform SVD random forest on TF-IDF metagenomes")
    parser.add_argument("svd_components",type=int)
    parser.add_argument("model", choices=['rf', 'svm', 'lr', 'knn', 'xgboost'])
    parser.add_argument("--contigs", choices = ['raw', 'kneaded'], default='raw')
    parser.add_argument("--bpe_model", default="/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/metagenomes_8192k.model")
    parser.add_argument("--save_path", default = "/gpfs/scratch/jic286/JohnsonLab/t2d_model_data")
    parser.add_argument("--lr_penalty", choices=['l1', 'l2', 'elasticnet'])
    parser.add_argument("--lr_max_iters", type=int, default = 100)
    parser.add_argument('--thresholded', dest='thresholded', default=False, action='store_true')
    parser.add_argument("--n_estimators", default=100)
    parser.add_argument("--cv", type=int, default=5)
    parser.add_argument("--random_state", default=42)
    args = parser.parse_args()
    svd_components = args.svd_components
    print("svd components:", svd_components)
    model = args.model
    print("model used:", model)
    lr_penalty = args.lr_penalty
    lr_max_iters = args.lr_max_iters
    random_state = args.random_state
    n_estimators = args.n_estimators
    cv = args.cv
    if model !='lr':
        print("Warning: lr not selected as model. lr penalty and lr max iters will not be used")
    else:
        print("lr penalty:", lr_penalty, "| lr max iters:", lr_max_iters)
    if model != 'rf' and model != 'xgboost':
        print("Warning: rf and xgboost not selected as model. n_estimators will not be used")
    else:
        print("n_estimators:", n_estimators)
    contigs = args.contigs
    model_path = args.bpe_model
    bpe_vocab = model_path[model_path.rfind("_")+1:model_path.rfind(".")]

    data_path = args.save_path
    thresholded = args.thresholded
    threshold = ""
    if thresholded:
        threshold ='threshold_10_'
    print(thresholded)
    path = '/gpfs/data/johnsonslab/nlp-genomics/t2d'
    h5file = open_file(os.path.join(path, contigs + "_tokenizations_" + threshold + bpe_vocab + "_new.h5"), 'r')
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
    #bpe = yttm.BPE(model=model_path)

    # path = '/gpfs/data/johnsonslab/nlp-genomics/t2d'
    key_df = pd.read_csv(os.path.join(path,'metadata', 't2d1+2+3meta.csv'))
#     if contigs == "raw":
#         ##need to remove the last entry due to the operation taking a long time
# #        key_df = key_df.iloc[:-1]
#         #need to remove missing index too
#         idx = key_df[key_df['sample_title']==61707].index[0]
#         key_df = pd.concat([key_df.iloc[:idx], key_df.iloc[idx + 1:]])
#     elif contigs == "kneaded":
#         idx = key_df[key_df['sample_title']==25632].index[0]
#         key_df = pd.concat([key_df.iloc[:idx], key_df.iloc[idx + 1:]])
    tokenize_raw = (tokenize)
    tokenize_kneaded = (tokenize)
    # key_df
    if contigs == "raw":
        tokenize_contigs = tokenize_raw
    elif contigs == "kneaded":
        tokenize_contigs = tokenize_kneaded

    X_train, X_test, y_train, y_test = train_test_split(key_df['Sample Id'], key_df['Label'])

    np.random.seed(42)
    tf_idf_vectorizer = TfidfVectorizer(tokenizer=tokenize_contigs, lowercase=False)
    if model == "rf":
        clf = RandomForestClassifier(bootstrap=False, criterion='entropy', n_estimators= n_estimators,random_state=random_state)
    elif model == "svm":
        clf = SVC()
    elif model == "lr":
        clf = LogisticRegression(penalty=lr_penalty, max_iter = lr_max_iters, random_state=random_state)
    elif model == "knn":
        clf = KNeighborsClassifier(n_neighbors = round(np.sqrt(len(X_train))))
    elif model == "xgboost":
        clf = xgb.XGBClassifier(n_estimators =n_estimators, eta=0.01, random_state=random_state)


    if svd_components >0:
        classifier = Pipeline([('tfidf',tf_idf_vectorizer),
        ('svd', TruncatedSVD(n_components=svd_components, n_iter=7, random_state=random_state)),
        ('clf',clf)])
    else:
        classifier = Pipeline([('tfidf',tf_idf_vectorizer),
        ('clf',clf)])

    start = time.time()
    scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted', 'roc_auc']
    scores = cross_validate(classifier, key_df['Sample Id'], key_df['Label'], scoring=scoring, cv=cv,
    return_estimator=True, return_indices = True)
    print(time.time()-start, "seconds to fit")
    model_type = model + "_model"
    if model=="rf" or model == "xgboost":
        model_type += f"_{n_estimators}_estimators"
    elif model == "lr":
        model_type+= f"_{lr_max_iters}_max_iters"

    for score in scoring:
        print("Mean", score + ":", scores["test_" + score].mean(), "|",
        score, "STD:", scores["test_" + score].std(), )
    joblib.dump(scores, os.path.join(data_path, f"{model_type}_svd_{svd_components}_scoring_{contigs}_bpe_new_{bpe_vocab}_{day}.pkl"))
    h5file.close()
