# Serdar-Ortac-Lyric-Generator

Markow Chain model for generating Serdar Ortaç lyrics (in fact any lyrics with mechanic rhymes and loose grammar). Levenshtein similarity is used for ryhmes. You can optionally input starting words of lyrics. Model writes 4 lines of lyrics with stochastic rhyme, number of words logic.

Example usage:

```
import os
os.chdir(r"..\serdarortac") #file containing lyrics
from serdarortac import *
idir = os.path.join(os.getcwd(),"lyrics")
ortac_fwprobdict, ortac_bwprobdict = readLyrics(idir)
print("Here's your Serdar Ortac lyrics:\n")"
print(makeSerdarOrtac("", ortac_fwprobdict, ortac_bwprobdict))
```
Here's your Serdar Ortac lyrics:

 sıkı dur  
 yaşanan hayal kurup dualar  
 uyanır dururum yakalar  
 eriyor gittin gideli güvenim
