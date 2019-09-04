# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:44:16 2017

@author: jsuter

Project: Language Level Analysis and Classification
Seminar "Educational Assessment for Language Technology" 
WS 2015/16, Magdalena Wolska

Julia Suter, January 2018

-----------------------------------------------------------------

parse_information.py

- classes for easy processing of ParZu and CorZu results
"""

# Import Statements
from operator import itemgetter

# --- Classes for Sentence and Token --- 

class Sentence(object):
    """Sentence Class for sentences parsed by ParZu.
    Offers many methods for returning syntatical functions of Sentence like subject, predicate or prepositional phrase
    """
    
    def __init__(self,data):
            self.data = data
    
    def subj(self):
        """Return (first) subject head of Sentence"""
        try:
            subj = [k for k in self.data if k.function == 'subj']
            return subj
        except StopIteration:
            return None 
            
    def predicate(self):
        """Return (first) predicate of Sentence"""
        try:
            # Predicate is finite verb
            pred = [k for k in self.data if k.full_pos.startswith('V') and k.full_pos.endswith('FIN')]
            return pred
    
        except StopIteration:
            return None 

    def agens(self, participle):
        """Return agens of Sentence"""
        pp_heads = [k for k in self.data if k.function == 'pn']
        for pn in pp_heads:
            for k in self.data:
                if (k.position == pn.dependency and (k.lemma == 'von') and (k.function == 'pp') \
                        and (k.dependency == participle.position)):
                    return pn


    def pass_verb(self,verb_pos):
        """Return passive verb (action verb) Sentence"""
        try:
            # The passive verb (action verb) is the past participle with function "aux" (or "cj")
            verb = next(k for k in self.data if ((k.function == 'aux' or k.function == 'cj') \
                                                 and (k.full_pos == 'VVPP') and (k.dependency == verb_pos)))
            return verb
        except StopIteration:
            return None
    
            
    def obj(self):
        """Return direct object's head of Sentence"""
        try:
            obj = [k for k in self.data if (k.function == 'objd' or k.function == 'obja')]
            return obj
        except StopIteration:
            return None   
        
    def genitive(self):
        """Return all genitive attributes of Sentence"""
        genitives = [k for k in self.data if (k.function() == 'gmod')]
        return genitives
        
    def prep_phrase(self):
        """Return all prepositiona phrases of Sentence"""
        prepositional_phrases = [k for k in self.data if k.function == 'pp']
        return prepositional_phrases
        
        
    def konj_1(self):
        """Return all konjunktiv I forms in Sentence"""
        konjunktiv_1 = [k for k in self.data if k.sim_pos.startswith('V') and k.mo.temp== 'Pres' \
                        and k.mo.mod.lower() == 'subj']
        return konjunktiv_1
        
    def konj_2(self):
        """Return all konjunktiv I forms in Sentence"""
        konjunktiv_2 = [k for k in self.data if k.sim_pos.startswith('V') and k.mo.temp == 'Past' \
                        and k.mo.mod.lower() == 'subj']
        return konjunktiv_2


class Token(object):
    """Token Class for representing Tokens in sentences parsed by ParZu.
    Offers many functions for returning linguistic information on token
    and changing it.
    """
    def __init__(self,token_data):    

            self.data = token_data
            self.position = int(token_data[0])
            self.word = token_data[1]
            self.lemma = token_data[2]
            self.sim_pos = token_data[3][0]
            self.sim_pos_full = token_data[3]
            self.full_pos = token_data[4]
            
            if self.full_pos == '_':
                self.full_pos = token_data[3]
                
            elif self.full_pos.endswith('IMP'):
                self.mo = Verb_Morphology('2|'+token_data[5]+'|_|_')     
            elif self.sim_pos.startswith('V'):
                self.mo =  Verb_Morphology(token_data[5])
            elif self.full_pos in ['ADJD', 'ADJA']:
                self.mo = Adj_Morphology(token_data[5])
            elif self.sim_pos_full == 'PRO':
                self.mo = Pro_Morphology(token_data[5])
            elif self.sim_pos == 'N':
                self.mo = Noun_Morphology(token_data[5])  
            else:
                self.mo = token_data[5]
                
            self.dependency = int(token_data[6])
            self.function = token_data[7].lower()
            self.coref = token_data[9]
                                  
            self.dependency = int(token_data[6])
            self.function = token_data[7].lower()
            self.coref = token_data[9]

            self.pos_color = [None]
            self.case_color = [None]
            self.object_color = [None]
            self.tempus_color = [None]
            self.mode_color = [None]
            self.pattern_color = [None]
            self.passive_color = [None]
            self.adj_color =  [None]
            self.coref_color = [None]
            self.clause_color = [None]
            

    def morph(self):
        """Return morphological information of Token in sentence.
        Depending on part-of-speech, morphology is safed in different class"""        
                
        if self.sim_pos == 'V':
            return Verb_Morphology(self.mo)

    def change_coref(self, new_coref):
        """Changes coreference index of Token to new_coref"""
        self.coref = new_coref
         

