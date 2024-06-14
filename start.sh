#!/bin/bash

git clone --depth 1 https://github.com/wahoosjw/wen_patch.git
python ./wen_patch/bot_test.py --config /etc/config.cfg
