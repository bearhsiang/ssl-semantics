#!/usr/local/bin bash

root=/hdd/LibriSpeech
split=train-clean-100
output_dir=data/librispeech

python prepare_data/librispeech.py \
    --root $root \
    --split $split \
    --output-dir $output_dir