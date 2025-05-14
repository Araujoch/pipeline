from collections import Counter
from queue import Full
import subprocess
import json
import sys
import os
from pyplexity import PerplexityModel, PerplexityProcessor
from pyplexity.tag_remover import HTMLTagRemover
import tqdm
from collections import Counter
import fasttext
import math
from huggingface_hub import hf_hub_download

from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))

def mt_assert_parallel(src_file: str, tgt_file: str):
    #check that both files have the same number of lines 
    with open(src_file, "r", encoding='utf-8') as src:
        with open(tgt_file, "r", encoding='utf-8') as tgt:
            src_lines = src.readlines()
            tgt_lines = tgt.readlines()
            if len(src_lines) != len(tgt_lines):
                raise Exception(f"Source and target files have different number of lines: {len(src_lines)} and {len(tgt_lines)}")
    return

def read_file_line_by_line(file):
    with open(file, "r", encoding='utf-8') as f:
        for line in f:
            yield line


def detect_language(text: str, model) -> str:
    """
    Predict the language code for the given text using the fastText model.
    Returns the label without the '__label__' prefix.
    """
    labels, _probs = model.predict(text.strip(), k=1)
    return labels[0],_probs[0]
def quelingua_lines(text:str,model):
    label,credibility= detect_language(text,model)
    if('__label__gug_Latn' in label and credibility>=0.8):#
        return label,credibility
    return None

