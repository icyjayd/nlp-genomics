import sys
import sentencepiece as spm
import pandas as pd

name=str(sys.argv[1])
size=str(sys.argv[2])
print(name)
input_dir='/gpfs/data/ruggleslab/microbiome/projects/autoimmunity/studies/assembly/unique_seqs/'
output_dir='/gpfs/data/ruggleslab/microbiome/projects/autoimmunity/studies/assembly/probabilities/'
spm.SentencePieceTrainer.Train('--input='+input_dir+name+'_unique.txt --model_prefix='+name+'_'+size+' --vocab_size='+size+' --model_type=bpe --shuffle_input_sentence=true --max_sentence_length=25000 --max_sentencepiece_length=500 --num_sub_iterations=10')
sp=spm.SentencePieceProcessor()
sp.Load(name+'_'+size+".model")

vocabs = [sp.id_to_piece(id) for id in range(sp.get_piece_size())]
frequency={}
text=[]
with open(input_dir+name+'_unique.txt', 'r') as my_file:
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

with open(output_dir+name+'_'+str(size)+'.txt', mode='wt') as out_file:
    out_file.write('\n'.join(text))
print(text)
