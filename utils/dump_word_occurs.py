import argparse
from pathlib import Path
from collections import defaultdict
import textgrid
from tqdm.auto import tqdm

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir')
    parser.add_argument('--output')
    args = parser.parse_args()
    
    return args

def main(args):
    
    data_dir = Path(args.data_dir)

    results = defaultdict(list)

    for file in tqdm(list(data_dir.glob('**/*.TextGrid'))):
        tg = textgrid.TextGrid.fromFile(file)
        total_time = tg.maxTime
        for interval in tg[0]:
            w = interval.mark
            min_time, max_time = interval.minTime, interval.maxTime
            if w:
                results[w].append(f'{file.stem}_{min_time}_{max_time}_{total_time}')
    
    words = sorted(results.keys(), key = lambda w: len(results[w]), reverse=True)

    with open(args.output, 'w') as f:

        for w in words:
            print(w, '|'.join(results[w]), sep='\t', file=f)
        

if __name__ == '__main__':

    args = get_args()
    main(args)