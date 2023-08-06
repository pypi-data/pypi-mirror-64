# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:37:34 2020

@author: jazzn
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:56:58 2020

@author: jazzn
"""

import sys
import random
import io
import base64


def alea(mmin,mmax,precision):
    p = 10**-precision
    return round(random.uniform(mmin/p,mmax/p))*p

def generate_xml(func,nb,cat=None,stype="random"):
    name = func.__name__
    cat = name if cat == None else cat
    questions = []
    if stype == "random":
        parameters = [random.randint(0,nb) for i in range(nb)]
    else:
        parameters = range(nb)
    for param in parameters:
        r = func(param)
        if r is not None:
            questions.append(func(param))
    file = open(name + ".xml","w",encoding="utf8")
    moodle_xml(name,questions,cloze_question,category = f'{cat}/', iostream = file)
    file.close()
    print("Questions were saved in " + name + ".xml, that can be imported into Moodle")
    
def num_q(x,p=0.001,sci = False):
    """Return formatted string for numerical question, that can be included into
    cloze type moodle question.
    x ... correct answer, p ... precision
    """
    if sci:
        return "{"+f"1:NUMERICAL:={x:e}:{p}#Pravilno~{x:e}:{10*p}#Premalo pravilnih decimalk"+"}"
    else:
        return "{"+f"1:NUMERICAL:={x}:{p}#Pravilno~{x}:{10*p}#Premalo pravilnih decimalk"+"}" 

def str_q(x):
    return "{1:SHORTANSWER:=%s}" %(x)

num_qr = lambda x,y=0.02:num_q(x,x*y)

def multi_q(answers):
    """Return formatted string for multichoice question, that can be included into
    cloze type moodle question.
    answers is a list of pairs (question, percent)
    """
    q  = "{1:MULTICHOICE:"
    for i in answers:
        q = q+"~%%%f%%%s\n" % (i[1],i[0])
    q = q+"}"
    return q

def multichoice_question(answers, name):
    """
    XML string for moodle multiple choice question.
    answers ... a list of pairs (answer,fraction),
              fraction tells how much percent is worth the answer 
    name ... name of the question
    """
    q  = """<question type="multichoice">
    <name>
      <text> %s </text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Odkljukaj pravilne izjave!<br></p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>false</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>abc</answernumbering>
    <correctfeedback format="html">
      <text>Odgovor je pravilen.</text>
    </correctfeedback>
    <partiallycorrectfeedback format="html">
      <text>Odgovor je delno pravilen.</text>
    </partiallycorrectfeedback>
    <incorrectfeedback format="html">
      <text>Odgovor je nepravilen.</text>
    </incorrectfeedback>
    <shownumcorrect/>""" %name
    for answer in answers:
        q = q + """
        <answer fraction="%f" format="html">
        <text><![CDATA[%s]]></text>
          <feedback format="html">
            <text></text>
          </feedback>
        </answer>
        """ % (answer[1],answer[0])
    q = q + "</question>"
    return q

def cloze_question(tekst, name, feedback=''):
    """
    XML string for moodle cloze question.
    tekst ... string with question in cloze format. (see
         https://docs.moodle.org/29/en/Embedded_Answers_(Cloze)_question_type )
    name ... name of the question
    """
    q = """
  <question type="cloze">
    <name>
        <text>%s</text>
    </name>
    <questiontext format="html">
        <text><![CDATA[%s]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text>%s</text>
    </generalfeedback>
    <penalty>0.2000000</penalty>
    <hidden>0</hidden>
  </question>
        """ % (name,tekst,feedback)
    return q

def moodle_xml(name, questions, template_fun, category = '',iostream=sys.stdout):
    """Write moodle xml file to be imported into Moodle.
    name ... name of the category, where the questions will be put
    questions ... list of strings containing xml code for the questions
    template_fun ... cloze_question or multichoice_question
    category ... optional upper category (default '')
    iostream ... file handle or other IOStream (default STDOUT)
    """
    iostream.write("""
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
<!-- question: 0  -->
  <question type="category">
    <category>
    <text>$course$/""" + category + name + """</text>

    </category>
  </question>
    """)
    for i in range(len(questions)):
        iostream.write(template_fun(questions[i], name+str(i)))
    iostream.write("</quiz>")
    
class Jokers:
    def __init__(self,var,nb,stype):
        assert len(stype)==len(var)*nb,f"incorrect lenght stype lenght -> {len(stype)} | vars -> {len(var)*nb}"
        assert ("0" in stype or "1" in stype),f"stype {stype} ne doit contenir que 0 ou 1"
        self.var = var
        self.nb = nb
        self.stype = stype
        listvar = []
        for v in var:
            for idx in range(1,nb+1):
                listvar.append(v+str(idx))
        self.list_var = listvar
        self.get_joker_dict()
    
    def get_joker_dict(self):
        self.dic_var = {v:int(s) for v,s in zip(self.list_var,list(self.stype))}
        return str(self.dic_var)
    
    def set_joker_value(self,var,func,*params):
        result = ""
        for v,typ in self.dic_var.items():
            if v[0] == var and typ == 0:
                r = func(*params)
                result += f"{v}={r}\n"
        return result

    def set_joker_alpha_value_by_list(self,var,lst):
        result = ""
        idx = 0
        for v,typ in self.dic_var.items():
            if v[0] == var and typ == 0:
                r = lst[idx]
                idx += 1
                result += f"""{v}='{r}'\n"""
        return result
    
    def set_joker_numeric_value_by_list(self,var,lst):
        result = ""
        idx = 0
        for v,typ in self.dic_var.items():
            if v[0] == var and typ == 0:
                r = lst[idx]
                idx += 1
                result += f"{v}={r}\n"
        return result
    
    def set_joker_short_response_by_list(self,var,lst):
        idx = 0
        result = ""
        for v,typ in self.dic_var.items():
            if v[0] == var and typ == 1:
                r = lst[idx]
                idx += 1
                result += f"{v}='{r}'\n"
                result += f"{v} = str_q({v})\n"
        return result
    
    def set_joker_numeric_response_by_function(self,var,func_exp,precision=0.01):
        def sfunc(f_exp,var):
            jokers = self.var.replace(var[0],"")
            new_f_exp = f_exp
            for j in list(jokers):
                new_f_exp = new_f_exp.replace('_'+j[0],j[0]+v[1])
            return new_f_exp
        result = ""
        for v,typ in self.dic_var.items():
            if v[0] == var and typ == 1:
                r = sfunc(func_exp,v)
                result += f"{v}={r}\n"
                result += f"{v} = num_qr({v},{precision})\n"
        return result
    
    def set_joker_numeric_response_by_list(self,var,lst,rtyp="num",precision=0.01):
        result = ""
        idx = 0
        for v,typ in self.dic_var.items():
            if v[0] == var and typ == 1:
                r = lst[idx]
                idx += 1
                result += f"{v}={r}\n"
                result += f"{v} = num_qr({v},{precision})\n"
        return result