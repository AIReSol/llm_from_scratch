"""Byte Pair Encoding (BPE) Algorithm Implementation.

An implementation of the Byte Pair Encoding (BPE) algorithm from:
https://arxiv.org/pdf/1508.07909, Algorithm 1.

The initial vocabulary contains words split into individual symbols (letters)
and the special end-of-word token </w>. Through multiple rounds of merging,
the algorithm generates combinations of existing symbols. The process stops
when a predefined number of rounds.
"""

import re, collections

def get_stats(vocab):
    """
    Get the frequency of pairs of symbols in a vocabulary.

    Args:
        vocab (dict): A vocabulary of words and their frequencies.

    Returns:
        dict: A dictionary of pairs of symbols and their frequencies.
    """

    # initialize paris as empty dict, default value is 0 for counting
    # count the frequency of consecutive symbols
    pairs = collections.defaultdict(int)

    # loop through each word in vocab
    for word, freq in vocab.items():
        # split into individual symbol/letter 
        symbols = word.split()

        # combine consecutive symbols and count frequency
        for i in range(len(symbols) - 1):
            # symbols[i], symbols[i+1]: this is a tuple
            pairs[symbols[i], symbols[i + 1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    """
    Merge a pair of symbols in a vocabulary.

    Args:
        pair (string): a pair of symbols as a string.
        v_in (_type_): a vocabulary of token (pairs) and their frequencies

    Returns:
        dict: a vocabulary of tokens (pairs) and their frequencies.
    """
    # updated vocab with merged pair
    v_out = {}

    # escape special characters in the pair
    # bi-gram: bi-two, gran-unit
    # by default the symbols are separated by white space
    bigram = re.escape(' '.join(pair))

    # compiled regular expression patter (p)
    # r'(?<!\S)': negative lookbehind, no non-whitespace before the bigram
    # r'(?!\S)': negative lookahead, no non-whitespace after the bigram
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')

    for word in v_in:
        # replace 'e s' with 'es' in the words containing 'e s'
        w_out = p.sub(''.join(pair), word)
        # update the output vocabulary
        v_out[w_out] = v_in[word]

    return v_out

if __name__ == '__main__':
    vocab = {'l o w </w>': 5, 'l o w e r </w>': 2,
            'n e w e s t </w>': 6, 'w i d e s t </w>': 3}
    num_merges = 10
    for i in range(num_merges):
        # get paris of consecutive symbols and their frequencies
        pairs = get_stats(vocab)
        # get the most frequent pair
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)

        print(f'{i}: ', '-' * 100)
        print('pairs:', dict(pairs))
        print('best:', best)
        print('vocabulary:', vocab)
        print()