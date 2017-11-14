# -*- coding: utf-8 -*-
"""
@author: KBK
"""

import random
from scipy.stats import norm
import sys
from editdistance import eval as lev

def readLyrics(idir,fw_freqdict={},bw_freqdict={}):
    """
    returns a dict in following form:
    word : {successor1: probability, successor2:probability}
    """
    files = os.listdir(idir)
    for fl in files:
        with open(os.path.join(idir,fl),"r") as f:
            corpus = fixChars(f.read())
            lines = corpus.replace("\n\n","\n").strip().lower().split("\n")
            for l in lines:
                words = l.strip().replace("  "," ").split()          
                for curr, succ in list(set(zip(words[:-1], words[1:]))):
                    #set is used for unique sequence effect per song (nakarat etkisinden korumak)
                    if curr not in fw_freqdict:
                        fw_freqdict[curr] = {succ: 1}
                    if succ not in bw_freqdict:
                        bw_freqdict[succ] = {curr: 1}
                    else:
                        if succ not in fw_freqdict[curr]:
                            fw_freqdict[curr][succ] = 1
                        else:
                            fw_freqdict[curr][succ] += 1
                        if curr not in bw_freqdict[succ]:
                            bw_freqdict[succ][curr] = 1
                        else:
                            bw_freqdict[succ][curr] += 1
     
     
    #convert freq_dict to prob_dict
    fw_probdict = {}
    for curr, curr_dict in fw_freqdict.items():
		fw_probdict[curr] = {}
		curr_total = sum(curr_dict.values())
		for succ in curr_dict:
			fw_probdict[curr][succ] = float(curr_dict[succ]) / curr_total
    
    bw_probdict = {}
    for succ, succ_dict in bw_freqdict.items():
		bw_probdict[succ] = {}
		succ_total = sum(succ_dict.values())
		for curr in succ_dict:
			bw_probdict[succ][curr] = float(succ_dict[curr]) / succ_total
    
    return fw_probdict, bw_probdict
                           
def markov_next(curr, prob_dict):
	if curr not in prob_dict:
		return random.choice(list(prob_dict.keys()))
	else:
		succ_probs = prob_dict[curr]
		rand_prob = random.random()
		curr_prob = 0.0
		for succ in succ_probs:
			curr_prob += succ_probs[succ]
			if rand_prob <= curr_prob:
				return succ

def markov_prev(curr, prob_dict):
	if curr not in prob_dict:
		return random.choice(list(prob_dict.keys()))
	else:
		pred_probs = prob_dict[curr]
		rand_prob = random.random()
		curr_prob = 0.0
		for prev in pred_probs:
			curr_prob += pred_probs[prev]
			if rand_prob <= curr_prob:
				return prev

def makeSerdarOrtac(curr, fw_probdict,bw_probdict, nlines = 4):
    lyrics = [curr]
    l = 1 #current n lines
    w = len(lyrics) #n words in the current line
    while l <= nlines:
        if l == 1:          
            cur_rand = random.random()
            threshold = norm.cdf(w,loc=4,scale=1.2) # we want roughly 4 words per line 
            if cur_rand > threshold:
                lyrics.append(markov_next(lyrics[-1],fw_probdict))
                w += 1
            else:
                lyrics.append("\n")
                w = 0
                l += 1
        elif l < nlines:
            if lyrics[-1] == "\n":
                prev = random.choice(list(fw_probdict.keys()))
                sim = levenshteinSimilarity(lyrics[-2],prev)
                eps = 0
                while sim < 0.75-eps+random.random()/4 and eps<0.50: #500 trials else random
                    prev = random.choice(list(fw_probdict.keys()))
                    sim = levenshteinSimilarity(lyrics[-2],prev)
                    eps+=0.001
                lyrics.append(prev)
                w += 1
            else:
                cur_rand = random.random()
                threshold = norm.cdf(w,loc=4,scale=1.2) # we want roughly 4 words per line 
                if cur_rand > threshold:
                    lyrics.insert(-w,markov_prev(lyrics[-w],bw_probdict))
                    w += 1
                else:
                    lyrics.append("\n")
                    w = 0
                    l += 1
        elif l == nlines:
            cur_rand = random.random()
            threshold = norm.cdf(w,loc=4,scale=1.2) # we want roughly 4 words per line 
            if cur_rand > threshold:
                lyrics.append(markov_next(lyrics[-1],fw_probdict))
                w += 1
            else:
                lyrics.append("\n")
                w = 0
                l += 1            
                
    return " ".join(lyrics)

def fixChars(text):
    for p in [".",",","!","?",":",";","x","(",")"]:
        text = text.replace(p," ")
    for p in [str(i) for i in range(10)]: #numbers
        text = text.replace(p,"")
    repl = [("â","a"),("û","u"),("Ş","ş"),("Ç","ç"),("Ü","ü"),("İ","i"),("Ö","ö")]
    for a,b in repl:
        text = text.replace(a,b)
    return text

def levenshteinSimilarity(a,b):
    sim = (max(len(a),len(b))-lev(a,b))/float(max(len(a),len(b)))
    return sim

    
if __name__ == '__main__':
    import os
    os.chdir("..\serdarortac") #directory containing lyrics 
	
    idir = os.path.join(os.getcwd(),"lyrics")
    ortac_fwprobdict, ortac_bwprobdict = readLyrics(idir)
    
    start_word = raw_input("What do you want to start your song with?\n > ")
    print("Here's your Serdar Ortac lyrics:\n")
    print(makeSerdarOrtac(start_word, ortac_fwprobdict, ortac_bwprobdict))
    

    
