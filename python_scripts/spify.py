import sentencepiece as spm
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, default = "NoteTextSentences.txt", help="filename to be SP-ified")
    parser.add_argument("model",type=str, default="RawnoteText_32000.model", help="SP model file" )
    parser.add_argument("-out", type = str, default="out.txt", help="name of outputfile")
    args = parser.parse_args()
    sp = spm.SentencePieceProcessor()
    sp.load(args.model)
    f = open(args.file, 'r')
    with open(args.out, "w") as o:
        for line in f:
            o.write(" ".join(sp.EncodeAsPieces(line)) + "\n")
    f.close()
    o.close()
