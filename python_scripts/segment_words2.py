# import sentencepiece as spm

# spm.SentencePieceTrainer.Train('--input=E:/Documents/JohnsonLab/RawNoteText.txt --model_prefix=SentencePiece32k --vocab_size=32000 --character_coverage=1.0 --model_type=unigram')

import sys
import sentencepiece as spm
import pandas as pd
import io
# coding: utf-8
name='kang_data_cleaned'
size=str(8000)
print(name)
input_dir='E:/Documents/JohnsonLab/'
output_dir='E:/Documents/JohnsonLab/'
spm.SentencePieceTrainer.Train('--input='+input_dir+name + '.txt --model_prefix='+output_dir+name+'_'+size+' --vocab_size='+size+' --model_type=unigram --shuffle_input_sentence=true --max_sentence_length=25000 --max_sentencepiece_length=500 --num_sub_iterations=10 --pad_id=0 --unk_id=1 --bos_id=2 --eos_id=3')
sp=spm.SentencePieceProcessor()
sp.Load(input_dir + name+'_'+size+".model")

vocabs = [sp.id_to_piece(id) for id in range(sp.get_piece_size())]
frequency={}
text=[]
with open(input_dir+name+'.txt', 'r') as my_file:
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
freq_df.to_csv(output_dir+name+'_'+str(size)+'_prob.csv',index=None,header=True)

with io.open(output_dir+name+'_'+str(size)+'.txt', 'wt',encoding="utf-8") as out_file:
    out_file.write('\n'.join(text))
print(text)
