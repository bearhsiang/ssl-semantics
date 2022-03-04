#!/usr/local/bin bash

lexicon=english
acoustic=english

data_dir=data/LibirSpeech
output_dir=data/tmp

mfa validate $data_dir $lexicon $acoustic
mfa align $data_dir $lexicon $acoustic $output_dir