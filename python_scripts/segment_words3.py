# import sentencepiece as spm

# spm.SentencePieceTrainer.Train('--input=E:/Documents/JohnsonLab/RawNoteText.txt --model_prefix=SentencePiece32k --vocab_size=32000 --character_coverage=1.0 --model_type=unigram')

import sys
import sentencepiece as spm
import pandas as pd
import argparse
import os
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str)
    parser.add_argument("-root", type=str, default="/gpfs/scratch/jic286/JohnsonLab/")
    parser.add_argument("-size", type=int, default=32000)
    parser.add_argument("-output_dir", type=str, default="/gpfs/scratch/jic286/JohnsonLab/")
    # parser.add_argument("-out", type="str", default="ou")
    args = parser.parse_args()


    name=args.infile[:args.infile.rfind(".")]
    print(name)
    infile = os.path.join(args.root, args.infile)

    spm.SentencePieceTrainer.Train('--input='+infile + ' --model_prefix='+name+'_'+str(args.size)+' --vocab_size='+str(args.size)+' --model_type=unigram --shuffle_input_sentence=true --max_sentence_length=25000 --max_sentencepiece_length=500 --num_sub_iterations=10')
    sp=spm.SentencePieceProcessor()
    sp.Load(name+'_'+str(args.size)+".model")

    vocabs = [sp.id_to_piece(id) for id in range(sp.get_piece_size())]
    frequency={}
    text=[]
    with open(infile, 'r') as my_file:
        for line in my_file.readlines():
            sentence=line.strip('\n')
            split_line=" ".join(sp.encode_as_pieces(sentence))
            text.append(split_line)
            for piece in sp.encode_as_pieces(sentence):
                frequency.setdefault(piece, 0)
                frequency[piece] += 1
    freq_df=pd.DataFrame(list(frequency.items()), columns=['Word', 'Frequency'])
    freq_df=freq_df.sort_values(by=['Frequency'],ascending=False)
    total_words=freq_df['Frequency'].sum()
    freq_df['Probability']=freq_df['Frequency'].div(total_words)
    freq_df.to_csv(args.output_dir+name+'_'+str(args.size)+'_prob.csv',index=None,header=True)

    with open(args.output_dir+name+'_'+str(args.size)+'.txt', mode='wt') as out_file:
        out_file.write('\n'.join(text))
    print(text)
