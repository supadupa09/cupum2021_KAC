# cupum2021_KAC

This is he supplementary material for the book chapter titled "Planning for Long-Term Climate Resilience: Analysing academic and non-academic literature to improve usage of Planning Support Systems" submitted for CUPUM 2021.

We used LiTCoF for text-mining analysis (Dayeen, F. R., Sharma, A. S., & Derrible, S. (2020). A text mining analysis of the climate change literature in industrial ecology. Journal of Industrial Ecology, 24(2), 276-284.).

Pre-processsing data for LiTCoF Analysis

(1) {Removal of words:} We first removed words that were overused but irrelevant such as results  copyright  important  provided  etc.  in addition to conjunctions  adverbs  mathematical symbols and numbers. We then removed relevant but overused words that did not bring much value to the analysis  but ended up skewing results like city  urban and data. The full list of words can be found in 'new_stop_words.txt' in 'src' folder.

(2) {Merging words}: Words that shared the same meaning like sustainable-sustainability, flooding-flood risk  flexibility-flexible were merged. Plural and singular versions of the same word were merged.
 
(3) {Grouping words:} This was the most important iteration to arrive at richer insights. Based on the preliminary rounds of analysis  we grouped together terms belonging to a single infrastructure sector or system to capture their combined frequencies. This was done in cases where terms on sub-sectors were too dispersed to provide relevant results.


Prerequisites for running the code:

1) Python 3.7 or higher installed on your machine.

- 'new_stop_words.txt' in 'src' folder contains the list of words we do not wish to consider for the analysis. 
- 'pre_processing _data.txt' in 'src' contains list of words that are grouped/merged together for the analysis.
- the abstracts for academic and non-academic (practice) are saved under 'data' in a .csv format. 

2) There are three folders with names: 'src', 'data', 'plots'. 
3) Run LiTCoF-v1.00.py in 'src' folder.
 
 