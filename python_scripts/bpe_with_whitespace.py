import pickle
import argparse

class BPE():
    def __init__(self, vocab_size, corpus, unk="<UNK>"):
        self.vocab_size = vocab_size
        self.corpus = [[c for c in line[: len(line) if line.find("\n") == -1 else -1] ] for line in corpus]
        self.vocab = set()
        self.merge = {}
        self.unk = unk
        for line in self.corpus:
            self.vocab = self.vocab.union(set(line))
        self.init_vocab_size = len(self.vocab)
        self.vocab = list(self.vocab)
        self.vocab = [self.unk] + self.vocab
        self.vocab = dict(zip(self.vocab, list(range(len(self.vocab)))))

    def train(self):
        corpus = self.corpus
        pair_freqs = {}
        new_corpus = []
        ##get most frequent tokens
        for i in range(self.init_vocab_size, self.vocab_size):
            for line in corpus:
                for i in range(len(line)-1):
                    if (line[i], line[i+1]) in pair_freqs.keys():
                        pair_freqs[(line[i], line[i+1])] += 1
                    else:
                        pair_freqs[(line[i], line[i+1])] = 1
            max_pair = max(pair_freqs, key=pair_freqs.get)
            new_token = "".join(max_pair)
            # print(new_token)
            self.merge[max_pair] = new_token
            self.vocab[new_token] = max(self.vocab.values()) + 1
            for line in corpus:
                # print("pristine line:", line)
                for i in range(len(line)-1):
                    # print("i:", i)
                    # print(i)
                    if i < len(line)-1:
                        if line[i] == max_pair[0] and line[i + 1] == max_pair[1]:
                            line[i] = new_token
                            line.pop(i+1)

    def tokenize(self, strings, ids=True):
        if type(strings)!= list:
            assert type(strings) == str, "input must be string or list of strings"
            strings = [strings]
        tokenized_strings = []
        for string in strings:
            string = list(string)
            while True:
                cur_len = len(string)
                for i in range(len(string)-1):
                    if i < len(string)-1:
                        if (string[i], string[i+1]) in self.merge.keys():
                            string[i] = self.merge[(string[i], string[i+1])]
                            string.pop(i+1)
                if len(string)== cur_len:
                    if ids:
                        tokenized_strings.append([self.vocab[s] if s in self.vocab.keys() else self.vocab[self.unk] for s in string])
                    else:
                        all_in_vocab = True
                        for i in range(len(string)):
                            all_in_vocab = string[i] in self.vocab.keys()
                            if not all_in_vocab:
                                string[i] = self.unk

                        tokenized_strings.append(string)
                    break
                else:
                    cur_len = len(string)
        return tokenized_strings

    def save(self, path):
        with open(path, 'wb') as out:
            pickle.dump(self, out, pickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
    parser =argparse.ArgumentParser(description="Train a byte pair encoding tokenizer which incorporates white space into its tokens")
    parser.add_argument("vocab_size", type=int)
    parser.add_argument("corpus_path", type=str)
    parser.add_argument("out_prefix", type=str)
    parser.add_argument("--unk_token", type=str, default="<UNK>")
    args = parser.parse_args()
    vocab_size = args.vocab_size
    corpus_path = args.corpus_path
    out_prefix = args.out_prefix
    unk_token = args.unk_token
    with open(corpus_path) as f:
        corpus = f.readlines()

    bpe = BPE(vocab_size, corpus, unk_token)
    bpe.train()
    bpe.save(out_prefix + "_" + str(vocab_size) + ".pkl")
