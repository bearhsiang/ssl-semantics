#!/usr/local/bin bash

root=/hdd/LibriSpeech
split=train-clean-100
output_dir=data/LibriSpeech

python prepare_data/librispeech.py \
    --root $root \
    --split $split \
    --output-dir $output_dir