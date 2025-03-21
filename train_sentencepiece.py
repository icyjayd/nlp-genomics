import argparse
import sentencepiece as spm
parser = argparse.ArgumentParser()
parser.add_argument("input", help="text file to be used as input", type=str)
parser.add_argument("model_prefix", help = "prefix of output model", type=str)
parser.add_argument("vocab_size", help = "size of model vocabulary", type=int)
parser.add_argument("--pad_id", help="ID of pad token", type=int)
#/gpfs/data/johnsonslab/nlp-genomics/pasolli-2019/all_genomes_unlabeled_1000bp.txt
#'sp_1000bp_full'
#pad_id = 3
args = parser.parse_args()
print(args.model_prefix)

spm.SentencePieceTrainer.train(input=args.input, model_prefix=args.model_prefix, vocab_size=args.vocab_size, pad_id=args.pad_id)