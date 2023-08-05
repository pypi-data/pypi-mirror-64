import pandas as pd
import pandass

class Characters():
    def capitalAlpha(self):
        return([chr(i) for i in range(65,91)])
    def smallAlpha(self):
        return([chr(i) for i in range(97,123)])
    def compAperators(self):
        comp_list=['==','<=','>=','!=','<','>']
        return(comp_list)
    def mathOperator(self):
        math_list=['+','-','*','/','=']
        return(math_list)
    def specialChars(self):
        char_list=["`",'~',"@",'#','$','%','^','&','*','-','_',';',':',"\ ",'|','/',',',"<",".",">","?","'",'"',"!",'+',' ']
        return(char_list)
    def tags(self):
        dic={'HV':'Helping verb','WP':'Wh-Pronoun','CD':'Cardinal number','PR':'Pronoun','IN':'Preposition','INV':'Negative word','INC':'Word enhancing sense of another word',
             'CC':'Conjunction','SYM':'Symbol','VB':'Verb base form','VBD':'Verb past form','VBN':'Verb past participle form','VBZ':'Verb s/es/ies/ form',
             'VBG':'Verb ing form','JJ':'Adjective','RB':'Adverb','Nn':'Noun','V':'Verb','NN':'Noun','IA':'Indefinite articles'}
        return(dic)
        
def sentTokenizer(paragraph):
    sentence_list=[]
    sentence=''
    title=0
    for letter in paragraph:
        if(letter.istitle()):
            title=1
        if(letter == ' '):
            title=0
        if(letter == '.'):
            if(title == 1):
                sentence+=letter
            else:
                sentence+=letter
                sentence_list.append(sentence)
                sentence=''
        elif(letter == '?'):
            sentence+=letter
            sentence_list.append(sentence)
            sentence=''
        else:
            if(letter == ' '):
                if(len(sentence) > 0):
                    sentence+=letter
            else:
                sentence+=letter

    if(len(sentence)>0):
        sentence_list.append(sentence)
    return(sentence_list)


def sortElements(dictionary):
    word_list=[]
    for i in dictionary:
        word_list.append((i,dictionary[i]))
    for i in range(len(word_list) - 1):
        for j in range(len(word_list) -1,i,-1):
            if(word_list[j-1][1] < word_list[j][1]):
                c=word_list[j-1]
                word_list[j-1]=word_list[j]
                word_list[j]=c
    return(word_list)

global __verbData__
global __sentiWords__

