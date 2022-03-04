import argparse
from cProfile import label
import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from scipy import stats
from tqdm.auto import tqdm
import matplotlib.pyplot as plt

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--occur-file')
    parser.add_argument('--feat-dir')
    parser.add_argument('--sim-file')
    parser.add_argument('--w1-key', default='word1')
    parser.add_argument('--w2-key', default='word2')
    parser.add_argument('--score-key', default='similarity')
    parser.add_argument('--output-path')
    parser.add_argument('--output-title', default='')
    parser.add_argument('--max', type=int)
    args = parser.parse_args()

    return args

def similarity(a, b):    
    return - cosine_distances([a], [b])[0][0]

def sim_score(hyp, ref):    
    return stats.spearmanr(hyp, ref)


def output_fig(hyp, ref, occur_times, output_path, output_title):

    key=[min(x) for x in occur_times]
    sort_index = np.argsort(key)[::-1]

    new_hyp = [hyp[i] for i in sort_index]
    new_ref = [ref[i] for i in sort_index]
    new_occur_times = [occur_times[i] for i in sort_index]

    data = {
        'score': [],
        'p_value': [],
        'N': [],
        'id': [],
    }

    for i in range(len(new_hyp)):
        score, p_value = sim_score(new_hyp[:i+1], new_ref[:i+1])
        data['score'].append(score)
        data['p_value'].append(p_value)
        data['N'].append(min(new_occur_times[i]))
        data['id'].append(i)

    fig, ax1 = plt.subplots()
    c1, c2 = 'red', 'blue'
    ax1.plot(data['id'], data['score'], color=c1, label='score')
    ax1.plot(data['id'], data['p_value'], color=c1, linestyle='dashed', label='p value')
    ax1.set_xlabel('rank')
    ax1.set_ylabel('score', color=c1)
    ax1.tick_params(axis='y', labelcolor=c1)
    ax2 = ax1.twinx()
    ax2.plot(data['id'], data['N'], color=c2, label='N')
    ax2.set_ylabel('N', color=c2)
    ax2.tick_params(axis='y', labelcolor=c2)
    ax1.set_title(output_title)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.legend()
    fig.savefig(output_path)

def main(args):

    w_feats = {}
    w_occur_times = {}

    words = [line.strip().split('\t')[0] for line in open(args.occur_file)]

    df = pd.read_csv(args.sim_file, index_col=0)
    df = df[df[args.w1_key].isin(words) & df[args.w2_key].isin(words)]

    candidate_words = set(pd.concat([df[args.w1_key], df[args.w2_key]]))
    
    feat_dir = Path(args.feat_dir)

    for line in tqdm(open(args.occur_file)):
        w, occurs = line.strip().split('\t')
        occurs = occurs.split('|')
        if args.max and args.max > 0:
            occurs = occurs[:args.max]
        if w in candidate_words:
            w_occur_times[w] = len(occurs)
            w_feat = None
            count = 0
            for segment in tqdm(occurs):
                feat_file, min_time, max_time, total_time = segment.split('_')
                feat_file = feat_dir / f'{feat_file}.npy'
                min_time = float(min_time)
                max_time = float(max_time)
                total_time = float(total_time)
                total_feat = np.load(feat_file)
                start = round(min_time / total_time * total_feat.shape[0])
                end = round(max_time / total_time * total_feat.shape[0])
                feat = np.mean(total_feat[start:end], axis=0)
                if count >= 1:
                    w_feat += feat
                else:
                    w_feat = feat
                count += 1
            w_feat /= count
            w_feats[w] = w_feat

    hyps, refs = [], []

    pair_occur_times = []

    for item in df.iterrows():
        item = item[1]
        w1, w2 = item[args.w1_key], item[args.w2_key]
        if w1 in w_feats and w2 in w_feats:
            hyp = similarity(w_feats[w1], w_feats[w2])
            ref = item[args.score_key]
            hyps.append(hyp)
            refs.append(ref)
            pair_occur_times.append((w_occur_times[w1], w_occur_times[w2]))
    
    sim_result = sim_score(hyps, refs)
    print(sim_result)
    output_fig(hyps, refs, pair_occur_times, args.output_path, args.output_title)



if __name__ == '__main__':

    args = get_args()
    main(args)