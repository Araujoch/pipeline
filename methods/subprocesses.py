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
import re
from typing import Optional
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



import re

def advanced_text_filter(
    text: str,
    min_sentence_words: int = 2,
    max_sentence_words: int = 100,

    max_repetitions: int = 10,
    max_upper_ratio: float = 0.2,
    discard: int = 4
) -> bool:
    """
    Applies advanced heuristic filtering to a text document.

    Parameters:
        text (str): The document text.
        min_sentence_words (int): Minimum number of words allowed in a sentence.
        max_sentence_words (int): Maximum number of words allowed in a sentence.
        max_repetitions (int): Maximum allowed repetitions of the same word.
        max_upper_ratio (float): Maximum ratio of uppercase characters in the text.

    Returns:
        bool: True if the document passes the filter, False otherwise.
    """
    count_discard = 0
    # 1. Check credibility threshold
    if len(text) < 30:  # Minimum length threshold
        count_discard+=1
        #return False
    if len(text) > 10000:  # Maximum length threshold
        count_discard+=1
        #return False
    # 2. Detect suspicious characters
    if re.search(r"[^\w\sáéíóúÁÉÍÓÚñÑãẽĩõũ.,:;!?()\[\]\'\"\-]", text):
        count_discard+=1
        #return False

    # 3. Check uppercase ratio
    total_letters = sum(c.isalpha() for c in text)
    uppercase_letters = sum(c.isupper() for c in text)
    if total_letters > 0 and (uppercase_letters / total_letters) > max_upper_ratio:
        count_discard+=1
        #return False

    # 4. Check sentence length bounds
    sentences = re.split(r'[.!?]', text)
    for sentence in sentences:
        words = sentence.strip().split()
        if len(words) < min_sentence_words or len(words) > max_sentence_words:
            count_discard+=1
            #return False

    # 5. Check excessive word repetition
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = {word: words.count(word) for word in set(words)}
    if any(freq > max_repetitions for freq in word_freq.values()):
        count_discard+=1
        #return False

    return True if count_discard<discard else False

def detect_language_old(text: str, model) -> str:
    """
    Predict the language code for the given text using the fastText model.
    Returns the label without the '__label__' prefix.
    """
    labels, _probs = model.predict(text.strip(), k=1)
    return labels[0],_probs[0]

def quelingua_lines_old(text:str,model,args):
    # print(args.reliability) 
    if(advanced_text_filter(text)):
        label,reliability= detect_language_old(text,model)
        if('__label__gug_Latn' in label and reliability>args.reliability):#
            return label,reliability
    return None

def detect_language(text: str, model) -> str:
    """
    Predict the language code for the given text using the fastText model.
    Returns the label without the '__label__' prefix.
    """
    labels, _probs = model.predict(text.strip(), k=3)
    return labels,_probs

def quelingua_lines(text:str,model,args):
    # print(args.reliability)
    if(advanced_text_filter(text)):
        label,reliability= detect_language(text,model)
        result = dict(zip(label,reliability))
        for lbl, rel in result.items():
            if('__label__gug_Latn' in lbl and rel>args.reliability):
                return lbl, rel
    return None