class Words():
    __callv__=0
    __callw__=0
    
    def stop_words(self):
        stop_words_list=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
            'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who',
            'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
            'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
            'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                         'than', 's', 't', 'can', 'will', 'just', 'don', 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren']
        return(stop_words_list)
    
    def invert_words(self):
        invert_words_list=['not','no','never','neither','nor','nobody','none','nothing',"don't","aren't","couldn't","didn't","doesn't",'couldn', 'didn', 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
            "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", ".weren't", "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        return(invert_words_list)

    def increase_words(self):
        increase_words_list=["very","extremely",'too','so',"real"]
        return(increase_words_list)
    
    def decrease_words(self):
        decrease_words_list=["quite",'rarely','seldom']
        return(decrease_words_list)

    def adverb_words(self):
        adverb_words_list=['adoringly','awkwardly','beautifully','brutally','carefully','cheerfully','grimly','lazily','loyally','really','ruthlessly','sloppily','stylishly','unevenly',
                           'rubato','eternity','gigahertz','thz','hypervelocity']
        return(adverb_words_list)
    
    def pronoun_words(self):
        pronoun_words_list=['i','me','we','us','you','he','she','it','her','him','they','them',
                            'that','this','that','these','those','anybody','anyone','anything','each',
                            'either','everybody','everyone','everything',
                            'one','someone','something','both','few','many','several','all',
                            'any','most','none','some','myself','ourselves','yourself','yourselves',
                            'himself','herself','itself','themselves','what','who','which','whom','whose',
                            'my','our','your','his','its','their','mine','ours','yours','his','hers','ours',
                            'yours','theirs','you','whatever']
        return(pronoun_words_list)

    def wh_pronouns(self):
        wh_pronoun_list=['who','whom','which','whose','whoever','whichever','whomever']
        return(wh_pronoun_list)
    
    def cardinal_numbers(self):
        num_list=['one','two','three','four','five','six','seven','eight','nine','zero']
        return(num_list)

    def prepositions(self):
        preposition_list=['in','into','up','on','at','since','for','down','behind','after','of','with','off','till','out','about','across','beside','besides','before','in front of',
                          'on account','among','between','in spite','in front','for the sake of','by means','according to','with reference','due to','by','to']
        return(preposition_list)
    def helping_verbs(self):
        helping_verb_list=['do','does','is','are','am','has','have','been','did','was','were','had','will','shall','be']
        return(helping_verb_list)

    __baseForm__ =[]
    __pastForm__ =[]
    __pastParticipleForm__ =[]
    __sEsIesForm__ =[]
    __ingForm__ =[]
    __polarity__ =[]
    
    def __verbs__(self):
        if(self.__callv__ == 0):
            global __verbData__
            __verbData__ =[]
            verb_file=open("verb_list.csv",'r')
            verb_file_data=verb_file.read()
            verb_file.close()
            data_lines=verb_file_data.split('\n')
            verb_file_data=[line.split(',') for line in data_lines[1:1001]]
            for line in verb_file_data:
                self.__baseForm__.append(line[0])
                self.__pastForm__.append(line[1])
                self.__pastParticipleForm__.append(line[2])
                self.__sEsIesForm__.append(line[3])
                self.__ingForm__.append(line[4])
                self.__polarity__.append(line[5])

            __verbData__ = {'base_form':self.__baseForm__ ,'pastForm':self.__pastForm__ ,'pastParticiple':self.__pastParticipleForm__ ,'s/es/iesForm':self.__sEsIesForm__ ,
                    'ingForm':self.__ingForm__ ,'polarity':self.__polarity__ }


    def __wordData__(self):
        global __sentiWords__
        word_file=pd.read_csv("words.csv",index_col=0)
        __sentiWords__ ={'posScore':word_file.PosScore ,'negScore':word_file.NegScore ,'pos':word_file.Pos}

    def conjunctions(self):
        con_word_list=['but','and','also','if','or','as well','either','while','so','because','than','still','yet','nevertheless','whereas','otherwise','else','therefore','as','although',
                       'though','wherever','where','where','untill','as soon','as long','else','for','not only','how','that','till','when','lest','unless']
        return(con_word_list)


def load():
    global __verbData__
    global __sentiWords__
    __verbData__ = pandass.__verbData__
    __sentiWords__ = pandass.__sentiWords__

def wordTokenizer(sentence):
    obj=Characters()
    symbols=obj.specialChars()
    capalpha=obj.capitalAlpha()
    small_alpha=obj.smallAlpha()
    token_list=[]
    s=''

    for letter in sentence:
        if((letter in capalpha) or (letter in small_alpha)):
            if((s.isnumeric()) or (s in symbols)):
               token_list.append(s)
               s=letter
            else:
               s+=letter
        elif(letter.isnumeric()):
            if((s == '') or (s.isnumeric())):
                s+= str(letter)
            else:
                token_list.append(s)
                s=str(letter)
        else:
            if(s == ''):
                s= str(letter)
            else:
                if((letter == "'") and (s[-1] == "n")):
                    s+=letter
                elif(letter == ' '):
                    token_list.append(s)
                    s=''
                elif(letter == '.'):
                    if(('mr' in s) or ('ms' in s)):
                        s+=letter
                    else:
                        token_list.append(s)
                        s= str(letter)
                else:
                    token_list.append(s)
                    s= str(letter)
    token_list.append(s)
    return(token_list)

'''
def load_data(key):
    f = Fernet(key)
    f1=open("words.py",'rb')
    f1_data=f1.read()
    de1=f.decrypt(f1_data)
    f1.close()
    f2 = open("words2.py",'rb')
    f2_data=f2.read()
    de2=f.decrypt(f2_data)
    f2.close()
    csvf1=open("words.csv","w",newline='')
    csvf1.write(de1.decode())
    csvf1.close()
    csvf2=open("verb_list.csv","w",newline='')
    csvf2.write(de2.decode())
    csvf2.close()
    obj=Words()
    obj.__verbs__()
    obj.__wordData__()
    os.remove("words.csv")
    os.remove("verb_list.csv")
'''
        
         
class FreqDist():
    def __init__(self,text):
        words=wordTokenizer(text)
        self.words_dict={}
        for word in words:
            if(word in self.words_dict):
                self.words_dict[word]+=1
            else:
                self.words_dict.update({word:1})
        self.dict_size=len(self.words_dict)
                         
    def most_common(self,num):
        sorted_list = sortElements(self.words_dict)
        return(sorted_list[:num])
    def least_common(self,num):
        sorted_list = sortElements(self.words_dict)
        length=len(sorted_list)
        return(sorted_list[length-num:length])

             
    

class Lemmatizer():

    def lemmatize(self,word):
        global __verbData__
        if(word in __verbData__['base_form']):
            return(word)
        elif(word in __verbData__['pastForm']):
            word_index=__verbData__['pastForm'].index(word)
            return(__verbData__['base_form'][word_index])
        elif(word in __verbData__['pastParticiple']):
            word_index=__verbData__['pastParticiple'].index(word)
            return(__verbData__['base_form'][word_index])
        elif(word in __verbData__['s/es/iesForm']):
            word_index=__verbData__['s/es/iesForm'].index(word)
            return(__verbData__['base_form'][word_index])
        elif(word in __verbData__['ingForm']):
            word_index=__verbData__['ingForm'].index(word)
            return(__verbData__['base_form'][word_index])
        else:
            return(-1)
def remove_stopwords(text):
    global __sentiWords__
    global __verbData__
    data2=__verbData__
    obj=Words()
    words_list=[]
    stop_words=obj.stop_words()
    tokens_list=wordTokenizer(text)
    pos_tags=__sentiWords__['pos']
    ps=__sentiWords__['posScore']
    ns=__sentiWords__['negScore']
    rb=0
    for token in tokens_list:
        if(rb == 0):
            if(token not in stop_words):
                if(token in pos_tags):
                    tag=pos_tags[token]
                    if(tag == "r"):
                        if((ps[token] + ns[token]) !=0):
                            words_list.append(token)
                            rb=1
                    else:
                        words_list.append(token)
                else:
                    words_list.append(token)
        else:
            if(token in stop_words):
                rb=0
            else:
                if(token in ps):
                    if((ps[token] +ns[token]) == 0):
                        rb=0
                    else:
                        rb=0
                        words_list.pop()
                        words_list.append(token)
                elif(Lemmatizer.lemmatize(token) != (-1)):
                    word_index=data2['base_form'].index(Lemmatizer.lemmatize(token))
                    if(data2['polarity'][word_index] == 0):
                        rb=0
                    else:
                        rb=0
                        words_list.pop()
                        words_list.append(token)
                else:
                    rb=0
                    words_list.append(token)
    return(words_list)

def remove_noise(words_list):
    words=["sr.","'un","st.","mr.","ms.","'em","d'oc","mt.","dr.","jr.","de'","d'or","oz.","jr's","b'av","e'en"]
    word_list=[]
    for word in words_list:
        if(len(word) >3):
            word_list.append(word)
        elif((len(word) == 3) and (word not in words)):
            word_list.append(word)
    return(word_list)

def remove_bitmap(words_list):
    obj=Characters()
    char_list = obj.specialChars()
    sa=obj.smallAlpha()
    ca=obj.capitalAlpha()
    word_list=[]
    for word in words_list:
        s=''
        for letter in word:
            if((letter.isnumeric()) or (letter in char_list) or (letter in ca) or (letter in sa)):
                s+=letter
        if(s != ''):
            word_list.append(s.casefold())
    return(word_list)
            

class PosTag():
    def __init__(self,words_list):
        global __verbData__
        global __sentiWords__
        self.tagged_words=[]
        words_length=len(words_list)
        obj=Words()
        char_obj=Characters()
        data=__sentiWords__
        data2=__verbData__
        pos_tags=data['pos']
        hv=obj.helping_verbs()
        wp=obj.wh_pronouns()
        pr=obj.pronoun_words()
        IN=obj.prepositions()
        inv=obj.invert_words()
        inc=obj.increase_words()
        dic=obj.decrease_words()
        cc=obj.conjunctions()
        cd=obj.cardinal_numbers()
        sym=char_obj.specialChars()
        lem_obj = Lemmatizer()
        i=0
        while(i < words_length):
            word=words_list[i]
            if((words_length -i) >=2):
                next_word=words_list[i+1]
                tagged_word=str(word) + " " + str(next_word)
                if(tagged_word in hv):
                    self.tagged_words.append((word,word,["HV"]))
                    self.tagged_words.append((next_word,next_word,["HV"]))
                    i+=2
                elif(tagged_word in inc):
                    self.tagged_words.append((word,word,["INC"]))
                    self.tagged_words.append((next_word,next_word,["INC"]))
                    i+=2
                elif(tagged_word in wp):
                    self.tagged_words.append((word,word,["WP"]))
                    self.tagged_words.append((next_word,next_word,["WP"]))
                    i+=2
                elif(tagged_word in pr):
                    self.tagged_words.append((word,word,["PR"]))
                    self.tagged_words.append((next_word,next_word,["PR"]))
                    i+=2
                elif(tagged_word in IN):
                    self.tagged_words.append((word,word,["IN"]))
                    self.tagged_words.append((next_word,next_word,["IN"]))
                    i+=2
                elif(tagged_word in inv):
                    self.tagged_words.append((word,word,["INV"]))
                    self.tagged_words.append((next_word,next_word,["INV"]))
                    i+=2
                elif(tagged_word in cc):
                    self.tagged_words.append((word,word,["CC"]))
                    self.tagged_words.append((next_word,next_word,["CC"]))
                    i+=2
                else:
                    if(word in hv):
                        self.tagged_words.append((word,word,["HV"]))
                        i+=1
                    elif(word in ['a','an','the']):
                        self.tagged_words.append((word,word,["IA"]))
                        i+=1 
                    elif(word in wp):
                        self.tagged_words.append((word,word,["WP"]))
                        i+=1
                    elif((word in cd) or (word.isnumeric())):
                        self.tagged_words.append((word,word,["CD"]))
                        i+=1
                    elif(word in pr):
                        self.tagged_words.append((word,word,["PR"]))
                        i+=1
                    elif(word in IN):
                        self.tagged_words.append((word,word,["IN"]))
                        i+=1
                    elif(word in inv):
                        self.tagged_words.append((word,word,["INV"]))
                        i+=1
                    elif(word in inc):
                        self.tagged_words.append((word,word,["INC"]))
                        i+=1
                    elif(word in cc):
                        self.tagged_words.append((word,word,["CC"]))
                        i+=1
                    elif(word in sym):
                        self.tagged_words.append((word,word,["SYM"]))
                        i+=1
                    elif(word in data2['base_form']):
                        self.tagged_words.append((word,word,["VB"]))
                        i+=1
                    elif(word in data2['pastForm']):
                        b_word=lem_obj.lemmatize(word)
                        self.tagged_words.append((word,b_word,["VBD"]))
                        i+=1
                    elif(word in data2['pastParticiple']):
                        b_word=lem_obj.lemmatize(word)
                        self.tagged_words.append((word,b_word,["VBN"]))
                        i+=1
                    elif(word in data2['s/es/iesForm']):
                        b_word=lem_obj.lemmatize(word)
                        self.tagged_words.append((word,b_word,["VBZ"]))
                        i+=1
                    elif(word in data2['ingForm']):
                        b_word=lem_obj.lemmatize(word)
                        self.tagged_words.append((word,b_word,["VBG"]))
                        i+=1
                        
                    elif(word in pos_tags):
                        i+=1
                        tag=pos_tags[word]
                        if(tag == 'a'):
                            self.tagged_words.append((word,word,["JJ"]))
                        elif(tag == 'r'):
                            self.tagged_words.append((word,word,["RB"]))
                        elif(tag == 'n'):
                            self.tagged_words.append((word,word,["Nn"]))
                        elif(tag == 'v'):
                            self.tagged_words.append((word,word,["V"]))
                        else:
                            self.tagged_words.append((word,word,["NN"]))
                    else:
                        self.tagged_words.append((word,word,["NN"]))
                        i+=1
            else:
                if(word in hv):
                    self.tagged_words.append((word,word,["HV"]))
                    i+=1
                elif(word in wp):
                    self.tagged_words.append((word,word,["WP"]))
                    i+=1
                elif((word in cd) or (word.isnumeric())):
                    self.tagged_words.append((word,word,["CD"]))
                    i+=1
                elif(word in pr):
                    self.tagged_words.append((word,word,["PR"]))
                    i+=1
                elif(word in IN):
                    self.tagged_words.append((word,word,["IN"]))
                    i+=1
                elif(word in inv):
                    self.tagged_words.append((word,word,["INV"]))
                    i+=1
                elif(word in inc):
                    self.tagged_words.append((word,word,["INC"]))
                    i+=1
                elif(word in cc):
                    self.tagged_words.append((word,word,["CC"]))
                    i+=1
                elif(word in sym):
                    self.tagged_words.append((word,word,["SYM"]))
                    i+=1
                elif(word in data2['base_form']):
                    self.tagged_words.append((word,word,["VB"]))
                    i+=1
                elif(word in data2['pastForm']):
                    b_word=lem_obj.lemmatize(word)
                    self.tagged_words.append((word,b_word,["VBD"]))
                    i+=1
                elif(word in data2['pastParticiple']):
                    b_word=lem_obj.lemmatize(word)
                    self.tagged_words.append((word,b_word,["VBN"]))
                    i+=1
                elif(word in data2['s/es/iesForm']):
                    b_word=lem_obj.lemmatize(word)
                    self.tagged_words.append((word,b_word,["VBZ"]))
                    i+=1
                elif(word in data2['ingForm']):
                    b_word=lem_obj.lemmatize(word)
                    self.tagged_words.append((word,b_word,["VBG"]))
                    i+=1
                elif(word in pos_tags):
                    i+=1
                    tag=pos_tags[word]
                    if(tag == 'a'):
                        self.tagged_words.append((word,word,["JJ"]))
                    elif(tag == 'r'):
                        self.tagged_words.append((word,word,["RB"]))
                    elif(tag == 'n'):
                        self.tagged_words.append((word,word,["Nn"]))
                    elif(tag == 'v'):
                        self.tagged_words.append((word,word,["V"]))
                    else:
                        self.tagged_words.append((word,word,["NN"]))
                else:
                    self.tagged_words.append((word,word,["NN"]))
                    i+=1
                '''
                elif(tagged_word in pos_tags):
                    i+=2
                    print(tagged_word , 3)
                    tag=pos_tags[tagged_word]
                    if(tag == 'a'):
                        self.tagged_words.append((word,word,["JJ"]))
                        self.tagged_words.append((next_word,next_word,["JJ"]))
                    elif(tag == 'r'):
                        self.tagged_words.append((word,word,["RB"]))
                        self.tagged_words.append((next_word,next_word,["RB"]))
                    elif(tag == 'n'):
                        self.tagged_words.append((word,word,["Nn"]))
                        self.tagged_words.append((next_word,next_word,["Nn"]))
                    elif(tag == 'v'):
                        self.tagged_words.append((word,word,["V"]))
                        self.tagged_words.append((next_word,next_word,["v"]))
                    else:
                        self.tagged_words.append((word,word,["NN"]))
                        self.tagged_words.append((next_word,next_word,["NN"]))
                '''

class Polarity():
    def fix_polarity(self,tagged_words_list):
        obj=Words()
        global __verbData__
        data=__sentiWords__
        data2=__verbData__
        base_form=data2['base_form']
        polarity=data2['polarity']
        pos_score=data['posScore']
        neg_score=data['negScore']
        for word in tagged_words_list:
            if((word[2][0] == 'JJ') or (word[2][0] == 'RB') or (word[2][0] == 'Nn') or (word[2][0] == 'V')):
                word[2].append(float(pos_score[word[0]]) + float(neg_score[word[0]]))
            elif('VB' in word[2][0]):
                word_index=base_form.index(word[1])
                word[2].append(float(polarity[word_index]))
            elif(word[2][0] == 'INC'):
                word[2].append(0.0)
                if(word[1] == "real"):
                    word[2].append(1.5)
                else:
                    word[2].append(1.3)
            else:
                word[2].append(0.0)
        return(tagged_words_list)

load()

                
class Sentiment():
    def __init__(self,text):
        wt_obj=wordTokenizer(text)
        data=remove_noise(wt_obj)
        data=remove_bitmap(data)
        pt_obj=PosTag(data)
        tagged_words=pt_obj.tagged_words
        
        pol_obj=Polarity()
        self.__wordList__ = pol_obj.fix_polarity(tagged_words)
        self.__polarity__ =0
        self.__count__=0

    def __analyzer__(self,sec_last,last_token,current_token):
        pol=0
        if(current_token == []):
            if(last_token == ()):
                #print(1)
                return(0)
            elif((last_token[2][0] == "RB") and (last_token[2][1] != 0)):
                if(sec_last == ()):
                    self.__count__ +=1
                    pol=last_token[2][1]
                    #print(2)
                    return(pol)
                else:
                    if(sec_last[2][0] == "INV"):
                        pol=(- last_token[2][1])/2
                        self.__count__ +=1
                        return(pol)
                    elif(sec_last[2][0] == "INC"):
                        pol=last_token[2][1]*sec_last[2][2]
                        self.__count__ +=1
                        return(pol)
                    elif(sec_last[2][0] == "DIC"):
                        pol=last_token[2][1]*0.7
                        self.__count__ +=1
                        return(pol)
                    else:
                        self.__count__ += 1
                        return(last_token[2][1])
            elif(last_token[2][0]=='INC'):
                if(sec_last == ()):
                    pol=0.2
                    self.__count__ +=1
                    return(pol)
                elif(sec_last[2][0] == 'INV'):
                    pol=-0.1
                    self.__count__ +=1
                    return(pol)
                elif(sec_last[2][0] == 'INC'):
                    pol=0.2 * sec_last[2][2]
                    self.__count__+=1
                    return(pol)
                else:
                    self.__count__ +=1
                    return(0.2)
            else:
                #print(3)
                return(0)
        else:
            ct=current_token[0]
            if(ct[2][1] == 0):
                #print(ct)
                if(last_token == ()):
                    #print(4)
                    return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                elif(last_token[2][0] == "RB"):
                    if(sec_last == ()):
                        pol=last_token[2][1]
                        if(pol != 0):
                            self.__count__ +=1
                        #print(5)
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    else:
                        if(sec_last[2][0] == "INV"):
                            pol=(-last_token[2][1])/2
                            if(pol == 0):
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                            else:
                                self.__count__ +=1
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        elif(sec_last[2][0] == "INC"):
                            pol=last_token[2][1]* sec_last[2][2]
                            if(pol > 1):
                                pol=1
                            if(pol == 0):
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                            else:
                                self.__count__ +=1
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        elif(sec_last[2][0] == "DIC"):
                            pol=last_token[2][1]*0.7
                            if(pol == 0):
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                            else:
                                self.__count__ +=1
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        else:
                            pol=last_token[2][1]
                            if(pol == 0):
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                            else:
                                self.__count__ +=1
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                elif(last_token[2][0] == 'INC'):
                    if(sec_last == ()):
                        pol=0.2
                        self.__count__ +=1
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    elif(sec_last[2][0]== 'INV'):
                        pol=-0.1
                        self.__count__ +=1
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    elif(sec_last[2][0]== 'INC'):
                        pol=0.2 * sec_last[2][2]
                        self.__count__ +=1
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    else:
                        pol=0.2
                        self.__count__ +=1
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                else:
                    return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
            else:
                if(last_token == ()):
                    if(ct[2][0] == "RB"):
                        #print(8)
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    else:
                        pol=ct[2][1]
                        self.__count__ +=1
                        #print(9)
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                elif(last_token[2][0] == "INV"):
                    if(ct[2][0] == "RB"):
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    else:
                        pol=(-ct[2][1])/2
                        self.__count__ +=1
                        #print(10)
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                elif(last_token[2][0] == "INC"):
                    if(sec_last == ()):
                        if(ct[2][0] == "RB"):
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        else:
                            pol=ct[2][1]* last_token[2][2]
                            if(pol > 1):
                                pol=1
                            self.__count__ +=1
                            #print(11)
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    elif(sec_last[2][0] == "INV"):
                        pol=(-ct[2][1])/(2 * last_token[2][2])
                        self.__count__ +=1
                        #print(12)
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    else:
                        if(ct[2][0] == 'RB'):
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        else:
                            pol=ct[2][1]* last_token[2][2]
                            if(pol > 1):
                                pol=1
                            self.__count__ +=1
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                elif(last_token[2][0] == "DIC"):
                    if(sec_last == ()):
                        if(ct[2][0] == "RB"):
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        else:
                            pol=ct[2][1]*0.7
                            self.__count__ +=1
                            #print(13)
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    elif(sec_last[2][0] == "INV"):
                        pol=(-ct[2][1])/1.4
                        self.__count__ +=1
                        #print(14)
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    else:
                        pol=ct[2][1]*0.7
                        self.__count__ +=1
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                elif(last_token[2][0] == "RB"):
                    if(sec_last == ()):
                        if(ct[2][0] == "RB"):
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        else:
                            pol=ct[2][1]
                            self.__count__ +=1
                            #print(16)
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    elif(sec_last[2][0] == "INV"):
                        pol= (-ct[2][1])/2
                        self.__count__ +=1
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    else:
                        if(ct[2][0] == "RB"):
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        else:
                            pol=ct[2][1]
                            self.__count__ +=1
                            #print(16)
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                else:
                    if(ct[2][0] == "RB"):
                        #print(15)
                        return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                    else:
                        if(sec_last !=()):
                            if((sec_last[2][0] == 'INV') and (last_token[2][1] == 0)):
                                pol=(- ct[2][1])/2
                                self.__count__ +=1
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                            else:
                                pol=ct[2][1]
                                self.__count__ +=1
                                return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        else:
                            pol=ct[2][1]
                            self.__count__ +=1
                            return(pol + self.__analyzer__(last_token,ct,current_token[1:]))
                        
                
                       
    def analyze(self):
        poll=self.__analyzer__((),(),self.__wordList__)
        #pol=self.__analyzer__((),(),text)
        self.__polarity__ =0
        if(self.__count__ !=0):
            #print(self.__count__ , pol)
            self.__polarity__=poll/ self.__count__
        self.__count__ = 0
        return(self.__polarity__)
    
    def isPositive(self):
        if(self.__polarity__ >0):
            return(bool(1))
        else:
            return(bool(0))
    def isNegative(self):
        if(self.__polarity__ < 0):
            return(bool(1))
        else:
            return(bool(0))
    def isNeutral(self):
        if(self.__polarity__ == 0):
            return(bool(1))
        else:
            return(bool(0))

MAX_POLARITY=1
MIN_POLARITY=-1
NEUTRAL_POLARITY=0
