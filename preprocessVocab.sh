#!/bin/bash

sed "s/^\([A-Za-z]*\).*/\1/g" unprocessed_vocab.txt > vocab.txt