class Adj_Morphology(object):
     """Class for Morphology information for Adjectives as given by ParZu.
     Offers many methods for returning morphological information"""

     def __init__(self, morphdata):
        
        self.morphdata = morphdata    
        self.comp = '_' if self.morphdata == '_' else self.morphdata.split('|')[0]
        try:
            self.part = '_' if self.morphdata == '_' else self.morphdata.split('|')[1]        
        except IndexError:
            self.part = '_'
        
class Pro_Morphology(object):
    """Class for Morphology information for Pronouns as given by ParZu.
    Offers many methods for returning morphological information"""

    def __init__(self, morphdata):
            
        self.morphdata = morphdata   
        
        self.person = '_' if self.morphdata == '_' else self.morphdata.split('|')[0]
        self.numerus = '_' if self.morphdata == '_' else self.morphdata.split('|')[1]
        if len(self.morphdata.split('|'))>3:
            self.genus = '_' if self.morphdata == '_' else self.morphdata.split('|')[2]  
            self.casus = '_' if self.morphdata == '_' else self.morphdata.split('|')[3] 
        else:
            self.casus = '_' if self.morphdata == '_' else self.morphdata.split('|')[2]
    
class Noun_Morphology(object):
    """Class for Morphology information for Nouns as given by ParZu.
    Offers many methods for returning morphological information"""

    def __init__(self, morphdata):
            
            self.morphdata = morphdata
            self.genus = '_' if self.morphdata == '_' else self.morphdata.split('|')[0]  
            self.casus = '_' if self.morphdata == '_' else self.morphdata.split('|')[1]
            self.numerus = '_' if self.morphdata == '_' else self.morphdata.split('|')[2]
            self.person = 3
   
class Verb_Morphology(object):
    """Class for Morphology information for Verbs as given by ParZu.
    Offers many methods for returning morphological information"""

    def __init__(self,morphdata):
        
        # get morphological data
        self.morphdata = morphdata     
        self.person = (self.morphdata.split('|')[0])
        self.numerus = '_' if self.morphdata == '_' else self.morphdata.split('|')[1]
        self.temp = '_' if self.morphdata == '_' else self.morphdata.split('|')[2]
        try:
            self.mod = '_' if self.morphdata == '_' else self.morphdata.split('|')[3]
        except IndexError:
            self.mod = '_'
        

def adjust_passive(tokens):
    """If passive construction in sentence, change subject and agent to object and logical subject."""

    passive_found = False
    
    # transform tokens to Sentence class instance 
    sent = Sentence(tokens)
    
    # get predicates
    preds = sent.predicate()
    
    # get preds that involve passive
    preds = [t for t in preds if (t.lemma.startswith('werden') and t.morph().mod().lower() != 'subj' \
                                  and (t.function == 'root' or t.function == 'neb'))]

    for pred in preds:
        
        # get particple (action verb)
        participle =  sent.pass_verb(pred.position)
        # get subj (logical object)
        try:
            subj = next(t for t in sent.subj() if (t.dependency == pred.position))
        except AttributeError:
            continue
        except StopIteration:
            continue
        # get agent (logical subject)
        if participle == None:
            continue
        agens = sent.agens(participle)
        if agens == None:
            continue
        
        # change functions
        subj.change_function('obja')
        agens.change_function('subj')
        passive_found = True
        
    return passive_found

