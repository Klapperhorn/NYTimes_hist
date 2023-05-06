Key_uncertain=['suggests', 'possible', 'may', 'potentially', 'not adequately', 'should', 'will', 
'probably', 'hypothesis', 'could', 'implicate', 'perhaps', 'likely', 'might', 'perhaps', 
'possibility', 'possible', 'possibly', 'potentially', 'probably', 'seem', 'speculate', 
'whether', 'suspect', 'suppose', 'unsure', 'speculation', 'uncertainty']

Key_ignorance=['not understood', 'not been explored', 'not explored', 'not assessed' , 
'did not demonstrate', 'little is known', 'unexplored', 'unknown', 'not known', 'unclear', 
'not designed to', 'did not allow for', 'controversial', 'has not been determined', 
'have not been determined', 'incomplete', 'open question', 'not fully', 'not comprehensively', 
'not specifically', 'debated', 'contentious', 'unknown', 'further investigation', 'not intended to', 
'not planned to', 'not yield', 'not distinguish', 'not determined', 'not evaluated', 'not estimated', 
'not measured', 'not investigated', 'has not been specified', 'has not been settled', 'has not been concluded', 
'not been investigated', 'not been researched']

#hype according to the Miller et al.
hypeAdj=["experienced","important","relevant","essential","novel","senior","notable","unique",
"trained","significant","key","emphasize","exhaustive","comprehenisve","fundamental","specialized",
"excellent","unwanted","appropriate","innovative"," precise","strong","high","scarce","newer","useful",
"detailed","expert","critical","impactful","board-certified","high-volume","particular","qualified"]

hypeAdv=["very", "more", "particularly", "obviously", "well", "importantly", "even", "most highly", 
"especially", "greatly", "further", "markedly", "successfully", "much", "without question", "always", 
"objectively", "interestingly", "exactly", "specifically", "ever", "stricly", "certainly", "effectively", 
"easily", "steadily", "few", "entirely", "significantly", "unlike", "only", "all"]

hypeNoun=["strength", "importance", "robustness", "experience", "interest", "expert"]
hypeVer=["assure", "note succeed", "strengthen", "maximize", "reinforce", "empower", "highlight", "recognize"]

#manually added hype terms
hypeAdded=["fundamentally","transformed","in a world"]

# However, as it is interesting :D
Key_However=["however","but", "nevertheless","even so", "nonetheless", "still","though","yet","notwithstanding"]

#Combined Hypeterms
Key_hypes=hypeAdj+hypeAdv+hypeNoun+hypeVer+hypeAdded

def keyWords():


    d={"uncertainty": Key_uncertain,"ignorance": Key_ignorance, "hype": Key_hypes, "however": Key_However} 
    return d

def textCheck(txt,keys=Key_hypes):
   
    exp=[""]
    for parag in txt:
        for key in keys:
            if key in parag.lower(): ## To include capitalized strings, I added .lower() in the search
               # print(key)
                #uncertainD[key].extend([parag])
                match=""
                match=[match for match in parag.split(". ") if key in match]
                exp+=[match]
    return exp
