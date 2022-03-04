#!/usr/local/bin bash

dataset=librispeech
model=hubert
layer=6
split=train-clean-100
feat_dir=/hdd/ssl_feat/$dataset/$model/$layer/$split
sim_set=yp-130
sim_file=word-benchmarks/word-similarity/monolingual/en/$sim_set.csv
output_dir=output/word-similarity

python utils/feature_sim.py \
    --occur-file data/occur/$dataset.txt \
    --feat-dir $feat_dir \
    --sim-file $sim_file \
    --output-path $output_dir/$sim_set/$dataset-$split/$model-L$layer.png \
    --output-title "$sim_set $dataset $split $model L$layer" \
    --max 1000

