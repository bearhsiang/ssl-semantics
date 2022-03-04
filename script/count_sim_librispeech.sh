#!/usr/local/bin bash

dataset=LibriSpeech
model=hubert
layer=9
split=train-clean-100
feat_dir=/hdd/ssl_feat/librispeech/$model/$layer/$split
sim_set=mc-30
sim_file=word-benchmarks/word-similarity/monolingual/en/$sim_set.csv
output_dir=output/word-similarity

python utils/feature_sim.py \
    --occur-file data/occur/$dataset.txt \
    --feat-dir $feat_dir \
    --sim-file $sim_file \
    --output-path $output_dir/$sim_set/$split/$model-L$layer.png \
    --output-title "$sim_set $split $model L$layer" \
    --max 1000

