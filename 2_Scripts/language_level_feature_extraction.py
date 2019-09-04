# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:44:16 2017

@author: jsuter

Project: Language Level Analysis and Classification
Seminar "Educational Assessment for Language Technology" 
WS 2015/16, Magdalena Wolska

Julia Suter, January 2018

-----------------------------------------------------------------

language_level_feature_extraction.py

- get parsed sentences for input text
- extract features 
- color specific linguistic patterns
- save results in output file 

"""

### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 
### Import Statements
### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 

from __future__ import division

import os
import shutil
import subprocess
from subprocess import PIPE

import parse_information as easy_parse
import config
   
import itertools
import codecs
import pickle

import sys
#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')


### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 
### Set word lists etc.
### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 


# German stopwords (derived from NLTK)
german_stopwords = ['aber', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'also', 'am', 'an', 'ander', 'andere',
                    'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern', 'anderr', 'anders', 'auch', 'auf',
                    'aus', 'bei', 'bin', 'bis', 'bist', 'da', 'damit', 'dann', 'der', 'den', 'des', 'dem', 'die',
                    'das', 'da\xdf', 'derselbe', 'derselben', 'denselben', 'desselben', 'demselben', 'dieselbe',
                    'dieselben', 'dasselbe', 'daz', 'dein', 'deine', 'deinem', 'deinen', 'deiner', 'deines', 'denn',
                    'derer', 'dessen', 'dich', 'dir', 'd', 'dies', 'diese', 'diesem', 'diesen', 'dieser', 'dieses',
                    'doch', 'dort', 'durch', 'ein', 'eine', 'einem', 'einen', 'einer', 'eines', 'einig', 'einige',
                    'einigem', 'einigen', 'einiger', 'einiges', 'einmal', 'er', 'ihn', 'ihm', 'es', 'etwas', 'euer',
                    'eure', 'eurem', 'euren', 'eurer', 'eures', 'für', 'gegen', 'gewesen', 'hab', 'habe', 'haben',
                    'hat', 'hatte', 'hatten', 'hier', 'hin', 'hinter', 'ich', 'mich', 'mir', 'ihr', 'ihre', 'ihrem',
                    'ihren', 'ihrer', 'ihres', 'euch', 'im', 'in', 'indem', 'ins', 'ist', 'jede', 'jedem', 'jeden',
                    'jeder', 'jedes', 'jene', 'jenem', 'jenen', 'jener', 'jenes', 'jetzt', 'kann', 'kein', 'keine',
                    'keinem', 'keinen', 'keiner', 'keines', 'können', 'könnte', 'machen', 'man', 'manche', 'manchem',
                    'manchen', 'mancher', 'manches', 'mein', 'meine', 'meinem', 'meinen', 'meiner', 'meines', 'mit',
                    'muss', 'musste', 'nach', 'nicht', 'nichts', 'noch', 'nun', 'nur', 'ob', 'oder', 'ohne', 'sehr',
                    'sein', 'seine', 'seinem', 'seinen', 'seiner', 'seines', 'selbst', 'sich', 'sie', 'ihnen', 'sind',
                    'so', 'solche', 'solchem', 'solchen', 'solcher', 'solches', 'soll', 'sollte', 'sondern', 'sonst',
                    'über', 'um', 'und', 'uns', 'unsere', 'unserem', 'unseren', 'unser', 'unseres', 'unter', 'viel',
                    'vom', 'von', 'vor', 'während', 'war', 'waren', 'warst', 'was', 'weg', 'weil', 'weiter', 'welche',
                    'welchem', 'welchen', 'welcher', 'welches', 'wenn', 'werde', 'werden', 'wie', 'wieder', 'will',
                    'wir', 'wird', 'wirst', 'wo', 'wollen', 'wollte', 'würde', 'würden', 'z', 'zum',
                    'zur', 'zwar', 'zwischen']
             

# Verbs of talking
# derived from: https://norberto68.wordpress.com/2011/02/22/wortfeld-sprechen-sagen-reden/
# used for indirect speech detection

verbs_of_talking = ['sprechen','schweigen','sagen', 'fragen', 'berichten', 'meinen','behaupten','antworten','erklären',
                    'ablehnen',
                    'abstreiten','andeuten','anerkennen','anfahren','angeben','anklagen','ankündigen','anmerken',
                    'annehmen','anordnen','ansagen', 'anschreien','anspornen','ansprechen','anstacheln','anvertrauen', 
                    'anweisen', 'argumentieren', 'auffordern', 'aufhetzen', 'aufklären', 'aufmuntern', 'aufsagen', 
                    'aufschwatzen', 'auftragen', 'auftrumpfen', 'aufzählen', 'ausdrücken', 'ausführen', 'ausplaudern', 
                    'ausrichten', 'ausrufen', 'aussagen', 'äußern', 'aussprechen', 'beantragen', 'beanspruchen',
                    'bedanken',
                    'befragen', 'befürworten', 'begründen', 'beichten', 'beipflichten', 'bejahen', 'bejammern',
                    'bekanntgeben', 'bekennen',
                    'beklagen', 'belegen', 'beleidigen', 'bemerken', 'benachrichtigen', 'benennen', 'beraten',
                    'berichten', 'berichtigen',
                    'beschimpfen', 'beschließen', 'beschuldigen', 'beschwatzen', 'beschwören', 'bestätigen',
                    'bestimmen', 'bestreiten',
                    'bestürmen', 'beten', 'beteuern', 'betteln', 'beurteilen', 'beweisen', 'bewerten', 'bezeichnen',
                    'bezeugen', 'bezweifeln',
                    'billigen', 'brummen', 'brüsten', 'darlegen', 'darstellen', 'dazwischenreden', 'debattieren',
                    'definieren', 'dementieren',
                    'deuten', 'dichten', 'diskutieren', 'durchsagen', 'eingestehen', 'einleiten', 'einreden',
                    'einwenden', 'einwerfen', 'entgegnen', 'entscheiden',
                    'entschlüpfen', 'entschuldigen', 'erinnern', 'ermuntern', 'ermutigen', 'erörtern', 'erwähnen',
                    'erwidern', 'exemplifiziren', 'falsifizieren',
                    'faseln', 'feststellen', 'fluchen', 'fordern', 'formulieren', 'fortfahren', 'freisprechen',
                    'gebieten', 'geloben', 'genehmigen', 'gestehen', 'grölen',
                    'gutheißen', 'herausreden', 'herunterrasseln', 'herunterspielen', 'hervorheben', 'hervorstoßen',
                    'hetzen', 'hineinreden', 'hinweisen', 'hinzufügen', 'interpretieren',
                    'interviewen', 'jammern', 'jauchzen', 'johlen', 'jubeln', 'jubilieren', 'klagen', 'klarmachen',
                    'klarstellen', 'klassifizieren', 'klatschen', 'kommandieren',
                    'kommentieren', 'kondolieren', 'konfrontieren', 'konkretisieren', 'krächzen', 'kreischen',
                    'kritisieren', 'kundgeben', 'lachen', 'lallen', 'lamentieren', 'lästern', 'lehren', 'leugnen',
                    'lispeln', 'lospoltern', 'lossagen', 'meinen', 'melden', 'missbilligen', 'mitteilen', 'moderieren',
                    'munkeln', 'murmeln', 'nachgeben', 'nachplappern', 'nachsagen',
                    'nachsprechen', 'nebenordnen', 'negieren', 'nörgeln', 'offenbaren', 'paraphrasieren', 'plappern',
                    'plaudern', 'postulieren', 'präzisieren', 'predigen', 'preisen', 'protestieren',
                    'quengeln', 'radebrechen', 'raten', 'raunen', 'referieren', 'reklamieren', 'richtigstellen',
                    'schildern', 'schließen', 'schmeicheln', 'schwatzen', 'schwätzen', 'schwören', 'seufzen',
                    'spezifizieren', 'spotten', 'stammeln', 'staunen', 'sticheln', 'stocken', 'stöhnen', 'stottern',
                    'subsumieren', 'tadeln', 'tuscheln', 'übermitteln', 'überordnen', 'überreden',
                    'übertreiben', 'überzeugen', 'unterhalten', 'unterordnen', 'unterreden', 'untersagen',
                    'unterstellen', 'unterstreichen', 'unterweisen', 'urteilen', 'verabschieden', 'verallgemeinern',
                    'verbitten', 'verdeutlichen', 'vergleichen', 'verheißen', 'verhören', 'verifizieren', 'verkünden',
                    'verleugnen', 'verneinen', 'versichern', 'verspotten', 'versprechen',
                    'verständigen', 'verteidigen', 'verweigern', 'verweisen', 'verzeihen', 'voraussagen', 'vorbringen',
                    'vorhalten', 'vorhersagen', 'vorschreiben', 'vorstellen',
                    'vortragen', 'vorwerfen', 'weigern', 'weitersagen', 'widerlegen', 'widerrufen', 'wiedergeben',
                    'wimmern', 'wundern', 'würdigen', 'zerreden', 'zitieren', 'zugeben', 'zugestehen',
                    'zurechtweisen', 'zurückgeben', 'zurückweisen', 'zusagen', 'zusammenfassen', 'zustimmen',
                    'zutexten', 'zuweisen']


# subordinating conjunction types

conj_dict = {'causal':0,
             'concessive':0,
             'conditional':0,
             'consecutive':0,
             'final':0,
             'interrogative':0,
             'modal':0,
             'other':0,
             'temporal':0 }     # originally:  + adversative + local
             
             
# list of frequent subordinating conjunctions

temporal =      ['als',  'während',   'seit',   'seitdem',  'solange',   'sobald', 'sooft', 'sowie',
                 'nachdem', 'kaum dass', 'bis', 'bevor', 'ehe' ]
conditional =   ['falls', 'wenn', 'sofern', 'ausser wenn', 'sofern']
causal =        ['weil', 'da','zumal','deshalb', 'denn', 'wegen']
concessive =    ['obwohl','obgleich','obschon', 'wennschon', 'auch wenn', 'selbst wenn', 'sogar wenn', 'wenn auch']
consecutive =   ['dass', 'sodass', 'ohne dass', 'so dass','als dass', 'daher']
final =         ['damit', 'dass', 'auf dass', 'um']
modal =         ['indem', 'dadurch dass', 'ohne dass', 'ausser dass','soviel', 'soweit', 'anstatt',
                 'als ob', 'als', 'wie']
interrogative = ['wer','was','welcher','welches','welche','wann','wo','wem','ob','warum','wie','wen','wessen',
                 'wohin','woher','weshalb']


# Features divided by categories

pos_features = ['Nouns','Verbs','Adjectives','Pronouns',
                'Particles','Punctuation marks','Splittable prefix',
                'Full verbs','Auxiliary verbs','Modal verbs',
                'Poss pronouns','Refl pronouns', 'Genitive modifiers',
                'Prepositions with genitive']
    
pattern_features = ['Subjunctions','Conjunctions',
                    'Relative clauses', 'Participial constructions',
                    'Placeholder es', 'Negations', 'Questions', 'Inversions',
                    'Indirect speech','Irrealis',
                    'Brauchen constructions','Lassen constructions']

passive_features = ['Passive', 'Passive agens']

case_features = ['Nominative','Genitive','Dative','Accusative']

obj_features = ['Genitive objects','Dative objects','Accusative objects','Prepositional objects']

tempus_features = ['Present', 'Perfect', 'Plusquamperfect','Past simple', 'Futur']

mode_features = ['Subjunctive 1','Subjunctive 2', 'Imperatives']

adj_features = ['Comparative adjectives','Superlative adjectives']

coref_features = ['Discourse entities']
    
# combine all features   
all_features = (pos_features, case_features, obj_features, tempus_features, mode_features, passive_features, \
                pattern_features, adj_features, coref_features)

# color dictionary for color phenomenons

color_dict = {             
              'Nouns':'brown',
              'Verbs':'blue',
              'Adjectives':'yellow',
              'Pronouns':'orange',
              'Particles':'green',
              'Punctuation marks':'magenta',
              'Splittable prefix':'rgb(255, 153, 153)',
              'Full verbs':'gray',
              'Auxiliary verbs':'rgb(153, 0, 204)',
              'Modal verbs':'rgb(77, 0, 77)',
              'Poss pronouns':'olive',
              'Refl pronouns':'lime',
              
              
              'Comparative adjectives':'goldenrod',
              'Superlative adjectives':'per',
              
              'Genitive modifiers':'coral',
              'Prepositions with genitive':'rgb(255, 51, 0)',
              
              'Nominative':'rgb(173, 216, 230,0.5)',
              'Accusative': 'rgb(0, 128, 0,0.5)',
              'Dative': 'rgb(0, 0, 255, 0.5)',
              'Genitive': 'rgb(255, 165, 0,0.5)',
              
              'Accusative objects': 'green',
              'Dative objects': 'blue',
              'Genitive objects': 'orange',
              'Prepositional objects':'LightBlue',
              
              
              'Present':'rgb(255, 160, 122,0.2)',
              'Past simple':'rgb(220, 20, 60,0.7)',
              'Futur':'rgb(255, 153, 255,0.7)',
              'Perfect':'rgb(205, 92, 92,0.7)',
              'Plusquamperfect':'rgb(139, 0, 0,0.7)',
             
              
              'Subjunctive 1':'rgb(255, 102, 153)',
              'Subjunctive 2':'rgb(204, 0, 102)',
              'Imperatives':'rgb(153, 0, 204)',
              
              'Indirect speech':'rgb(0, 102, 255)',
              'Irrealis':'rgb(51, 51, 153)',
              
              'Passive':'mediumblue',
              'Passive agens':'navy',
             
              'Relative clauses':'rgb(0, 204, 102)',
              'Conjunctions':'rgb(0, 77, 77)',
              'Subjunctions':'teal',
              
              'Participial constructions':'rgb(0, 153, 51)',
              
              'Questions':'mediumvioletred',
              
              'Brauchen constructions':'mediumpurple',
              'Lassen constructions':'darkorchid',
              'Inversions':'rosybrown',
              
              'Discourse entities': 'rgb(51, 0, 51)',

              'Placeholder es':'rgb(255, 153, 0)',
              'Negations':'rgb(204, 0, 0)',              
              
              None:'black'          
              }
                 

### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 
### Read and parse texts
### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 

def get_sentences_from_unparsed_text(doc, save_in_dir):
    """Return ParZu and CorZu parsed sentences for input document"""
        
    input_type = 'cat'
    
    # parse document and store results in /CorZu_results  
    cmd = "%(type)s %(filename)s | " \
          "python %(parse_path)s/ParZu_NEW/parzu -q -o conll > "\
          "%(parse_res_path)s/parsed.conll && "\
          "python %(parse_path)s/CorZu/extract_mables_from_conll.py "\
          "%(parse_res_path)s/parsed.conll > "\
          "%(parse_res_path)s/markables.txt && "\
          "python %(parse_path)s/CorZu/corzu.py "\
          "%(parse_res_path)s/markables.txt "\
          "%(parse_res_path)s/parsed.conll > "\
          "%(parse_res_path)s/coref.conll "\
          "&& python %(parse_path)s/CorZu/conll_to_html.py "\
          "%(parse_res_path)s/coref.conll > "\
          "%(parse_res_path)s/coref.html" % {'type':input_type, 'filename': doc,'parse_path':config.PARSER_PATH, \
                                             'parse_res_path':config.PARSE_RESULTS_PATH}


    # call ParZu
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    
    # catch parsing errors from ParZu or CorZu
    if not os.path.isfile(config.PARSE_RESULTS_PATH+'/parsed.conll'):
        raise IOError('Sorry, CorZu failed. Coref.conll file does not exist. Try another document.')
    else:
        with open(config.PARSE_RESULTS_PATH+'/parsed.conll', "r") as infile:
            infile = infile.read()
            if len(infile)<1:
                raise IOError('Sorry, ParZu failed. No parsing results.')
        
    if not os.path.isfile(config.PARSE_RESULTS_PATH+'/coref.conll'):
        raise IOError('Sorry, CorZu failed. Coref.conll file does not exist. Try another document.')
    
    
    # open the parsing result file, split at sentence boarders 
    with open(config.PARSE_RESULTS_PATH+'/coref.conll', "r") as infile:
        infile = infile.read()
        sentences = infile.split('\n\n')[:-1]
     
    # if requested, save parsing results
    if save_in_dir != None:
        shutil.copy2(config.PARSE_RESULTS_PATH+'/coref.conll', save_in_dir)
        
    return sentences
    
    
def get_sentences_from_parsed_text(doc):
    """Return sentences of a document with already parsed text in CoNNL format"""
    
    # open file and split at sentence boarders    
    with open(doc,"r") as infile:
        infile = infile.read()
        sentences = infile.split('\n\n')[:-1]

    return sentences
    

def get_sentences(filename, is_parsed=True, save_in_dir=None):    
    """Get parsed sentences, whether pre-parsed or not"""
    
    if is_parsed:   
        sentences = get_sentences_from_parsed_text(filename)
    else:
        sentences = get_sentences_from_unparsed_text(filename, save_in_dir)
             
    return sentences

    
def get_sentence_token_information(sentences):
    """Return parsed as nested sentence-token-information list"""
    
    parsed_text = []
    
    for sent in sentences:
        parsed_sentence = []
    
        # split sentence into tokens 
        tokens = sent.split('\n')
        for token in tokens:
            
            # split token string into token information
            parsed_token = [t for t in token.split('\t')]
            parsed_sentence.append(parsed_token)
            
        parsed_text.append(parsed_sentence)
        
    return parsed_text
    
    
### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 
### Feature Extraction functions
### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~     

def get_main_pos(tokens):
    """Return main POS frequencies: adjectives, nouns, verbs, pronouns, punctuation, particles"""
    
    adjectives = [t for t in tokens if t.full_pos.startswith('ADJ')]
    nouns = [t for t in tokens if t.sim_pos.startswith('N')]
    verbs = [t for t in tokens if t.sim_pos.startswith('V')]
    
    pronouns =[t for t in tokens if (t.full_pos.startswith('P') 
                and not t.full_pos.startswith('PTK') 
                and t.full_pos.startswith not in ['PROAV', 'PWAV'])
                or t.full_pos == 'ART']
                
    interpunct =[t for t in tokens if t.full_pos.startswith('$')]
    particles = [t for t in tokens if t not in adjectives+nouns+verbs+pronouns+interpunct \
                 and t.full_pos not in ['TRUNC', 'CARD']]
    
    for t in adjectives:
        t.pos_color.append('Adjectives')
        
    for t in nouns:
        t.pos_color.append('Nouns')

    for t in  pronouns:
        t.pos_color.append('Pronouns')
        
    for t in interpunct:
        t.pos_color.append('Punctuation marks')
        
    for t in particles:
        t.pos_color.append('Particles')
        
    for t in verbs:
        t.pos_color.append('Verbs')
            
    return len(adjectives), len(nouns), len(verbs), len(pronouns), len(interpunct), len(particles)
    
    
def get_more_spec_pos(tokens):
    """Return frequencies for more specific POS"""
    
    # adverbs and preps, particles
    adverbs = [t for t in tokens if t.full_pos == 'ADV']
    apprart = [t for t in tokens if t.full_pos == 'APPRART']
    postpos = [t for t in tokens if t.full_pos == 'APPO']
    circum_pos = [t for t in tokens if t.full_pos == 'APZR']
    compare_conj = [t for t in tokens if t.full_pos == 'KOKOM']
    
    # foreign words, interjections
    fremds = [t for t in tokens if t.full_pos == 'FM']
    interj = [t for t in tokens if t.full_pos == 'ITJ']
    
    # proper names and adjectives
    prop_name = [t for t in tokens if t.full_pos == 'NE']    
    adja = [t for t in tokens if t.full_pos.startswith('ADJA')]
    adjd = [t for t in tokens if t.full_pos.startswith('ADJA')]   
    
    # pronouns    
    dem_pro_s = [t for t in tokens if t.full_pos == 'PDS']
    dem_pro_a = [t for t in tokens if t.full_pos == 'PDAT']
    
    ind_pro_s = [t for t in tokens if t.full_pos == 'PIS']
    ind_pro_a = [t for t in tokens if t.full_pos in ['PIAT','PIDAT']]
    
    pers_pron = [t for t in tokens if t.full_pos == 'PPER']
    poss_s = [t for t in tokens if t.full_pos == 'PPOSS']
    poss_a = [t for t in tokens if t.full_pos == 'PPOSAT']
    
    refl_pron = [t for t in tokens if t.full_pos == 'PRF']
    inter_pron = [t for t in tokens if t.full_pos == ['PWS','PWAT','PWAV']]
    
    all_prons = dem_pro_s+dem_pro_a+ind_pro_s+ind_pro_a+poss_s+poss_a+refl_pron+inter_pron
    
    # compartives, punctuation    
    comp = [t for t in tokens if t.full_pos == 'TRUNC']    
    sent_int_interpunct = [t for t in tokens if t.full_pos == '$(']   
    
    # pronom adverbs and others
    pro_adv = [t for t in tokens if t.full_pos == 'PROAV' and t.function == 'pp']
    part_kvz = [t for t in tokens if t.full_pos == 'PTKVZ' and t.function == 'avz']    
    inf_with_zu = [t for t in tokens if t.full_pos == 'PTKVZ' and t.function == 'VVIZU']
    
    for t in poss_s+poss_a:
        t.pos_color.append('Poss pronouns')
        
    for t in refl_pron:
        t.pos_color.append('Refl pronouns')
    
    return (len(adverbs), len(apprart), len(postpos), len(circum_pos), len(fremds), len(interj), \
            len(prop_name), len(adja), len(adjd),
            len(dem_pro_s), len(dem_pro_a), len(dem_pro_s)+len(dem_pro_a), len(ind_pro_s), len(ind_pro_a), \
            len(ind_pro_s)+len(ind_pro_a),
            len(pers_pron), len(poss_s), len(poss_a), len(poss_s)+len(poss_a), len(refl_pron), \
            len(inter_pron), len(comp),
            len(sent_int_interpunct), len(pro_adv), len(part_kvz), len(compare_conj), \
            len(inf_with_zu), len(all_prons))


def get_cases(tokens):
    """Return case frequencies (counting by noun phrase heads)"""
    
    nom = [t for t in tokens if t.sim_pos in ['N','PRO'] and t.mo.casus == 'Nom']
    acc = [t for t in tokens if t.sim_pos in ['N','PRO'] and t.mo.casus == 'Acc' or t.function == 'obja']
    dat = [t for t in tokens if t.sim_pos in ['N','PRO'] and t.mo.casus == 'Dat' or t.function == 'objd']
    gen = [t for t in tokens if t.sim_pos in ['N','PRO'] and t.mo.casus == 'Gen' or t.function == 'objg']
    
    for t in nom:
        t.case_color.append('Nominative')
        
    for t in acc:
        t.case_color.append('Accusative')
        
    for t in dat:
        t.case_color.append('Dative')
    
    for t in gen:
        t.case_color.append('Genitive')
    
    return len(nom), len(acc), len(dat), len(gen)
    

def get_objects(tokens):
    """Return object frequencies"""
    
    acc_obj =  [t for t in tokens if t.function == 'obja']
    dat_obj =  [t for t in tokens if t.function == 'objd']
    gen_obj =  [t for t in tokens if t.function == 'objg']
    prep_obj = [t for t in tokens if t.function == 'objp']
    
    for t in acc_obj:
        t.object_color.append('Accusative objects')
        
    for t in dat_obj:
        t.object_color.append('Dative objects')
        
    for t in gen_obj:
        t.object_color.append('Genitive objects')
    
    for t in prep_obj:
        dep = [k for k in tokens if k.dependency== t.position and k.function == 'pn']
        
        for d in dep:
            d.object_color.append('Prepositional objects')
    
    return len(acc_obj), len(dat_obj), len(gen_obj), len(prep_obj), len(acc_obj)+len(dat_obj), len(gen_obj)+len(prep_obj)
    
    
def brauchen_lassen(tokens):
    """Return frequencies for constructions with 'brauchen' and 'lassen', and color them """
    
    # pre-filtering
    brauchen =  [(k,j) for (k,j) in itertools.product(tokens, tokens) if k.lemma == 'brauchen' \
                 and k.full_pos == 'VVFIN' and j.full_pos == 'VVINF' and j.function == 'obji' \
                 and j.dependency == k.position ]

    # actual construction
    full_brauchen = [(k,j) for ((k,j),i) in itertools.product(brauchen, tokens) if i.lemma == 'zu' \
                     and i.full_pos == 'PTKZU' and i.dependency == j.position]
    
        
    # pre-filtering
    lassen =  [(k,j) for (k,j) in itertools.product(tokens, tokens) if k.lemma == 'lassen' and k.full_pos == 'VVFIN' \
               and j.full_pos == 'VVINF' and j.function == 'obji' and j.dependency == k.position ]

    # actual construction
    full_lassen = [(k,j) for ((k,j),i) in itertools.product(lassen, tokens) if i.full_pos == 'PRF' \
                   and i.function == 'obja' and i.dependency == j.position]
    
    # coloring
    for k,j in full_brauchen:
        k.pattern_color.append('Brauchen constructions')
        
    for k,j in full_lassen:
        k.pattern_color.append('Lassen constructions')
        
    return len(full_brauchen), len(full_lassen), len(full_brauchen)+len(full_lassen)
      
    
def get_passive_voice(tokens, sent):
    """Identify, color and count passive voice (with and without agens)"""
    
    passive_w_agens = 0
    passive_count = 0
    
    # get predicates
    preds = sent.predicate()
    
    # get preds that involve passive
    preds = [t for t in preds if (t.lemma.startswith('werden') and t.mo.mod.lower() != 'subj' \
                                  and (t.function == 'root' or t.function == 'neb'))]
    
    for pred in preds:
        
        # get particple (action verb)
        participle =  sent.pass_verb(pred.position)
        
        # if participle is found
        if participle:
            
#            # get subj (logical object)
#            subj = next(t for t in sent.subj() if (t.dependency == pred.position))
                     
            # find agens
            agens = sent.agens(participle)
            
            # increase counter and color agens
            if agens:
                agens.passive_color.append('Passive agens')
                passive_w_agens += 1
                
            passive_count += 1
            pred.passive_color.append('Passive')
            participle.passive_color.append('Passive')
        
    return passive_count, passive_w_agens
        

def get_conjunctions(tokens):    
    """Identify, color and count conjunctions that connect to main clauses"""

    # identify conjunctions
    conj = [t for t in tokens if t.lemma in ['und','aber','sondern','denn','oder','doch', 'sowie'] and \
            t.full_pos == 'KON' and t.function == 'kon' and
          len([k for k in tokens if (k.dependency == t.position) and (k.full_pos.endswith('FIN') or \
                                                                      k.full_pos.endswith('PP')) and k.function == 'cj'])> 0 and
          len([k for k in tokens if (k.position == t.dependency) and (k.full_pos.endswith('FIN') or \
                                                                      k.full_pos.endswith('PP'))])> 0]
         
    # color conjunctions
    for t in conj:
        t.clause_color.append('Conjunctions')
        t.pattern_color.append('Conjunctions')
        
    return len(conj)


def get_participial_constructions(tokens):
    """Identify, color and count participial constructions"""
    
    # get part pres and praets
    part_pres = [t for t in tokens if t.full_pos == 'ADJD' and t.mo.part == '<PPRES' and t.function in  ['root','pn']]
    part_praet = [t for t in tokens if t.full_pos == 'VVPP' and t.function == 'neb']
    
    # for each participle
    for part in part_pres+part_praet:
        
        # get full participle construction
        part_con = easy_parse.get_dependent_tokens(tokens, part) + [part]
        part_con = easy_parse.get_all_tokens(part_con, tokens)
        
        # set initial comma positions
        first_comma_position = None
        sec_comma_position = None
        
        # find comma positions
        for comma in [t for t in part_con if t.lemma == ',']:
            if comma.position < part.position:
                first_comma_position = comma.position
            if comma.position > part.position:
                sec_comma_position = comma.position
    
        # cut participle construction at commas (only in-between)
        part_con = [k for k in part_con 
                    if (first_comma_position == None or first_comma_position < k.position) 
                    and (sec_comma_position == None or sec_comma_position > k.position)]

        # color
        for token in part_con:
            token.clause_color.append('Participial constructions')
            token.pattern_color.append('Participial constructions')
        
    # return counts
    return len(part_pres), len(part_praet), len(part_pres)+len(part_praet)


def get_rel_clauses(tokens):
    """Identify, color and count relative clauses"""
    
    rel_count = 0
    
    # get rel pronouns
    rel_prons = [t for t in tokens if t.full_pos in ['PRELS', 'PRELAT']]
    
    # get rel clauses
    rel_clauses = [(k,j) for (k,j) in itertools.product(rel_prons, tokens)     
                    if j.function in ['rel','cj', 'objc']
                    and j.full_pos.endswith('FIN') and j.position > k.position]
        
    # color relative clause tokens
    for (rel_pron, rel_pred) in rel_clauses:
        for token in tokens:
            if token.position >= rel_pron.position and token.position <= rel_pred.position:                
                token.clause_color.append('Relative clauses')      
                token.pattern_color.append( 'Relative clauses')
                
        rel_count +=1
        
    return rel_count
    

def get_subjunctive_forms(tokens, sent):
    """Identify, color and count subjunctives (Konjunktiv I and II)"""
    
    # subjunctive forms
    konj_1 = sent.konj_1()
    konj_2 = sent.konj_2()
    
    konjs = [k for k in konj_1+konj_2]
    
    konj_2_aux = [k for k in konj_1 if k.lemma in ['haben','sein','werden']]
    
    # indirect speech
    ind_speech = [(k,j) for (k,j) in itertools.product(tokens, konjs) 
                    if k.lemma in verbs_of_talking 
                    and k.function == 'root' 
                    and k.position == j.dependency]
                  
    # color indirect speech
    for k,j in ind_speech:
#        k.color.append('speak')
        j.pattern_color.append('Indirect speech')
                
    # irrealis 
    irrealis = [(k,j) for (k,j) in itertools.permutations(konjs,2)
                    if k.function == 'root' 
                    and j.function in ['neb','objc'] 
                    and j.dependency == k.position]  
                    
    # color irrealis            
    for k,j in irrealis:
        k.pattern_color.append('Irrealis')
        j.pattern_color.append('Irrealis')
            
    # counts
    ind_speech_count = len(ind_speech)
    irrealis_count  = len(irrealis)
    konj_1_count = len([k for k in konj_1])
    konj_2_count = len([k for k in konj_2 if k.lemma not in ['haben','sein','werden']])
    konj_aux_count = len(konj_2_aux)
    all_konj = konj_1_count+konj_2_count+konj_aux_count
    
    for t in konj_1:
        t.mode_color.append('Subjunctive 1')
    
    for t in konj_2+konj_2_aux:
        t.mode_color.append('Subjunctive 2')

    
    return konj_1_count, konj_2_count, konj_aux_count, ind_speech_count, irrealis_count, all_konj


def get_tempora(tokens):
    """Identify, color and count various tempora"""
     
    # pres, praet and participle forms
    pres =  [t for t in tokens if t.sim_pos == 'V' and t.mo.temp == 'Pres' and t.mo.mod != 'Subj' and t.lemma != 'werden']
    praet = [t for t in tokens if t.sim_pos == 'V' and t.mo.temp == 'Past' and t.mo.mod != 'Subj' and t.lemma != 'werden']
    
    praet_aux = [t for t in praet if t.lemma in ['sein', 'haben']]
    
    participle = [t for t in tokens if t.full_pos.endswith('PP') and t.function == 'aux']
    
    # perfect and plusquamperfect
    perf = [(k,j) for (k,j) in itertools.product(pres, participle) if k.position == j.dependency]
    pqp  = [(k,j) for (k,j) in itertools.product(praet, participle) if k.position == j.dependency]
    
    
    pres_werden = [t for t in tokens if t.sim_pos == 'V' and t.mo.temp == 'Pres' \
                   and t.mo.mod != 'Subj' and t.lemma == 'werden']
    futur_1 = [(k,j) for (k,j) in itertools.product(pres_werden, tokens) if  j.full_pos == 'VVINF' \
               and j.function == 'aux' and j.dependency == k.position]
    
    futur_2 = [(k,j) for (k,j) in itertools.product(pres_werden, tokens)
                                    if  j.full_pos == 'VAINF' and j.function == 'aux' and j.dependency == k.position]
                                        
    full_futur_2 = [(k,i) for ((k,j),i) in itertools.product(futur_2, tokens)  if i.full_pos == 'VVPP' 
                                         and i.function == 'aux' and i.dependency == j.position ]

    # coloring
    
    for t in pres:
        t.tempus_color.append('Present')
        
    for k in praet:
        k.tempus_color.append('Past simple')
    for k,j in perf:
        k.tempus_color.append('Perfect')
        j.tempus_color.append('Perfect') 
    for k,j in pqp:
        k.tempus_color.append('Plusquamperfect')     
        j.tempus_color.append('Plusquamperfect') 
        
    for k,j in futur_1+full_futur_2:
        k.tempus_color.append('Futur')
        j.tempus_color.append('Futur')

    # counts
    pres_count, praet_count, perf_count, \
    pqp_count, praet_aux_count, futur_1, futur_2 =  (len(pres), len([p for p in praet if p.lemma \
                                                                     not in ['haben','sein']]), len(perf), len(pqp), \
                                                     len(praet_aux), len(futur_1), len(full_futur_2) )
       
    all_perfects = perf_count+pqp_count
    all_futurs = futur_1 + futur_2
    return (pres_count - perf_count), (praet_count - pqp_count), perf_count, pqp_count, praet_aux_count, \
           futur_1, futur_2, all_perfects, all_futurs


def get_splittable_prefix(tokens):    
    """Identify, color and count verbs with splittable prefix"""
    
    # get splittable verb prefixes
    part_kvz = [t for t in tokens if t.full_pos == 'PTKVZ' and t.function == 'avz']
    
    # color
    for t in part_kvz:
        t.pos_color.append('Splittable prefix')
        
    return len(part_kvz)
    

def get_comparative_forms(tokens):
    """Identify, color and count comparatives and superlatives"""
    
    # find comp. forms of adjectives
    comparatives = [t for t in tokens if t.full_pos in ['ADJA', 'ADJD'] and t.mo.comp == 'Comp']
    superlatives = [t for t in tokens if t.full_pos in ['ADJA', 'ADJD'] and t.mo.comp == 'Sup' ]
   
    # color
    for t in comparatives:
        t.adj_color.append('Comparative adjectives')
    for t in superlatives:
        t.adj_color.append('Superlative adjectives')
        
    # count
    return len(comparatives), len(superlatives), len(comparatives)+len(superlatives)    


def get_genitives(tokens):
    """Identify, color and count genitive attributes and genitive objects"""
    
    # get genitives
    gen_mod = [t for t in tokens if t.sim_pos == 'N' and t.function == 'gmod']
    gen_obj = [t for t in tokens if t.sim_pos == 'N' and t.function == 'objg']   
    prep_with_gen = [t for t in tokens if t.sim_pos == 'N' and t.mo.casus == 'Gen' and t.function == 'pn']	
    prepositions = [p for (p,t) in itertools.product(tokens, prep_with_gen) if t.dependency == p.position \
                    and p.full_pos.startswith('APPR')]
    
    # color
    for t in gen_mod:#+gen_obj+prep_with_gen:
        t.pos_color.append('Genitive modifiers')
    for p in prepositions:#prep_with_gen:
        p.pos_color.append('Prepositions with genitive')
    
    return len(gen_mod), len(prep_with_gen), len(gen_mod)+len(prep_with_gen)+len(gen_obj)
        
        
def get_negations(tokens):
    """Identify, color and count negations (nicht)"""
    
    # get negations
    nicht = [t for t in tokens if t.full_pos == 'PTKNEG' and t.lemma == "nicht"]
    kein = []
#    kein =  [t for t in tokens if t.full_pos == 'PIAT' and t.lemma == 'kein']
    negations = nicht + kein
    
    # color
    for t in negations:        
        t.pattern_color.append('Negations')
        
    return len(negations)
        
def get_modal_verbs(tokens):
    """Identify, color and count modal verbs"""
    
    # get modals
    modals = [(k,j) for (k,j) in itertools.product(tokens, tokens) if k.position == j.dependency \
              and k.full_pos.startswith('VM') and j.full_pos == 'VVINF']
    
    # color
    for (k,j) in modals:
        k.pos_color.append('Modal verbs')
        
    return len(modals)
    
    
def get_aux_verbs(tokens):
    """Identify, color and count auxiliary verbs """
    
    aux_verbs = [k for k in tokens if k.full_pos.startswith('VA')]
    
    for t in aux_verbs:
        t.pos_color.append('Auxiliary verbs')
        
    
    return len(aux_verbs)
    
    
def get_full_verbs(tokens):
    """Identify, color and count full verbs """
    
    full_verbs = [k for k in tokens if k.full_pos.startswith('VV')]
    
    for t in full_verbs:
        t.pos_color.append('Full verbs')
    
    return len(full_verbs)

        
def get_questions(tokens):
    """Identify, color and count question words and marks"""
    
    # get question words
    question_words = [t for t in tokens if t.full_pos in ['PWAV','PWS']]
    
    # ?
    question_mark = True if tokens[-1].lemma == '?' else False
    
    # question marks
    if question_mark:
        tokens[-1].pattern_color.append('Questions')
    
    # color
    for t in question_words:
        t.pattern_color.append('Questions')
        
    return len(question_words), 1 if question_mark else 0

        
def get_imperatives(tokens):
    """Identify, color and count imparative forms"""
    
    imperatives = [t for t in tokens if t.full_pos.endswith('IMP')]
    
    for t in imperatives:
        t.mode_color.append('Imperatives')
        
    return len(imperatives)

def get_inversion(tokens):
    """Identify, color and count subject/predicate inversions"""
    
    # get preds 
    preds = [t for t in tokens if t.full_pos.startswith('V') and t.full_pos.endswith('FIN')]

    # get inversion candidates 
    inversion = [(k,j) for (k,j) in itertools.product(preds, tokens) if j.function == 'subj' 
                                                                    and j.dependency == k.position 
                                                                    and j.position > k.position ]
                                                                    
    # filter out "es" candidates                                                                
    not_inversion = [(k,j) for ((k,j),i) in itertools.product(inversion, tokens) if (i.lemma == 'es' \
                                                                                     and i.function == 'expl' \
                                                                                     and (i.dependency == k.position \
                                                                                          or easy_parse.get_dep_token(tokens, i).dependency == k.position))]
    final_inversion = [elem for elem in inversion if elem not in not_inversion]
                            
    # color                              
    for (k,j) in final_inversion:
        k.pattern_color.append('Inversions')
        j.pattern_color.append('Inversions')
        
    return len(final_inversion)
        
def get_subjunctions(tokens):
    """Identify, color and count subjunctions and subjunctional phrases"""
    
    # get conjunction candidates
    conjunctions = [t for t in tokens if t.full_pos == 'KOUS' and t.function == 'konj']
    
    # get conjunctions and preds
    conj_pred = [(k,j) for (k,j) in itertools.product(conjunctions, tokens) if j.full_pos.startswith('V') 
                                                                   and j.full_pos.endswith('FIN')
                                                                   and j.function in  ['root','neb'] 
                                                                   and j.position == k.dependency ]
    used_conjunctions = []
                                                                 
    for (k,j) in conj_pred:
        
        conj = k.word
    
        # color
        for t in tokens:
            if t.position >= k.position and t.position <= j.position:
                t.clause_color.append('Subjunctions')
                t.pattern_color.append('Subjunctions')
              
        # take care of multi word subjunction     
    
        # ... with "wenn"
        if k.word == 'wenn':
            
            # "wenn" as second word            
            prev_token =  easy_parse.get_prev_token(tokens, k)
            
            if prev_token.word in ['auch','ausser','sogar','selbst'] and prev_token.full_pos in ['ADV','APPR']:
                prev_token.clause_color.append('Subjunctions')
                prev_token.pattern_color.append('Subjunctions')
                conj = prev_token.word + ' ' + k.word
                
            # "wenn" as first first
            next_token = easy_parse.get_next_token(tokens, k)
            
            if next_token.word in ['auch'] and next_token.full_pos == 'ADV':
                next_token.clause_color.append('Subjunctions')
                next_token.pattern_color.append('Subjunctions')
                conj = k.word + ' ' + next_token.word
            
        # ... with "dass"
        if k.word == 'dass':
            prev_token =  easy_parse.get_prev_token(tokens, k)

            if prev_token.word in ['ohne', 'dadurch','kaum','so','als','ausser','außer','auf'] \
                    and prev_token.full_pos in ['ADV','APPR','PROAV','KOKOM']:
                prev_token.clause_color.append('Subjunctions')
                prev_token.pattern_color.append('Subjunctions')
                conj = prev_token.word + ' ' + k.word
            
        # ... with "ob"
        if k.word == 'ob':
            prev_token =  easy_parse.get_prev_token(tokens, k)
            if prev_token.word in ['als'] and prev_token.full_pos in ['KOKOM']:
                prev_token.clause_color.append('Subjunctions')
                prev_token.pattern_color.append('Subjunctions')
                conj = prev_token.word + ' ' + k.word
                
                
                
        used_conjunctions.append(conj)
         
    # increase count for subjunctional categories
    
    for word in used_conjunctions:
        
        if word in temporal:
            conj_dict['temporal']+=1
        elif word in conditional:
            conj_dict['conditional']+=1
        elif word in causal:
            conj_dict['causal']+=1
        elif word in concessive:
            conj_dict['concessive']+=1
        elif word in consecutive:
            conj_dict['consecutive']+=1
        elif word in final:
            conj_dict['final']+=1
        elif word in modal:
            conj_dict['modal']+=1           
        elif word in interrogative:
            conj_dict['interrogative']+=1      
        else:
            conj_dict['other']+=1

    return len(conj_pred), conj_dict
            

def get_platzhalter_ES(tokens):
    """Identify, color and count Platzhalter ES"""
    
    # get Platzhalter "es"
    es = [t for t in tokens if t.lemma == 'es' and t.function == 'expl']
    
    # color
    for e in es:
        e.pattern_color.append('Placeholder es')
        
    return len(es)
    
    
def get_coreferences(tokens):
    """Return number of coreferent entities and frequencies"""
    
    tokens = easy_parse.adjust_coref_new(tokens)
    
    corefs = [int(t.coref.strip(')')) for t in tokens if not  '_' in t.coref \
              and (t.full_pos.startswith('N') or t.full_pos=='PPER')]
    corefs_t = [t for t in tokens if not  '_' in t.coref and (t.full_pos.startswith('N') or t.full_pos=='PPER')]
    
    for k in corefs_t:
        k.coref_color.append('Discourse entities')
    
    if len(corefs) >0:
        max_cor = max(corefs)
    else:
        max_cor = 0
        
    return corefs, max_cor


def get_lix_score(n_sents, words):
    """Return LIX score"""
    
    n_words = len(words)
    long_words = len([w for w in words if len(w)>6])

    LIX = (n_words/n_sents) + ((long_words*100)/n_words)
    
    return LIX

### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 
### Collecting features, saving results
### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~     
    
    
def save_to_html_file(sents, file, all_features):    
        """Create HTML output with colored tokens according to syntactic features"""

        pos_f,case_f, object_f, tempus_f, mode_f, passive_f, pattern_f, adj_f, coref_f = all_features
                  
        # set beginning of HTML string
        html_string = '<head><meta charset="UTF-8"></head>'        
            
        # set beginning of legend string
        legend = '<b>Legend</b><br><br>'+'<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">'

        # make legend elements for selected features

        for feat in pos_f:  
                # set color settings according to syntactic feature
                icon = '<i class="material-icons" style="font-size:12px;border:2px solid '+color_dict[feat]+'; border-radius:5px;">equalizer</i>'
                # icon with color settings
                legend += icon+'   '+' '+feat+'<br>'
            
        legend += '<br>'
        
        for feat in case_f: 
            if feat!= '--None--':
                icon = '<i class="material-icons" style="font-size:12px;background-color:'+color_dict[feat]+';">equalizer</i>'
                legend += icon+'    '+' '+feat+'<br>'
            
        legend += '<br>'   
        
        for feat in object_f:  
            if feat!= '--None--':
                icon = '<i class="material-icons" style="font-size:12px;outline-style:double;outline-color:'+color_dict[feat]+';">equalizer</i>'
                legend += icon+'    '+feat+'<br>'   
        
        legend += '<br>'   
                
        for feat in mode_f:   
            if feat!= '--None--':
                icon = '<i class="material-icons" style="font-size:12px;outline-style: double;outline-color:'+color_dict[feat]+';">equalizer</i>'
                legend += icon+'    '+feat+'<br>'             
        
        legend += '<br>'   
                                             
        for feat in tempus_f:  
            if feat!= '--None--':
                icon = '<i class="material-icons" style="font-size:12px;background-color:'+color_dict[feat]+';">equalizer</i>'
                legend += icon+'    '+feat+'<br>' 
        
        legend += '<br>'   
         
        for feat in passive_f:   
            if feat!= '--None--':
                icon = '<i class="material-icons" style="font-size:12px;color:'+color_dict[feat]+';">equalizer</i>'
                legend += icon+'    <font style="font-weight:bold;">'+feat+'</font><br>'        
        
        legend += '<br>'   
                 
        for feat in pattern_f:
            if feat!= '--None--':
                icon = '<i class="material-icons" style="font-size:12px;color:'+color_dict[feat]+';">equalizer</i>'
                legend += icon+'   '+feat+'</font><br>'  #'  <font style="font-weight:bold;">'
        
        legend += '<br>'   
                         
        for feat in coref_f:  
            if feat!= '--None--':
                icon = '<i class="material-icons" style="font-size:12px; color:'+color_dict[feat]+';">equalizer</i>'
                legend += icon+'    <font style="font-variant:small-caps;">'+feat+'</font><br>'
        
        legend += '<br>'   
                         
        for feat in adj_f:     
            if feat!= '--None--':
                icon = '<i class="material-icons" style="font-size:12px; color:'+color_dict[feat]+';">equalizer</i>'
                legend += icon+'    <font style="font-style: italic;">'+feat+'</font><br>'
         
        legend += '<br><br><br>'                 
                  
        # for each sent and token
        for sent in sents:
            for token in sent:              

                # set html tags
                html_tags = []
                start_html = '<font style="'
                end_html =  '">'+token.word+'</font>'
                    
                # for each feature assigned to token, 
                # check if is selected in widgets
                # then, color the token accordingly
                
                for feat in token.pos_color:
                    if feat in pos_f:    
                        html_tags.append('border:2px solid '+color_dict[feat]+'; border-radius:5px;')
                        
                for feat in token.case_color:
                    if feat in case_f:
                        html_tags.append('background-color:'+color_dict[feat]+';')# opacity: 0.5; filter: alpha(opacity=50)')

                for feat in token.object_color:   
                    if feat in object_f:
                        html_tags.append('outline-style: double; outline-color:'+color_dict[feat]+';border-radius:5px')#00ff00)
        
                for feat in token.tempus_color:
                    if feat in tempus_f:
                        html_tags.append('background-color:'+color_dict[feat]+';')
                
                for feat in token.mode_color:
                    if feat in mode_f:                
                        html_tags.append('outline-style: double;outline-color:'+color_dict[feat]+';')

                for feat in token.coref_color:
                    if feat in coref_f:
                        html_tags.append('font-variant: small-caps; color:'+color_dict[feat]+';')
                    
                for feat in token.pattern_color:
                    if feat in pattern_f:
                        html_tags.append('color:'+color_dict[feat]+';')
                    
                for feat in token.adj_color:
                    if feat in adj_f:
                        html_tags.insert(0,'font-style: italic; color:'+color_dict[feat]+';')
                
                for feat in token.passive_color:
                    if feat in passive_f:
                        html_tags.append('font-weight: bold; color:'+color_dict[feat]+';')
                
                # if no color settings were needed, just use word    
                if len(html_tags)==0:
                    final_html = token.word
                    
                # put together start, end, and color tags
                else:
                    final_html = start_html+"".join(html_tags)+end_html
                       
                # append to final string
                html_string+=final_html

                # get prev and next token
                next_token = easy_parse.get_next_token(sent, token)
                
                # insert white space unless there is punctuation mark
                if ((not (token.position != len(sent)
                    and next_token.sim_pos.startswith('$')
                    and next_token.word != '('))  
                    and token.word != '('):  
                                            
                    html_string += ' '  
                    
        # open file
        with codecs.open(file,'w') as infile:
            infile.write(str(legend))
            infile.write(html_string)

def save_to_file(sent, file):
    """Save color-coded text to file"""
    
    # open file
    with codecs.open(file,'a') as infile:
        infile.write('<head><meta charset="UTF-8"></head>')
        
        # write out each token with color
        for token in sent:
            if token.color:
                html_token = '<font color="'+color_dict[token.color]+'">'+token.word+'</font>'
                infile.write(html_token)
            else:
                infile.write(token.word)                
                infile.write(' ')
            
        infile.write('')


def process_text(parsed_text, output_file='./outputs/feature_frequencies.csv', write_to_html=False):
    """Parse text, extract features, count and save them."""
    
    # initial counting states 
    # Ugly, I know, next time I'll use classes, I promise
    
    adjective_count = 0
    noun_count = 0
    verb_count = 0
    pronoun_count  = 0
    particle_count = 0    
    
    adverbs_count = 0
    apprart_count = 0
    postpos_count = 0
    circum_pos_count = 0
    fremds_count = 0 
    interj_count = 0
    
    adja_count = 0
    adjd_count = 0    
    
    prop_name_count = 0
    dem_pro_s_count = 0
    dem_pro_a_count = 0
    dem_pro_count = 0
    ind_pro_s_count = 0
    ind_pro_a_count = 0
    ind_pro_count = 0
    pers_pron_count = 0
    poss_s_count = 0
    poss_a_count = 0
    poss_count = 0
    refl_pron_count = 0
    inter_pron_count = 0
    
    all_prons_count = 0
    
    trunc_count = 0
    sent_int_interpunct_count = 0
    comp_conj_count = 0
    
    proadv_count = 0
    part_kvz_count = 0
    inf_with_zu_count = 0
    split_verbs_count = 0 
    
    modal_count = 0 
    aux_verbs_count = 0
    full_verbs_count = 0
    
    nom_count = 0
    acc_count = 0
    dat_count = 0
    gen_count = 0
    
    gen_mod_count = 0
    prep_with_gen_count = 0
    all_gens_count = 0
    
    acc_obj_count = 0
    dat_obj_count = 0
    gen_obj_count = 0
    prep_obj_count = 0
    
    acc_dat_obj_count = 0
    prep_gen_obj_count = 0
    
    present_count = 0 
    past_count = 0 
    perfect_count = 0 
    pqp_count = 0 
    all_perfect_count = 0
    praet_aux_count = 0
    futur_1_count = 0
    futur_2_count = 0
    all_futurs_count = 0
    
    konj_1_count = 0
    konj_2_count = 0
    konj_aux_count = 0
    ind_speech_count = 0
    irrealis_count = 0
    all_konjs_count = 0
    
    imperative_count = 0
    
    passive_count = 0 
    passive_w_agens = 0
    
    comp_count = 0
    sup_count = 0
    comp_sup_count = 0
    comp_conj_count = 0
        
    conjunctions = 0
    subjunctions = 0 
    rel_count = 0 
        
    part_pres_count = 0 
    part_praet_count = 0
    all_part_count = 0

    negation_count = 0 
    question_words_count = 0
    question_marks_count = 0 
    
    interpunction_count  =  0

    inversion_count = 0    
    es_count = 0
    brauchen_count = 0
    lassen_count = 0
    brauchen_lassen_count = 0
    
    # specific POS types    
    spec_pos_list = [adverbs_count, apprart_count, postpos_count, circum_pos_count, fremds_count, interj_count, \
                     adja_count, adjd_count,
                     prop_name_count, dem_pro_s_count, dem_pro_a_count, dem_pro_count, ind_pro_s_count, \
                     ind_pro_a_count, ind_pro_count,
                     pers_pron_count, poss_s_count, poss_a_count, poss_count, refl_pron_count, inter_pron_count, \
                     trunc_count, sent_int_interpunct_count, proadv_count,
                     part_kvz_count, comp_conj_count, inf_with_zu_count, all_prons_count]
        
    # names for features              
    feature_names = ["adjectives", "nouns", "verbs", "pronouns", "particles", "punctuation marks",
                   "poss pronouns", "refl pronouns",
                   "modal verbs", "aux verbs", "full verbs", "split verbs",
                   
                   "nominative", "accusative", "dative", "genitive", "gen modifiers", "prep with gen","all genitives", 
                   
                   "accusative obj", "dative obj", "genitive obj", "prepositional obj", "acc+dat obj","gen+prep obj",
                   
                   "present forms", "past forms", "perfect forms", "pqp forms", "perfect+pqp forms",
                   "past aux forms", "futur 1 forms", "futur 2 forms", "all futur forms",
                   "subj 1 forms", "subj 2 forms", "subj 2 aux forms", "ind speech", "irrealis mode", "all subj forms", 
                   "imperatives",
                   
                   "passive voice", "passive with agens", "comparative", "superlative","comp+superlative", 
                   
                   "conjunctions", "subjunctions", "relative clauses", "participial clauses pres",
                   "participial clauses past", "all participial clauses",
                  
                   "negations", "question words", "question marks", "subj/pred inversions", "placeholder 'es'", 
                   "'brauchen' constr", "'lassen' constr", "'brauchen'+'lassen' constr"]
                       
    
    # number of diff entities and their frequencies
    n_entities = []
    ent_freq = []    
    
    # sents, words and lemmas
    n_sents = len(parsed_text)
    n_words = 0
    all_words = []
    all_lemmas = []
           
    final_tokens = []
      
    # get features for each sentence      
    for sentence in parsed_text:          
        
            
        # transform tokens into Token class instances
        tokens = [easy_parse.Token(k) for k in sentence]
        sent = easy_parse.Sentence(tokens)
        
        # get words and lemmas, add them to all words and lemmas
        words = [t.word for t in tokens]    
        lemmas = [t.lemma for t in tokens]
                
        all_words += words
        all_lemmas += lemmas
        
        # get number of words
        n_words += len(words)
        
        # pos counts
        adjectives, nouns, verbs, pronouns, interpunct, particles = get_main_pos(tokens)     
        adjective_count += adjectives
        noun_count += nouns
        verb_count += verbs
        pronoun_count += pronouns
        particle_count += particles
        interpunction_count += interpunct 
        
        # spec pos counts
        spec_pos_results = get_more_spec_pos(tokens)

        # increase counts        
        for i, j in enumerate(spec_pos_results):
            spec_pos_list[i] += j      
            
            
        # get modals
        modal_count += get_modal_verbs(tokens)                    
        aux_verbs_count += get_aux_verbs(tokens)
        full_verbs_count += get_full_verbs(tokens)
            
        # get splittable verbs
        split_verbs_count += get_splittable_prefix(tokens)

        # get cases
        nom, acc, dat, gen = get_cases(tokens) 
        nom_count += nom
        acc_count += acc
        dat_count += dat
        gen_count += gen
                           
        # genitives
        gen_mod, prep_gen, all_gens =  get_genitives(tokens)
        gen_mod_count += gen_mod
        prep_with_gen_count += prep_gen
        all_gens_count += all_gens

        # get objects
        acc_obj, dat_obj, gen_obj, prep_obj, acc_dat_obj, gen_prep_obj = get_objects(tokens)
        acc_obj_count  += acc_obj
        dat_obj_count  += dat_obj
        gen_obj_count  += gen_obj
        prep_obj_count += prep_obj
        acc_dat_obj_count += acc_dat_obj
        prep_gen_obj_count += gen_prep_obj

        # get tempora
        present, past, perfect, pqp, all_perfects, praet_aux, futur_1, futur_2, all_futurs = get_tempora(tokens)
        present_count += present
        past_count += past
        perfect_count += perfect
        pqp_count += pqp
        all_perfect_count += all_perfects
        praet_aux_count += praet_aux
        futur_1_count += futur_1
        futur_2_count += futur_2
        all_futurs_count += all_futurs

        # get subjunctive mode   
        konj_1, konj_2, konj_aux, ind_speech, irrealis, all_konjs = get_subjunctive_forms(tokens, sent)
        konj_1_count += konj_1
        konj_2_count += konj_2
        konj_aux_count += konj_aux
        ind_speech_count += ind_speech
        irrealis_count += irrealis
        all_konjs_count += all_konjs
        imperative_count += get_imperatives(tokens)
        
        # passive        
        passive_count_new, passive_w_agens_new = get_passive_voice(tokens, sent)
        passive_count += passive_count_new
        passive_w_agens += passive_w_agens_new
        
        # get comp levels
        comp, sup, comp_sup = get_comparative_forms(tokens)
        comp_count += comp
        sup_count += sup
        comp_sup_count += comp_sup

        # con and subjunctions
        conjunctions += get_conjunctions(tokens)
        subjunctions_new, conj_dict =     get_subjunctions(tokens)
        subjunctions += subjunctions_new
        
        # rel clauses
        rel_count += get_rel_clauses(tokens)
        
        # participal constructions
        part_pres, part_praet, all_part = get_participial_constructions(tokens)
        part_pres_count += part_pres
        part_praet_count += part_praet
        all_part_count += all_part

        # negations
        negation_count += get_negations(tokens)
        
        # get questions
        question_words, marks = get_questions(tokens)
        question_words_count += question_words
        question_marks_count += marks
        
        # inversion
        inversion_count += get_inversion(tokens)
        
        # Platzhalter "es"
        es_count += get_platzhalter_ES(tokens)
        
        # get brauchen und lassen
        brauchen, lassen, brau_la = brauchen_lassen(tokens)
        brauchen_count += brauchen
        lassen_count += lassen
        brauchen_lassen_count += brau_la
        
        # get entities
        corefs,max_cor = get_coreferences(tokens)
        n_entities.append(max_cor)
        ent_freq.extend(corefs)
        
        #save_to_file(tokens, 'test.html')
        
        final_tokens.append(tokens)
        
        
    # get baseline features
    lix = get_lix_score(n_sents, all_words)        
    words_per_sent = len(all_words)/n_sents
    
    # vocabulary density
    vocabulary = [lemma for lemma in all_lemmas if lemma not in german_stopwords]
    voc_density = len(set(vocabulary))/len(vocabulary)
    
    # entity features
    n_entities = max(n_entities)+1
    avg_freqs = sum([ent_freq.count(p) for p in set(ent_freq)])/n_entities    
 
    # all frequency features            
    frequency_features =  [adjective_count, noun_count, verb_count, pronoun_count, particle_count, interpunction_count, 
                   poss_count, refl_pron_count, 
                   modal_count, aux_verbs_count, full_verbs_count, split_verbs_count,
                   nom_count, acc_count, dat_count, gen_count, gen_mod_count, prep_with_gen_count, all_gens_count, 
                   acc_obj_count, dat_obj_count, gen_obj_count, prep_obj_count, acc_dat_obj_count, prep_gen_obj_count,
                   present_count, past_count, perfect_count, pqp_count, all_perfect_count, 
                   praet_aux_count, futur_1_count, futur_2_count, all_futurs_count,
                   konj_1_count, konj_2_count, konj_aux_count, ind_speech_count, irrealis_count, all_konjs_count, 
                   imperative_count,
                   passive_count, passive_w_agens, comp_count, sup_count, comp_sup_count, conjunctions, subjunctions,
                   rel_count, part_pres_count, part_praet_count, all_part_count,
                   negation_count, question_words_count, question_marks_count, inversion_count, es_count,
                   brauchen_count, lassen_count, brauchen_lassen_count ]
                     
                         
    # check that features and feature names have same length
    assert (len(feature_names))  == (len(frequency_features))     
             
    # Combined level features
    
    a1_features = [question_words_count, question_marks_count, negation_count, split_verbs_count, poss_count, conjunctions, 
                   modal_count, imperative_count, praet_aux_count, perfect_count]

    a2_features = [comp_count, past_count, dat_obj_count, prep_obj_count, conj_dict['causal'], \
                   conj_dict['conditional'], conj_dict['consecutive'],
                  konj_aux_count, futur_1_count, gen_mod_count, refl_pron_count, adja_count]    
    
    b1_features = [gen_obj_count, conj_dict['consecutive'], conj_dict['interrogative'], conj_dict['concessive'],
                   conj_dict['temporal'], rel_count, passive_count, passive_w_agens]
                   
    # occurence of level features
    a1_features_bin =  sum([True for f in a1_features if f>0])
    a2_features_bin =  sum([True for f in a2_features if f>0])
    b1_features_bin =  sum([True for f in b1_features if f>0])
    all_features_bin = sum([True for f in frequency_features if f>0])
        
    # summing the level features
    a1_features_sum = sum([f/n_sents for f in a1_features])
    a2_features_sum = sum([f/n_sents for f in a2_features])
    b1_features_sum = sum([f/n_sents for f in b1_features])
    all_features_sum = sum([f/n_sents for f in frequency_features])
    
    
    # dictionary for level features and feature names
    combined_features = {'A1 features': a1_features_bin,
                         'A2 features': a2_features_bin,
                         'B1 features': b1_features_bin,
                      'level features (all)': all_features_bin,
                         
                         'A1 features summed': a1_features_sum,
                         'A2 features summed': a2_features_sum,
                         'B1 features summed': b1_features_sum,
                      'level features (all) summed': all_features_sum}
       
       
    # save information on colored tokens    
    with open('./outputs/colored_tokens', 'wb') as fp:
            pickle.dump(final_tokens, fp)                  

        
    with open('./outputs/color_dict', 'wb') as fp:
        pickle.dump(color_dict, fp)    

    # WRITE HTML FILE
        
    if write_to_html:
        save_to_html_file(final_tokens,'./outputs/colored_output.html', all_features)

    # WRITE ALL INTO AN OUTPUT FILE           

    # open file
    with codecs.open(output_file, 'w') as infile:
        
        # print head line
        stuff_to_print = 'Feature,Value\n'
        infile.write(stuff_to_print)
        
        # print baseline features and information about numbers of sentences and words
        infile.write('words per sent,'+str(words_per_sent)+'\n')
        infile.write('LIX,'+str(lix)+'\n')   
        infile.write('# words,'+str(len(all_words))+'\n')
        infile.write('# sents,'+str(n_sents)+'\n')
        
        # entity features and vocab density
        infile.write('discourse entities,'+str(n_entities/n_sents)+'\n')
        infile.write('avg entity frequency,'+str(avg_freqs)+'\n')
        infile.write('vocabulary density,'+str(voc_density)+'\n')

        # write frequency features to file
        for i,stat in enumerate(frequency_features):           
            
            stuff_to_print = feature_names[i]+','+str(stat/n_sents)+'\n'
            infile.write(stuff_to_print)
     
     
        # sort subordinating conjunctions dict alphabetically by key (to assure same order each time)
        conj_dict = sorted(conj_dict.items())
        
        # write subordinating conjunctions features to file
        for key, value in conj_dict:
            stuff_to_print = key+','+str(value/n_sents)+'\n'
            infile.write(stuff_to_print)
            
            
        # sort combined level feature dict alphabetically by key (to assure same order each time)
        combined_features = sorted(combined_features.items())
        
        # write combined level features to file
        for key, value in combined_features:
            
            stuff_to_print = key+','+str(value)+'\n'
            infile.write(stuff_to_print)

                   
    return color_dict, final_tokens     
    

### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 
### Main function with pipeline for extracting features
### ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ ~~~~~ 

def main():
    """Main function with pipeline for feature extraction"""

    # set filename
    filename = '../1_Text_collections/Language_Levels/B2/goethe_14.txt'

    # is it parsed?
    is_parsed = False
    
    # catch if file does not exist
    if not os.path.isfile(filename):        
        raise IOError('File %s does not exist'  % filename)
            
    # check if file is parsed
    with open(filename,'r') as infile:
        infile = infile.read()     
        if infile.startswith('1\t'):   
            is_parsed = True
     
 
    # get parsed sentences
    sentences = get_sentences(filename, is_parsed)    
    parsed_text = get_sentence_token_information(sentences)
    
    print(filename)
    # process text
    color_dict, sents = process_text(parsed_text, write_to_html=True)

    with open(r'./outputs/goethe_14_color_dict.pkl', 'wb') as output_file:
        pickle.dump(color_dict, output_file)

    with open(r'./outputs/goethe_14_colored_tokens.pkl', 'wb') as output_file:
        pickle.dump(sents, output_file)

# main function
if __name__ == '__main__':
    main()
