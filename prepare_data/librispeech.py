import argparse
from pathlib import Path
import shutil

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--root')
    parser.add_argument('--split', choices={'test-clean', 'train-clean-100', 'dev-clean'})
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    
    return args

def main(args):
    
    data_dir = Path(args.root) / args.split
    output_dir = Path(args.output_dir)

    for speaker_dir in data_dir.iterdir():
        speaker_id = speaker_dir.stem
        output_speaker_dir = output_dir/speaker_id
        output_speaker_dir.mkdir(parents=True, exist_ok=True)
        for file in speaker_dir.glob('*/*.trans.txt'):
            for line in open(file):
                audio_id, text = line.strip().split(' ', 1)
                # shutil.copy(file.parent/f'{audio_id}.flac', output_speaker_dir/f'{audio_id}.flac')
                (output_speaker_dir/f'{audio_id}.flac').symlink_to(file.parent/f'{audio_id}.flac')
                print(text, file = open(output_speaker_dir/f'{audio_id}.lab', 'w'))


if __name__ == '__main__':

    args = get_args()
    main(args)
