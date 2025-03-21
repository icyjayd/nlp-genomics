import pandas as pd
import argparse
import numpy as np
from tables import *
from datetime import datetime
from sklearn.model_selection import train_test_split
import gzip
from multiprocessing import Pool
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import ShareableList
import os
from ast import literal_eval
def do_work(args):
    #k=16
    sl1, sl2, sl3, (x1, _) = args
    training_set = ShareableList(name=sl1.shm.name)
    training_set_lengths = ShareableList(name=sl2.shm.name)
    training_set_values = ShareableList(name=sl3.shm.name)

    Cx1 = len(gzip.compress(np.array(x1)))

    distance_from_x1 = []
    for x2, Cx2 in zip(training_set, training_set_lengths):
        x1x2 = x1 + literal_eval(x2)
        Cx1x2 = len(gzip.compress(np.array(x1x2)))
        ncd = (Cx1x2 - min(Cx1, Cx2)) / max(Cx1, Cx2)
        distance_from_x1.append(ncd)

    sorted_idx = np.argsort(np.array(distance_from_x1))
    top_k_class = [training_set_values[idx] for idx in sorted_idx[:k]]
    predict_class = max(set(top_k_class), key=top_k_class.count)
    return predict_class

if __name__ == "__main__":

    parser =argparse.ArgumentParser(description="Perform NCD method classification")
    parser.add_argument("sample_size",type=int)
    args = parser.parse_args()
    sample_size = args.sample_size

    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    if len(month) <2:
        month = "0" + month
    day = str(now.day)
    if len(day) <2:
        day = "0" + day
    day = "-".join([year, month, day])

    unique_species = pd.read_csv("/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/unique_species.csv")
    family_counts = unique_species['family'].value_counts()
    n=50
    family_counts_over_n= family_counts[family_counts>n]
    num_families = len(family_counts_over_n)
    print(f"number of families over {n}: {num_families}")
    # print((family_counts_over_n))
    # print(len(family_counts_over_n))
    all_families_over_n= unique_species[unique_species['family'].isin(family_counts_over_n.index)]
    np.random.seed(42)
    random_family_df = pd.DataFrame(columns=unique_species.columns)
    sample_num = sample_size #40 * 16 = 640 total genomes
    samples = []
    for family in all_families_over_n['family'].unique():
        family_df = unique_species[unique_species['family']==family]
        samples.append(family_df.sample(sample_num))
    samples = pd.concat(samples, axis=0)
    path = '/gpfs/data/johnsonslab/nlp-genomics/almeida-2020/'
    path_to_db = os.path.join(path, 'tokenizations_8192k_poc.h5')
    genomes = []
    with open_file(path_to_db, 'r') as file:
        data = file.root.data
        for idx in samples.index:
            tkns = data['Tknz%d' % idx].read()
            genomes.append(tkns)
    labels_dict= dict(zip(samples['family'].unique(), np.arange(len(samples['family'].unique()))))
    labels = [labels_dict[genome] for genome in samples['family']]
    data = []
    for i in range(len(genomes)):
        data.append((genomes[i], labels[i]))
    training_set, test_set = train_test_split(data, test_size=0.2)

    k = round(np.sqrt(len(training_set)))
    results = []
    with SharedMemoryManager() as smm, Pool() as pool:
        training_set_sl = smm.ShareableList([str(x2) for x2, _ in training_set])
        training_set_values = smm.ShareableList([int(val) for _, val in training_set])
        training_set_comp_lengths = smm.ShareableList([len(gzip.compress(np.array(x2))) for x2, _ in training_set])

        for i, result in enumerate(pool.imap(do_work, ((training_set_sl, training_set_comp_lengths, training_set_values, t) for t in test_set), chunksize=1)):
            results.append(result)
    total = len(test_set)
    hits = 0
    results_dict = {"predicted":[], 'ground truth':[]}
    for i, result in enumerate(results):
        if(int(test_set[i][1])==result):
            hits+=1
        results_dict['predicted'].append(result)
        results_dict['ground truth'].append(int(test_set[i][1]))
    print(f"{100 * hits/total}% accuracy")

    import pickle
    file_name = f'/gpfs/scratch/jic286/JohnsonLab/genomic_nlp/gzip_method_16_50-member_families_{num_families * sample_num}_samples_{day}.pkl'
    with open(file_name, 'wb') as file:
        pickle.dump(results_dict, file)
        print(f'Object successfully saved to "{file_name}"')