def coref_cleaning(t, new_coref_np, current_coref):
        """Assign the correct coreference tag according to
        Args:      t (token), new_coref_np (Boolean), current_coref (int)
        Return:   new_coref_np (Boolean), current_coref (int)
        """

        if t.coref.startswith('(') and t.coref.endswith(')'):
            current_coref = t.coref[1:-1]
            t.change_coref(current_coref)           
            new_coref_np = False

        # nested coref       
        elif t.coref.startswith('('):
            current_coref = t.coref[1:]  
            t.change_coref(current_coref)

            new_coref_np = True
            if t.full_pos == 'PRELS':
                new_coref_np = False

        # if value is - , get last found integer
        elif new_coref_np and t.coref.startswith('-'):
            t.change_coref(current_coref)
            
            if t.full_pos == 'PRELS':
                new_coref_np = False
           
        # end of nested coref 
        elif new_coref_np == True and t.coref.endswith(')'):

            current_coref = t.coref[:-1]  
            if t.sim_pos=='V':
                current_coref = '_'
            t.change_coref(current_coref)
            new_coref_np = False
           
        # no coref entity
        elif new_coref_np == False:
            t.change_coref('_')
            
        return (new_coref_np, current_coref)


def adjust_coref_new(tokens):
    """Adjust coref tags for easier processing (adpated version, July 2017 -- not relevant in this project)
    
    Args:       tokens (list of Tokens)
    Return:    tokens (list of Tokens)
    """    

    new_coref_np = False   
    current_coref = None
    
    # change coref value to integer between brackets     
    for t in tokens:

        if '|' in t.coref:            
            first_part = t.coref.split('|')[0]
            second_part = t.coref.split('|')[1]
            
            t.change_coref(first_part)          
            
            new_coref_np, current_coref = coref_cleaning(t,new_coref_np, current_coref)
        
            if second_part.startswith('('):    
                new_coref_np = True
                current_coref = second_part[1:]
                
        else:
            new_coref_np, current_coref = coref_cleaning(t,new_coref_np, current_coref)
        
        
    return tokens


def get_all_tokens(phrase, tokens):
    """ Return all tokens of a phrase
    
    Args:       phrase (list of Tokens), tokens (list of Tokens)
    Return:    new_phrase (list of Tokens)
    """    
    
    # positions of tokens in phrase
    positions = sorted([(t, t.position) for t in phrase], key=itemgetter(1))

    # get first and last token in phrase
    first_tok = positions[0][1]
    last_tok = positions[-1][1]
    
    # get full phrase
    new_phrase = [t for t in tokens if t.position >= first_tok and t.position <= last_tok]
    
    return new_phrase
    

def get_dependent_tokens(sent,head,already_processed = []):
    """ Return all words in sentence that are dependent on head
    
    Args:       sent (list), head (Token)
    Return:    dependent_tokens (list of Tokens)
    """

    for k in sent:
        dependent_tokens = [k for k in sent if (k.dependency == head.position) and k not in already_processed]
        # and k.lemma not in ['(',')','-]]

    if len(dependent_tokens)<1:
        return []
        
    #   for all dependent tokens, get their dependent tokens (recursion)
    else:
        for k in dependent_tokens:             
                new_dep_tokens = get_dependent_tokens(sent,k, dependent_tokens)
                dependent_tokens += new_dep_tokens
 
        return dependent_tokens


def get_prev_token(tokens, head):
    """ Return previous token
    Args:       tokens (list), head (Token)
    Return:    prev (Token)
    """
    
    try:
        prev = next(t for t in tokens if t.position == head.position-1)
    except StopIteration:
        return head
    return prev
    
def get_next_token(tokens, head):
    """ Return next token
    Args:       tokens (list), head (Token)
    Return:    next_t (Token)
    """
    
    try:
        next_t = next(t for t in tokens if t.position == head.position+1)
    except StopIteration:
        return head
    return next_t
    
def get_dep_token(tokens, head):
    """ Return dependent tokens
    Args:       tokens (list), head (Token)
    Return:    dep_tok (Tokens)
    """
 
    dep_tok = [t for t in tokens if t.position == head.dependency]
    if len(dep_tok)>0:
        return dep_tok[0]
    else:
        return head
