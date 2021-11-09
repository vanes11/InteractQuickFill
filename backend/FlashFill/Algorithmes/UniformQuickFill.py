#from typing import final
from graphviz import *
from collections import *
from collections.abc import Iterable
import itertools
import sys
import csv
import re
import json
import copy
import os
from backend.settings import BASE_DIR

#Definition des varibale global
MesChemin = {} 
valit = 0 
StepResult = []


class Graph:

    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices
        # default dictionary to store graph
        self.graph = defaultdict(list) # edge set
        

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    '''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''
    def printAllPathsUtil(self, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            
            global MesChemin
            global valit
            valtest = []
            for elt in path:
                valtest.append(elt)
            MesChemin[valit] = valtest
            valit = valit + 1 
                
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if visited[i]== False:
                    self.printAllPathsUtil(i, d, visited, path)
                    
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False


    
    def printAllPaths(self, s, d):
        """  Prints all paths from 's' to 'd' """
        # Mark all the vertices as not visited
        visited =[False]*(self.V)

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path)
        

class UniformQuickFill:
    def __init__(self):
        self.BOTTOM = "⊥"
        self.ClasseC = {}
    
    def flatten(self,items):
        """ Converti unes liste de liste en liste simple """
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                for sub_x in self.flatten(x):
                    yield sub_x
            else:
                yield x



    def  GenerateStr3(self,entree, s):
        """ 
        cette fonction retourne  l'ensemble des facons d'obtenir s a partir de l'etat d'entree sigma
        elle retourne un dag, une structure de donnee qui permet de representer des grands ensembles
        elle utilse le principe de l'algorithme CYK, base sur la programmation dynamique, qui consiste a reconnaitre un mot
        dans un langage en passant  par sa table de transition.
        """
        EtaTilda = set() ; PsiTilda = set() 
        """ EtaSource = 0
        EtaTarget = len(s) """  
        W = {}    # table de transition, pour chaque arrete (i,j) associe l'etique qui est un ensemble d'expressions at0mique

        for i in range(len(s)+1):      
            EtaTilda = EtaTilda.union(set([i]))  # construction de l'ensemble des noeuds

        for i in range(len(s)+1):
            k = i+1
            for j in range(k,len(s)+1):
                PsiTilda = PsiTilda.union(set([(i,j)]))   # ensemble des aretes
                #PsiTilda = list(PsiTilda)
    
        for i in PsiTilda:                                # Pour chaque arete
            x = "ConstStr("+s[i[0]:i[1]]+")"                # s[i:j] =  SubStr(i,j), c'est pourquoi je concerve i[1] au lieu de i[1]-1
            ConstString = set([x])
            SubString = self.GenerateSubstring(entree,s[i[0]:i[1]])
            ConstString = ConstString.union(SubString) 
            
            W[i] = ConstString  


        baseformule = self.ExpressionConcatenate(entree,s)
        baseformule = baseformule[-1][0]



        if baseformule != [] :
            
            baseformule = "Concatenate(" + "˅".join(baseformule) + ")"
            W[(0,len(s))] =  W[(0,len(s))].union(set([baseformule]))
        
        EtaTilda = list(EtaTilda)
        
        return W,EtaTilda
    
    
    def  GenerateStr2(self,entree, s):
        """ 
        cette fonction retourne  l'ensemble des facons d'obtenir s a partir de l'etat d'entree sigma
        elle retourne un dag, une structure de donnee qui permet de representer des grands ensembles
        elle utilse le principe de l'algorithme CYK, base sur la programmation dynamique, qui consiste a reconnaitre un mot
        dans un langage en passant  par sa table de transition.
        """
        EtaTilda = set() ; PsiTilda = set() 
        """ EtaSource = 0
        EtaTarget = len(s) """  
        W = {}    # table de transition, pour chaque arrete (i,j) associe l'etique qui est un ensemble d'expressions at0mique

        for i in range(len(s)+1):      
            EtaTilda = EtaTilda.union(set([i]))  # construction de l'ensemble des noeuds

        for i in range(len(s)+1):
            k = i+1
            for j in range(k,len(s)+1):
                PsiTilda = PsiTilda.union(set([(i,j)]))   # ensemble des aretes
                #PsiTilda = list(PsiTilda)
    
        for i in PsiTilda:                                # Pour chaque arete
            x = "ConstStr("+s[i[0]:i[1]]+")"                # s[i:j] =  SubStr(i,j), c'est pourquoi je concerve i[1] au lieu de i[1]-1
            ConstString = set([x])
            SubString = self.GenerateSubstring(entree,s[i[0]:i[1]])
            ConstString = ConstString.union(SubString) 
            
            W[i] = ConstString  


        baseformule = self.ExpressionConcatenate(entree,s)
        baseformule = baseformule[-1][0]



        if baseformule != [] :
            
            baseformule = "Concatenate(" + "˅".join(baseformule) + ")"
            W[(0,len(s))] =  W[(0,len(s))].union(set([baseformule]))
        
        EtaTilda = list(EtaTilda)
        
        #print("ancien",len(W),"**********************************\n\n")
        W5 = self.GenerateLoop(entree,s,W)
        #print("resultat",len(W5),"**********************************\n\n")
        return W5 ,EtaTilda

    def LoopSet(self,TraceSet,k,Sigma,s):
        """ Cherche l'expression de boucle  loop qui retourne  qui permet d'extraire  s dans sigma """
        TraceSet = list(TraceSet)
        LoopSetResult = list()
        LoopResultAll = list()
        
        # nous cherchons une expression Loop, on peut en vouloir plusieurs.
    
        for TraceExpression in TraceSet:
            LoopResult = self.Loop(TraceExpression, k,Sigma)
            #LoopResultAll.append(LoopResult)  
            if LoopResult == s:
                Expression = "Loop("+TraceExpression+","+str(k)+","+str(Sigma)+")"
                LoopSetResult.append(Expression)
        
            if len(LoopSetResult) > 5:
                return LoopSetResult
        

        if len(LoopSetResult) >= 1 :
            return  LoopSetResult
        else:         
            return self.BOTTOM

    def ConcatenateLoop(self,StringList):
        """ Concatene une liste de string pris en arguments"""
        
        StringList = list(self.flatten(StringList))
        Result = ""
        for  elt in StringList:
            Result = Result + elt

        return Result

    def ExecuteSubstr2(self,elt,sigma,x):
        elt= elt.split(",",1)
        elt[0] = elt[0].replace("SubStr2(","")
        elt1 = elt[1].split(")",1)
        elt1 = elt1[0].replace("TokenSeq(","")
        elt1 = elt1.split(",")

        regexpression = ""

        
        for temp1 in elt1:
            regexpression = regexpression + self.ClasseC[temp1]

        TokenComp = re.compile(regexpression)
        Test = TokenComp.findall(sigma[elt[0]])

        if Test != None and  len(Test)>= x:
            return Test[x-1] 

        else:
            regexpression = regexpression + self.ClasseC[temp1]
            return self.BOTTOM
        
    def Loop(self,TraceExpression,k,Sigma):
        k = 1
        global StepResult
        StepResult = []
        
        t = self.ExecuteTraceExpression(TraceExpression,Sigma,k)
        while t != self.BOTTOM:
            StepResult.append(t)
            k = k +1
            t = self.ExecuteTraceExpression(TraceExpression,Sigma,k)

        return self.ConcatenateLoop(StepResult)

    def ExecuteTraceExpression(self,TraceExpression,s,x):
        """ Execute une expression concatenate(trace expression)sur une chaine et retoune le resultat(Sous chaine) obtenu """
        # x est la variable entiere qui nous sert de compteur de boucle dans LoopR dont k
        Result = []
        AtomiqueExpression =  TraceExpression.split("˅")
        AtomiqueExpression[0] = AtomiqueExpression[0].replace("Concatenate(","")
        b = list(AtomiqueExpression[-1])
        b[-1] = ""
        AtomiqueExpression[-1] = "".join(b)


        for elt in AtomiqueExpression:

            if elt.startswith("SubStr("):
                y = self.ExecuteSubStr(elt,s,x)
                Result.append(y)

            elif elt.startswith("SubStr2"):
                y = self.ExecuteSubstr2(elt,s,x)
            
                Result.append(y)

            elif elt.startswith("ConstStr"):
                y = self.ExecuteConstStr(elt,x)
                Result.append(y)

        
        if self.BOTTOM in Result:
            return self.BOTTOM
        else:
            return Result  
        
    def ListOfAllCancatenateExpression(self,EtaTilda , W):
        """ Fonction permettant de d'avoir la liste de touste les expression concatenate """
        
        EtaTilda = copy.deepcopy(EtaTilda)
        W = copy.deepcopy(W)
        ListeDesExpression = []
            
        if (0,len(EtaTilda)-1) in W.keys():
            baseformule1 = list(W[(0,len(EtaTilda)-1)])
            indice1  = [i for i in range(len(baseformule1)) if baseformule1[i].startswith('Concatenate')]
            
            if indice1!=[] :
                
                elt = baseformule1[indice1[0]]
                elt = elt.replace(" ", "")
                ListeDesExpression.append(elt)
                baseformule1.remove(baseformule1[indice1[0]])
                W[(0,len(EtaTilda)-1)] = set(baseformule1)
                
        g = Graph(len(EtaTilda))
        for elt in list(W.keys()):
            g.addEdge(elt[0], elt[1])
        
        s = EtaTilda[0]
        d = EtaTilda[-1]
        
        global MesChemin
        global valit
        MesChemin = {}
        valit = 0
        g.printAllPaths(s, d)
                      
        for ett in MesChemin:
            elt = MesChemin[ett]
            listedesformule = {}
            ToutesLesCombinaissons = []
        
            for i in range(len(elt)-1):
                listedesformule[i] = list(W[(elt[i],elt[i+1])])
        
            a = list(listedesformule.values())
            
            ToutesLesCombinaissons = list(itertools.product(*a))
            
            for temp1 in ToutesLesCombinaissons:
                temp1 = list(temp1)
                ConcatenateStringExpression = "Concatenate(" + "˅".join(temp1) + ")"
                ListeDesExpression.append(ConcatenateStringExpression)
                
        
        return ListeDesExpression
    
    def GetExamples(self):
        S =[]
        s = set()
        sigma = {}
        d = {}
        sortie = ""
        decoupe = []
        chemin = os.path.join(BASE_DIR, 'FlashFill/Algorithmes/data.txt')
        with open(chemin,"r", newline=None) as f:
            for line in f:
                line = line.replace("\n", "")
                decoupe = line.split("---")
                if len(decoupe)==1:
                    if decoupe[0]=="***":
                        S.append(s)
                        s = set()
                else:
                    example =  decoupe[0]
                    sortie  =  decoupe[1]
                    example =  example.split("+++")
                    for i in range(len(example)):
                        sigma["v"+str(i+1)]  = example[i]

                    x = (json.dumps(sigma),sortie) 
                    s = s.union(set([x]))
                    sigma = {}
        
        S.append(s)

        return S
    
    def GetClassC(self):
        """
        Defintion de la classe de token C,
        Il s'agit d'un dico dont les cles st les noms de tokens et
        les valeurs st les expressions regulieres correspondantes 
        """ # a present on a 23 tokens dans ClassC
        self.ClasseC = {}
        chemin = os.path.join(BASE_DIR, 'FlashFill/Algorithmes/classeC.csv')
        with open(chemin, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for token in csv_reader:
                self.ClasseC[token[0]] = token[1]
            self.ClasseC['SemiColonTok'] = ";"
            
        return self.ClasseC
    
    def Cpos(self,s,k):
        """ CPos est un constructeur de position, il permet de representer une  position de la gauche vers la droite et de la droite vers la droite """
        if(k>= 0):
            return k
        else:
            return len(s) + k
        
    def TokenSeq(self,*tokens):
        """ contruit une sequence(concatenation)d'expression regulieres """
        TokenSeqResult = ""
        for token in tokens:
            TokenSeqResult = TokenSeqResult+token
        return TokenSeqResult
    
    def Pos(self,s,r1,r2,c):
        """ 
            Retourne l'indice de debut de r2 dans  le cieme matching de l'expression reguliere 
            TokenSeq(r1,r2)
        """   
        r = self.TokenSeq(r1, r2)
        r1 = re.compile(r1) ; r2 = re.compile(r2); 
        r3 = re.compile(self.ClasseC['Epsilon'])
        
        if r1 != r3 and r2 != r3: 
            r = re.compile(r)
        elif r1 != r3:
            
            r  = r1
        elif r2 != r3:
            r = r2
        else:
            return self.BOTTOM  
        
        RegularExpression = r.findall(s) # retourne la liste des chaines qui match l'expression reguliere r dans s
        if len(RegularExpression) >= abs(c):
        
            e = abs(c)-1 # -1 car on veut recuperer le cieme element dans RegulaExpression dont l'element d'indice c-1 car le comptage commence a -1
            if c > 0:
                
                if r1 != r3 and r2 != r3:
                    res = re.search(re.escape(RegularExpression[e]),s) # Escape permet a l'expression reguliere de contenir les caracteres speciaux
                    t1 = res.group()
                    res1 = re.search(r1,t1) # on recupere  l'occurrence de r1 dans res                
                    Taille = res1.end() - res1.start() # taille de res1
                    t = res.start() + Taille  
                    
                    #print(c,s,t)
                        
                elif r1 != r3:
                    res = re.search(re.escape(RegularExpression[e]),s)
                    t =  res.end()-1
                
                    
                elif r2 != r3:
                    res = re.search(re.escape(RegularExpression[e]),s)
                    t = res.start() 
                    #print("r1 est  epsilon" , c,s,t)
                    
                    
            else:
                e = len(RegularExpression) + c  # comme c est negatif, on applique son cpos et on applique le meme principe precedent
                res = re.search(re.escape(RegularExpression[e]),s)
                t1 = res.group()
                if r1 != r3:
                    res1 = re.search(r1,t1) # on recupere  l'occurrence de r1 dans res
                else:
                    res1 = re.search(r2,t1) # on recupere  l'occurrence de r1 dans res
                res1 = re.search(r1,t1) # on recupere l'occurrence de r1 dans rest1
                Taille = res1.end() - res1.start()  # on recupere la taille
                t = res.start() + Taille
            
            

            return t
        else:
            return self.BOTTOM

    def GenerateRegularExpressionLeft(self,s,k):
        """ 
        Retourne l'ensemble des expressions regulieres qui existent dans  s[k1:k] 
        pour k1 variant de 0 a k-1
        """
        k1 = 0 #on commence la recherche en debut de chaine
        r1 = []
        Tokens = [] # liste des tokens dans la sous chaine s[k1:k]
        while  k1 <= k-1 :
            for cle in self.ClasseC:
                Token = self.ClasseC[cle]
                TokenComp = re.compile(Token)
                Test = TokenComp.match(s[k1:k])
                
                if Test != None:
                    k1 = k1 + Test.start()
                    Tokens.append((k1,Token,cle))# 0n stoke  le tuplet contenant l'indice de k1 du token en k1, la valeur du token associe et la cle(nom du token correspondant)
                    k1 =  k1 + Test.end()
                
                    break
        Taille = len(Tokens)
        i = 0
        while  i < Taille : # on construit les tokens correspondant a la sous chaine s[k1:k]
            Expression = "".join([str(elt[1]) for elt in Tokens[i: Taille]]) # ecriture de valeurs de tokens
            Expression2 = ",".join([str(elt[2]) for elt in Tokens[i: Taille]])# ecriture sur forme de cle separe par les virgules: Numtok, Hyphentok...
            r1.append((Tokens[i][0],Expression,Tokens[i: Taille],Expression2))
            # r1 est un liste de quatuplet(a,b,c,d): a represente k1, b l'expression reguliere associe, c la sous liste de Tokens correspondant.et d les tokens correspondant
            i = i +1
        return r1        
    
    def GenerateRegularExpressionRigth(self,s,k):
        
        """ Retourne l'ensemble des expressions regulieres qui existent dans  s[k:k2] 
        pour k2 variant de k a len(s) """ # meme principe que precedement
    
        k1 = k
        r1 = []
        Tokens = []
        Longueur = len(s)
        while  k1 < Longueur:
            for cle in self.ClasseC:  
                Token = self.ClasseC[cle]
                TokenComp = re.compile(Token)
                Test = TokenComp.match(s[k1:Longueur])
                
                if Test != None:
                    k1 = k1 + Test.end()-1 # on doit nomalement faire end()-1, mais pour respecter l'indexation de python on prend end()
                    Tokens.append((k1,Token,cle))
                    k1 = k1 + 1  #on avance pour continuer le parcours
                    break

        Taille = len(Tokens)
        #print(Tokens)
        i = 0
        while  i < Taille:
            Expression = "".join([str(elt[1]) for elt in Tokens[0: i+1]])
            Expression2 = ",".join([str(elt[2]) for elt in Tokens[0: i+1]])
            r1.append((Tokens[i][0],Expression,Tokens[0: i+1],Expression2))
            i = i +1
        return r1   

    def MatchExpression(self,l,s):
        """ 
        etant donnee une liste  l, cette fonction retourne l'indice(l'occurence) de s  dans l s'il trouve
        """
        try:
            return l.index(s) + 1 # +1 parceque l'indxation dans les liste commence a 0

        except ValueError:
            return 0

    def GetBestKey(self,s):
        """ prend une chaine(nondigitToc) et retoune le type(cle) de l'expression reguliere correspondante. """
        k1 = "NonAlphtok"
        k2 = "NonSpaceTok"
    
        keylist = list(self.ClasseC.keys())
        k1 = keylist.index(k1)
        k2 = keylist.index(k2)
    
        for i in range((k1+1),k2):
            Token = self.ClasseC[keylist[i]]
            
            TokenComp = re.compile(Token)
            Test = TokenComp.match(s)
            if Test != None:
                return keylist[i]
        
        return ''

    def ExpressionConcatenate(self,entree,s):
        """ retourne la formule concatenate(de SubStr2) et concatenate(de ConstStr) qui permet d'obtenir s a partir de entree """
        k1 = 0
        r1 = []
        Tokens = []
        ExpressionExecute = []
        ExpressionExecuteFormule = []
        P1 = []
        P2 = []
        booldoitcontinuer = False

        k=len(s)

        while  k1 < k :
            for cle in self.ClasseC:
                Token = self.ClasseC[cle]
                TokenComp = re.compile(Token)
                Test = TokenComp.match(s[k1:k]) # k = len(s)
                
                if Test != None:
                    k1 = k1 + Test.start()
                    if cle == 'NonDigitTok' :
                        bestkey = self.GetBestKey(Test.group())
                        if bestkey != '':
                            cle = bestkey
                            Token = self.ClasseC[cle]
                            
                    Tokens.append((k1,Token,cle,Test.group()))
                    k1 =  k1 + Test.end()
                    break
                
        for elt in Tokens:
            
            booleen = False
            
            for key in entree:
                
                elt = list(elt) # elt est un tuple, on le convertir en  liste
                chaine = elt[3]
                expression = elt[1]
                Tokenname = elt[2]
                TokenComp = re.compile(expression)
                Test = TokenComp.findall(entree[key]) # Test est une liste

                for p in range(len(Test)):

                    K = len(chaine)
                    res = [Test[p][i: j] for i in range(len(Test[p])) for j in range(i + 1, len(Test[p]) + 1) if len(Test[p][i:j]) == K]

                    if chaine in res:

                        if len(chaine) == len(Test[p]): 
                            result = (p,-2)
                            booleen = booleen or True
                        else:
                            if res[0] == chaine:
                                result = (p,0,len(chaine))
                                booleen = booleen or True
                            elif res[-1] == chaine:
                                result = (p,-1,len(chaine))
                                booleen = booleen or True
                            else:
                                booleen = booleen or False

                        break
                

                if booleen:
                    break
                else:
                    booleen = booleen or False
                    
            if booleen:
                ExpressionExecute.append((key,expression,result))
                ExpressionExecuteFormule.append("SubStr2(" + key + "," + "TokenSeq(" + Tokenname + ")," + str(list(result)[0]+1) + ")")
            else:
                if chaine == s:
                    booldoitcontinuer = True
                    break
                ExpressionExecute.append(chaine)
                ExpressionExecuteFormule.append("ConstStr(" + chaine + ")")                          
        
        if ExpressionExecuteFormule == []:
            booldoitcontinuer = True


        if booldoitcontinuer :
            k1 = 0
            r1 = []
            Tokens = []
            ExpressionExecute = []
            ExpressionExecuteFormule = []
            P1 = []
            P2 = []
            booldoitcontinuer = False

            k=len(s)
            
            while  k1 < k :
                for cle in self.ClasseC:
                    Token = self.ClasseC[cle]
                    TokenComp = re.compile(Token)
                    Test = TokenComp.match(s[k1:k1+1]) # k = len(s)
                    
                    if Test != None:
                        k1 = k1 + Test.start()
                        if cle == 'NonDigitTok' :
                            bestkey = self.GetBestKey(Test.group())
                            if bestkey != '':
                                cle = bestkey
                                Token = self.ClasseC[cle]
                                
                        Tokens.append((k1,Token,cle,Test.group()))
                        k1 =  k1 + Test.end()
                        break                              

            for elt in Tokens:
                
                booleen = False
                
                for key in entree:
                    
                    elt = list(elt) # elt est un tuple, on le convertir en  liste
                    chaine = elt[3]
                    expression = elt[1]
                    Tokenname = elt[2]
                    TokenComp = re.compile(expression)
                    Test = TokenComp.findall(entree[key]) # Test est une liste

                    for p in range(len(Test)):

                        K = len(chaine)
                        res = [Test[p][i: j] for i in range(len(Test[p])) for j in range(i + 1, len(Test[p]) + 1) if len(Test[p][i:j]) == K]

                        if chaine in res:

                            if len(chaine) == len(Test[p]): 
                                result = (p,-2)
                                booleen = booleen or True
                            else:
                                if res[0] == chaine:
                                    result = (p,0,len(chaine))
                                    booleen = booleen or True
                                elif res[-1] == chaine:
                                    result = (p,-1,len(chaine))
                                    booleen = booleen or True
                                else:
                                    booleen = booleen or False

                            break
                    

                    if booleen:
                        break
                    else:
                        booleen = booleen or False
                        
                if booleen:
                    ExpressionExecute.append((key,expression,result))
                    ExpressionExecuteFormule.append("SubStr2(" + key + "," + "TokenSeq(" + Tokenname + ")," + str(list(result)[0]+1) + ")")
                else:
                    if chaine == s:
                        booldoitcontinuer = True
                        break
                    ExpressionExecute.append(chaine)
                    ExpressionExecuteFormule.append("ConstStr(" + chaine + ")")
             
        P1.append(ExpressionExecute) # P1 est une liste de tuple
        P2.append(ExpressionExecuteFormule) # liste 'expression Substr2, ConstStr
           
        return [P1,P2]

    def ExpressionConcatenateOfStringSigma(self,entre):
        """ retourne l'expression reguliere qui match l'entree sigma, sigma etant un dic de chaine de caractere"""
        DiskExpression= {}

        for key in entre:
            s = entre[key]
            k1 = 0
            r1 = []
            Tokens = []
            ExpressionExecuteFormule = ""
            k=len(s)
        

            while  k1 <= k-1 :
                for cle in self.ClasseC:
                    Token = self.ClasseC[cle]
                    TokenComp = re.compile(Token)
                    Test = TokenComp.match(s[k1:k])
                    
                    if Test != None:
                        k1 = k1 + Test.start()
                        if cle == 'NonDigitTok' :
                            bestkey = self.GetBestKey(Test.group())
                            if bestkey != '':
                                cle = bestkey
                                Token = self.ClasseC[cle]
                        
                        Tokens.append((k1,Token,cle,Test.group()))
                        k1 =  k1 + Test.end()
                    
                        break

            

            for elt in Tokens:
                ExpressionExecuteFormule = ExpressionExecuteFormule + " " + list(elt)[2]

            DiskExpression[key] = ExpressionExecuteFormule
            
        
        
        return DiskExpression

    def GeneratePosition(self,s,k):
        
        """ retourne l'ensemble des differentes facons de representer une position
        donnee dans une chaine donnee avec les primitives du langage  """

        POsList = []  # variable de formatage 
        PosChain = ""
        result = set([self.Cpos(s,k), self.Cpos(s,-(len(s)-k))])
        PosChain = "Cpos("+s+","+str(k)+")"
        POsList.append(PosChain)
        PosChain = "Cpos("+s+",-"+str((len(s)-k))+")"
        POsList.append(PosChain)
        R1List = self.GenerateRegularExpressionLeft(s,k)  #  liste des expressions regulieres dans la chaine s[0:k-1]
        R2List = self.GenerateRegularExpressionRigth(s,k) # Liste des expressions regulieres dans la chaine s[k:len(s)]
        for r1 in R1List :
            for r2 in R2List :
                r12 = self.TokenSeq(r1[1],r2[1])
                r12 = re.compile(r12)
                MatchingList = r12.findall(s)# liste de toutes les occurrences de qui match r12 dans s
                c = self.MatchExpression(MatchingList,s[r1[0]:r2[0]+1])
                c1 = len(MatchingList)
                if c!=0 and (r1[2][len(r1[2])-1][1] != r2[2][0][1]): 
                    # cette deuxieme condition sur if nous permet d'exclure le ou la fin de r1 est  de meme type que le debut de r2, car ceci pret a confusion, on ne sait plus dean ce cas determiner l;indice de debut de r2
                    c1 = -(c1 -c +1)   # c1 nous permet de parcourir la chaine de la droite vers la gauche
                    PosChain = "Pos("+"TokenSeq("+r1[3]+"),TokenSeq("+r2[3]+"),"+str(c)+")"
                    POsList.append(PosChain) 
                    PosChain = "Pos("+"TokenSeq("+r1[3]+"),TokenSeq("+r2[3]+"),"+str(c1)+")"
                    POsList.append(PosChain)

                    result = result.union(set([self.Pos(s,r1[1],r2[1],c),self.Pos(s,r1[1],r2[1],c1)]))  # result n'est rien d'autres que que k

        return result,set(POsList)
    
    def SubStr(self,s,p1,p2):
        """ 
        Expression de sous chaine tel que formuler dans l'article, un peu != de celle de python.l'indexation commence a 0
        """
        # par la suite on utile la fonction substring de python a ajoutant a l'indice de fin
        p2 = p2+1
        return s[p1:p2]

    def SubStrs(self,s,p1,p2):
        """
        Retourne la liste de sous chaine de s pouvant etre former avec les elements de p1 et p2: p1 et p2 etant les ensembles de positions , 
        """
        SubList = []  # pour affichage
        SubChain = ""
        p1 = list(p1); p2 = list(p2)
        for i in p1:
            for j in  p2:
                #result = result.union(set([SubStr(s,i,j)])) # ce ci n'est pertinent que lorsque l'ensemble p1 tout comme p2
                # represente les valeurs diff, ce qui n'est pas le cas pour nous
                #SubChain = "SubStr("+s+","+str(i)+","+str(j)+")"
                SubChain = "SubStr("+s+","+i+","+j+")"# pour  le formatage, on laisse i et j pour avoir les expressions pos et cpos
                SubList.append(SubChain)
        
        return set(SubList)
    
    def GenerateSubstring(self,entree,s):
        """ 
        Pour un etat d'entree sigma et une sortir s, cette fonction retourne l'ensemble des expressions Substr() 
        de notre langage qui permette d'obtenir d'extraire la chaine s dans l'entree sigma.
        l'etat d'entree sigma est un dictionnaire : les cle sont  vi et les valeurs sont des chaine de caracteres.
        ---------
        Ce qui nous interesse c'est l'affichage avec les expression pos et cpos, car la valeur est unique.
        """
        result = set()
        
        for cle in entree:
            # cle = vi, nom de colonne
            if s in entree[cle]:     
                k = entree[cle].index(s)         
                k1 = len(s)+k-1
                Y1 = self.GeneratePosition(entree[cle],k) # Y1 est un tuple car GeneratePosition retourne un tuple
                Y1 = Y1[1]  # ensemble de facons de retourner l'indince de debut de s sans entree
                Y1 = list(Y1)
                for i in range(len(Y1)):

                    Y1[i] = Y1[i].replace(entree[cle],cle,10)


                Y2 = self.GeneratePosition(entree[cle], k1)
                Y2 = Y2[1]
                Y2 = list(Y2)
                for i in range(len(Y2)):
                    Y2[i] = Y2[i].replace(entree[cle],cle,10)
                    

                SubResult = self.SubStrs(cle,Y1,Y2) # le resultat de Substrs est deja un set            
                result = result.union(SubResult) 
                    
                
        return result

    def ExecuteConstStr(self,s,x):

        s = s.replace("ConstStr(","")
        s = s.replace(")","")
        if x > 1:
            return self.BOTTOM
        else:
            return s
        
    def ExecuteSubStr(self,elt,sigma,x):
        s11=[]
        s1 = elt.split(",",1)
        s1[0] = s1[0].replace("SubStr(","")  
        p1=[]
        p11=[]
        p2=[]
        regexpression = ""
        # split SubStr(s,x,y), x et y etant les elements qui nous concerne

        if s1[1].rfind('Cpos') >=0:
            if  s1[1].rfind('Cpos') == 0:
                l = s1[1].rfind('Pos')-1
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])
            else:
                l = s1[1].rfind('Cpos')-1
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])
        else:
                l = s1[1].rfind('Pos')-1
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])


        #recuperons l'indice de debut p1 de la chaine.

        if s11[0].startswith("Cpos"):
            s2 =  s11[0].split(",")
            s2[-1]=s2[-1].replace(")","")
            p1 = self.Cpos(sigma[s1[0]],int(s2[-1]))

        else:
            # on cherche a recuperer les expressions regulieres r1, r2 qui forment le Pos
            p1 = s11[0].split("Pos(",1)
            
            p22=[]
            
            if p1[1].rfind('TokenSeq') >=0:
                l = p1[1].rfind('TokenSeq')-1
                p11.append(p1[1][0:l]) #on recupere le premier TokenSeq() dans pos
                k = p1[1][l+1:len(p1[1])]
                n = k.index(')')
                p11.append(k[0:n+1]) # on recupere le premier TokenSeq() dans pos
                p11.append(k[n+2:len(k)-1])  # pas besoin car la valeur de c est remplace par x
                
                
                #obtenons l'expression reguliere contenue dans chaque TokenSeq
                p11[0] = p11[0].replace("TokenSeq(","")
                p11[0] = p11[0].replace(")","")
                r1 = p11[0].split(",")
                regexpression1 = ""

                #reconstruction de la deuxieme exp reguliere 
                for token  in r1:
                    regexpression1 = regexpression1 + self.ClasseC[token]
                   
                p11[1] = p11[1].replace("TokenSeq(","")
                p11[1] = p11[1].replace(")","")
                r2 = p11[1].split(",")
                regexpression2 = ""

                # reconstruction de la deuxieme exp reguliere 
                for token  in r2:
                    regexpression2 = regexpression2 + self.ClasseC[token]

                p1 = self.Pos(sigma[s1[0]],regexpression1,regexpression2,x)  # indice de debut
                

        #recuperons l'indice de fin p2 de la chaine.
        if s11[1].startswith("Pos"):

            p2 = s11[1].split("Pos(",1)
        
            p22=[]
            
        #The rfind() method finds the last occurrence of the specified value

            if p2[1].rfind('TokenSeq') >=0:
                l = p2[1].rfind('TokenSeq')-1
                p22.append(p2[1][0:l]) # on recupere le premier TokenSeq() dans pos
                k=p2[1][l+1:len(p2[1])]
                n = k.index(')')
                p22.append(k[0:n+1]) # on recupere le premier TokenSeq() dans pos
                p22.append(k[n+2:len(k)-1]) # on recupere c, troisieme parametre de pos()
    
                p22[0] = p22[0].replace("TokenSeq(","")
                p22[0] = p22[0] .replace(")","")
                r1 = p22[0] .split(",")
                regexpression1 = ""

                #reconstruction de la deuxieme exp reguliere 
                for token  in r1:
                    regexpression1 = regexpression1 + self.ClasseC[token]
               
                p22[1] = p22[1].replace("TokenSeq(","")
                p22[1] = p22[1].replace(")","")
                r2 = p22[1].split(",")
                regexpression2 = ""

                # reconstruction de la deuxieme exp reguliere 
                for token  in r2:
                    regexpression2 = regexpression2 + self.ClasseC[token]
        
                
                p2 = self.Pos(sigma[s1[0]],regexpression1,regexpression2,x)
                
        else:
            s2 =  s11[1].split(",")
            s2[-1]=s2[-1].replace(")","")
            p2 =  self.Cpos(sigma[s1[0]],int(s2[-1]))
    
        if p2 == self.BOTTOM or p1 == self.BOTTOM or p2 > len(sigma[s1[0]]) or x >= len(sigma[s1[0]]):
            return self.BOTTOM

        else:
            return self.SubStr(sigma[s1[0]],p1,p2)

    def GenerateLoop(self,Sigma,s, w):
        """ Cherche les expressions de boucles permettants d'obtenir s a partir de Sigma """
        w = dict(w)
        w3 = copy.deepcopy(w)
        k = 1
                
        if len(s) >= 3: # si sortie  a moins de 3 caracteres, la boucle n'est ni possible , ni necessaire
            for k1 in range(len(s)):
                for k2 in range(k1+1, len(s)):
                    for k3 in range(k2+1, len(s)):
                        s1 = s[k1:k2] ; s2 = s[k2: k3+1] # k2+1, k3+1 pour python nous retourne effectivement la sous chaine de k1 a k2, non de k1 a k2-1
                        #print("voici s1 et s2:",s1, s2, "\n\n")
                       # il faut gerer la profondeur de la recursivite
                        w1 , EtaTilda1 = self.GenerateStr(Sigma,s1)
                        w2 , EtaTilda2  = self.GenerateStr(Sigma,s2)
                        # Unification stape
                        #˅
                        e1 = self.ListOfAllCancatenateExpression(EtaTilda1,w1)
                        e2 = self.ListOfAllCancatenateExpression(EtaTilda2,w2)
                        DagConcatenateResult = list()
                        #print("longueurs des dags: ",len(e1),len(e2),"***********\n\n")
                        
                        if len(e1)<4 and len(e2)<4:
                            for i in range(len(e1)):
                                e = e1[i].replace("Concatenate(","")
                                e = e[0:len(e)-1]
                                for j in range(len(e2)):
                                    f = e2[j].replace("Concatenate(","")
                                    f = f[0:len(f)-1]
                                    expression = "Concatenate("+e+"˅"+f+")"
                                    DagConcatenateResult.append(expression)

                        elif len(e1) < len(e2):
                            for i in range(len(e1)):
                                e = e1[i].replace("Concatenate(","")
                                e = e[0:len(e)-1]                          
                                f = e2[i].replace("Concatenate(","")
                                f = f[0:len(f)-1]
                                expression = "Concatenate("+e+"˅"+f+")"
                                DagConcatenateResult.append(expression)
                            
                        else:
                            for i in range(len(e2)):
                                e = e1[i].replace("Concatenate(","")
                                e = e[0:len(e)-1]                          
                                f = e2[i].replace("Concatenate(","")
                                f = f[0:len(f)-1]
                                expression = "Concatenate("+e+"˅"+f+")"
                                DagConcatenateResult.append(expression) # DagConcatenateResult is a trace set

                        LoopSetResult = self.LoopSet(DagConcatenateResult,k,Sigma,s[k1:k3+1]) 
                                
                        if LoopSetResult != self.BOTTOM:

                            
                            w3[(k1,k3+1)] = w[(k1,k3+1)].union(set(LoopSetResult))
                            
        return w3

    def GenerateStr(self,entree, s):
        """ 
        cette fonction retourne  l'ensemble des facons d'obtenir s a partir de l'etat d'entree sigma
        elle retourne un dag, une structure de donnee qui permet de representer des grands ensembles
        elle utilse le principe de l'algorithme CYK, base sur la programmation dynamique, qui consiste a reconnaitre un mot
        dans un langage en passant  par sa table de transition.
        """
        EtaTilda = set() ; PsiTilda = set() 
        """ EtaSource = 0
        EtaTarget = len(s) """  
        W = {}    # table de transition, pour chaque arrete (i,j) associe l'etique qui est un ensemble d'expressions at0mique

        for i in range(len(s)+1):      
            EtaTilda = EtaTilda.union(set([i]))  # construction de l'ensemble des noeuds

        for i in range(len(s)+1):
            k = i+1
            for j in range(k,len(s)+1):
                PsiTilda = PsiTilda.union(set([(i,j)]))   # ensemble des aretes
                #PsiTilda = list(PsiTilda)
    
        for i in PsiTilda:                                # Pour chaque arete
            x = "ConstStr("+s[i[0]:i[1]]+")"                # s[i:j] =  SubStr(i,j), c'est pourquoi je concerve i[1] au lieu de i[1]-1
            ConstString = set([x])
            SubString = self.GenerateSubstring(entree,s[i[0]:i[1]])
            ConstString = ConstString.union(SubString) 
            
            W[i] = ConstString  

        baseformule = self.ExpressionConcatenate(entree,s)
        baseformule = baseformule[-1][0]


        if baseformule != [] :
            
            baseformule = "Concatenate(" + "˅".join(baseformule) + ")"
            W[(0,len(s))] =  W[(0,len(s))].union(set([baseformule]))
        
        
    
        EtaTilda = list(EtaTilda)
        
        return W ,EtaTilda

    def PrintDag(self,Listenoeud , generatestring ,entree, s):
        """ 
        prend une chaine s et son resultat GenerateStr associe i.e la table de transition et la liste des noeuds et affiche le dag correspondant
        """
        sys.stdout.reconfigure(encoding='utf-8')
        dot = Digraph(name='GenerateStr',comment='Test')


        for elt in list(Listenoeud):
            if elt == list(Listenoeud)[0]:
                dot.node(str(elt) , str(elt),color="Red")
            elif elt == list(Listenoeud)[-1]:
                dot.node( str(elt) ,str(elt) ,shape="doublecircle")
            else:
                dot.node(str(elt) , str(elt))
        if len(list(Listenoeud)) != 0:       
            for cle in generatestring:
                r = "Const" ; r = re.compile(r)       
                target =list(generatestring[cle])
            
                val1 = target[0]
                label1="{"+val1 +"}"
                dot.edge(str(cle[0]) , str(cle[1]) , label=label1)

            
        dot.attr(label= "entree_sigma = " + str(entree)  +",s = "+s)
        dot.attr(fontsize='25')
        dot.format = 'png'
        dot.render()

    def SizeNoeud(self,n,W):
        #W = dict(W)
        size = 0
        if n ==0 :
            return 1   
        else:
            for i in range(n):
                if (i,n) in W.keys():
                    size = size + self.SizeNoeud(i,W)*(len(W[(i,n)])) # +1 parceque on ajoute l'expression atomique ConstStr dans la construction de w                                                                                                                                                                                                                                                                                                                          

        return size

    def SizeDag(self,EtaTarget, W):
        """ 
        Permet de retourner le nombre d'element d'un ensemble d'expression: 
        c'est la taille des Dags  qui nous interesse particulierement.
        """
        if W != {} :
            return self.SizeNoeud(EtaTarget,W)
        else:
            return 0

    def IntersectConstStr(self,s1,s2):
        if s1 == s2 : # s1 et s2 sont sur la forme ConstStr(s1),....
            return s1
        else:
            return self.BOTTOM

    def IntersectRegex(self,t1,t2):
        """ 
        Prend en entree deux expression regulieres (sur la forme TokenSeq) et le retoune leur intersection
        """
        t1 =  t1.split(",")
        t2 = t2.split(",")
        t1[0] = t1[0].replace("TokenSeq(","")
        t1[-1] = t1[-1].replace(")","")
        t2[0] = t2[0].replace("TokenSeq(","")
        t2[-1] = t2[-1].replace(")","")
        t3 = [] # TokenSeq resultat des tokenseq t1 et t2 
        
        if len(t1) != len(t2):
            return self.BOTTOM

        else:
            for i in range(len(t1)):
                if t1[i] == t2[i]:
                    t3.append(t1[i])


            if len(t3) == 0:
                return self.BOTTOM

            else:
                Expression = ",".join(t3)
                Expression = "TokenSeq("+Expression+")"
                return Expression

    def IntersectPos(self,p1,p2):
        """ 
        P1 et p2 sont des ensemble d'elements de type Pos(r1,r2,c)
        """
        if p1.startswith("Cpos") and p2.startswith("Cpos"):
            return self.IntersectCpos(p1,p2)
        

        elif p1.startswith("Pos") and p2.startswith("Pos"):
            
            
            p1 = p1.split("Pos(",1)
            p2 = p2.split("Pos(",1)
            p11=[]
            p22=[]
            

            if p1[1].rfind('TokenSeq') >=0:
                l = p1[1].rfind('TokenSeq')-1
                p11.append(p1[1][0:l])
                k = p1[1][l+1:len(p1[1])]
                n = k.index(')')
                p11.append(k[0:n+1])
                p11.append(k[n+2:len(k)-1])
        

            if p2[1].rfind('TokenSeq') >=0:
                l = p2[1].rfind('TokenSeq')-1
                p22.append(p2[1][0:l])
                k=p2[1][l+1:len(p2[1])]
                n = k.index(')')
                p22.append(k[0:n+1])
                p22.append(k[n+2:len(k)-1])
               
            
            if p11[2] != p22[2]:  # p1[2] et p2[2] represente c et c'. si c!= c' alors c inter c' = {} et l'intersection de pos devient impossible
                return self.BOTTOM
                
            x = self.IntersectRegex(p11[0],p22[0]) # p1[0] et p2[0] representent les expressions regulieres r1 et r1'
            y = self.IntersectRegex(p11[1],p22[1])
        

            if x != self.BOTTOM and y != self.BOTTOM :
                Expression = "Pos("+x+","+y+","+p11[2]+")"
                return Expression

            else:
                return self.BOTTOM

        else:
            return self.BOTTOM
    
    def IntersectCpos(self,s1,s2):
        # le resultat est sur la forme Cpos(s1) , s1 et s2 sont sur cette meme forme
        if s1 == s2:
            return s1
        else:
            return self.BOTTOM

    def IntersectSubstr(self,s1,s2):
        """
        Intersection de 2 sous expressions subStr() 
        """

        s11=[]
        s22=[]
        s1 = s1.split(",",1)
        s2 = s2.split(",",1)
        
        if s1[1].rfind('Cpos') >=0:
            if  s1[1].rfind('Cpos') == 0:
                l = s1[1].rfind('Pos')-1
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])
            else:
                l = s1[1].rfind('Cpos')-1
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])
        else:
                l = s1[1].rfind('Pos')-1
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])


        if s2[1].rfind('Cpos') >=0:
            if  s2[1].rfind('Cpos') == 0:
                l = s2[1].rfind('Pos')-1
                s22.append(s2[1][0:l])
                s22.append(s2[1][l+1:len(s2[1])-1])
            else:
                l = s2[1].rfind('Cpos')-1
                s22.append(s2[1][0:l])
                s22.append(s2[1][l+1:len(s2[1])-1])
        else:
                l = s2[1].rfind('Pos')-1
                s22.append(s2[1][0:l])
                s22.append(s2[1][l+1:len(s2[1])-1])


        s1[0] = s1[0].replace("SubStr(","")
        s2[0] = s2[0].replace("SubStr(","")
        


        x = self.IntersectPos(s11[0],s22[0])
        y = self.IntersectPos(s11[1],s22[1])

        if x != self.BOTTOM and y != self.BOTTOM:
            Expression = "SubStr("+s1[0]+","+x+","+y+")"
            return Expression

        else: 
            return self.BOTTOM

    def IntersectLoop(self,loop1,loop2):
        """ Intersection de deux expressions Loop , c'est le premier argument de Loop qui nous interress,
        car on regarde l'intersection des trace expression"""
        
        # il revient a comparer deux expressions concatenates
        loop11 = loop1.split(")",1)
        loop11 = loop11[0].replace("Loop(","")
        loop22 = loop2.split(")",1)
        loop22 = loop22[0].replace("Loop(","")

        if loop11 == loop22: # on fait un test car  on a faire a Loop et non a LoopSet comme dans l'article. ici on travail sur le resultat de LoopSet
            return loop1
        else:
            return self.BOTTOM

    def Intersect(self,f1,f2):
        """ 
        f1 et f2 sont les ensembles d'expressions atomiques.
        """
        result = set()
        """ cpos1 = []
        cpos2 = [] # liste des expressions atomiques contenant Cpos() dans f1     f1 = list(f1) """
        f1 = list(f1)
        f2 = list(f2)
        s1 = ""
        s2 = ""
        
        
        indice1  = [i for i in range(len(f1)) if f1[i].startswith('Const')]
        indice2  = [i for i in range(len(f2)) if f2[i].startswith('Const')]


        
        if indice1!=[] and indice2!=[] :
            
            s1 = f1[indice1[0]] #pn extrait le cas particulier des constantes.
            s2 = f2[indice2[0]]
            f1.remove(s1)
            f2.remove(s2)

        if self.IntersectConstStr(s1, s2) != self.BOTTOM: # cas des constrs
            result = result.union(set([s1]))

        # cas des expressions Substr avec  Pos 
        for elt1 in f1:
            for elt2 in f2:
                if elt1.startswith('SubStr') and elt2.startswith('SubStr'):
                    x = self.IntersectSubstr(elt1,elt2)  # elt1 et elt2 st sur la forme SubStr(vi,pos(....),Pos(,,,))
                    if x != self.BOTTOM: # ce x est de la forme IntersetPos
                        result = result.union(set([x]))

                elif elt1.startswith('Loop(') and elt2.startswith('Loop('):
                    x = self.IntersectLoop(elt1,elt2)  # le resultat est sur forme d'un Loop
                    if x != self.BOTTOM:
                        result = result.union(set([x]))

        return result

    def replace_char_at_index(self,org_str, index, replacement):
        ''' Replace character at index in string org_str with the
        given replacement character.'''
        new_str = org_str
        if index < len(org_str):
            new_str = org_str[0:index] + replacement + org_str[index + 1:]
        return new_str

    def ProgramsSet(self,EtaTilda1,W1):

        ProgramsSet1 = self.ListOfAllCancatenateExpression(EtaTilda1, W1)

        for i in range(len(ProgramsSet1)):
            if "Loop" in ProgramsSet1[i]:
                r1 =re.compile("{")
                indice = re.search(r1,ProgramsSet1[i])
                indice = indice.start()
                ProgramsSet1[i] = ProgramsSet1[i][0:indice]
                lastindexcommat = ProgramsSet1[i].rfind(',')
                ProgramsSet1[i] = self.replace_char_at_index(ProgramsSet1[i], lastindexcommat, ')')



        ProgramsSet1 = set(ProgramsSet1)


        return ProgramsSet1

    def ListOfCancatenateExpression(self,dagExpression):

        """ retourne une expression concatenate du Dag """
        
        EtaTilda = copy.deepcopy(dagExpression)[1]
        W = copy.deepcopy(dagExpression)[0]
        
        ListeDesExpression = []
        
        if (0,len(EtaTilda)-1) in W.keys():
            baseformule1 = list(W[(0,len(EtaTilda)-1)])
            indice1  = [i for i in range(len(baseformule1)) if baseformule1[i].startswith('Concatenate')]
            
            if indice1!=[] :
                elt = baseformule1[indice1[0]]
                elt = elt.replace(" ", "")
                ListeDesExpression.append(elt)
                baseformule1.remove(baseformule1[indice1[0]])
                print("\n\n  vvv" ,  baseformule1 , "\n\n  www" ,)
                W[(0,len(EtaTilda)-1)] = set(baseformule1)

                return ListeDesExpression[0]
                
                
        g = Graph(len(EtaTilda))
        for elt in list(W.keys()):
            g.addEdge(elt[0], elt[1])
        
        s = EtaTilda[0]
        d = EtaTilda[-1]
        global MesChemin
        global valit
        MesChemin = {}
        valit = 0
        g.printAllPaths(s, d)
        
    
        elt = MesChemin[0]
        listedesformule = {}
        ToutesLesCombinaissons = []
        for i in range(len(elt)-1):
            listedesformule[i] = list(W[(elt[i],elt[i+1])])

        a = list(listedesformule.values())
        ToutesLesCombinaissons = list(itertools.product(*a))
        
        for temp1 in ToutesLesCombinaissons:
            temp1 = list(temp1)
            ConcatenateStringExpression = "Concatenate(" + "˅".join(temp1) + ")"
            ListeDesExpression.append(ConcatenateStringExpression)
            
        
        
        return ListeDesExpression[0]

    def ExecuteBaseCaseConstStr(self,s):

        s = s.replace("ConstStr(","")
        s = s.replace(")","")
        return s

    def ExecuteBaseCaseSubstr2(self,elt,sigma):
                
        elt= elt.split(",",1) 
        elt[0] = elt[0].replace("SubStr2(","")
        elt1 = elt[1].split(")",1)
        c = elt1[1].replace(")","")
        c = c.replace(",","")
        c = int(c)
        
       
        elt1 = elt1[0].replace("TokenSeq(","")
        elt1 = elt1.split(",")
        regexpression = ""

        
        for temp1 in elt1:
            regexpression = regexpression + self.ClasseC[temp1]

        TokenComp = re.compile(regexpression)
        Test = TokenComp.findall(sigma[elt[0]])
        

        if Test != None :
            return Test[c-1] 

        else:
            regexpression = regexpression + self.ClasseC[temp1]
            return self.BOTTOM

    def ExecuteBaseCaseSubStr(self,elt,sigma):
        
        s11=[]
        s1 = elt.split(",",1)
        s1[0] = s1[0].replace("SubStr(","")  
        cle = s1[0]
       
        p1=[]
        p11=[]
        p2=[]
        # split SubStr(s,x,y), x et y etant les elements qui nous concerne


        if s1[1].rfind('Cpos') >=0:
            if  s1[1].rfind('Cpos') == 0:                
                l = s1[1].rfind('Pos')-1 # on recupere l'indice du dernier Pos
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])

            else:
                l = s1[1].rfind('Cpos')-1              
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])              
        else:
                l = s1[1].rfind('Pos')-1
                s11.append(s1[1][0:l])
                s11.append(s1[1][l+1:len(s1[1])-1])

        #recuperons l'indice de debut p1 de la chaine.
       
        if s11[0].startswith("Cpos"):
            s2 =  s11[0].split(",")
            s2[-1]=s2[-1].replace(")","")    
            p1 = self.Cpos(sigma[cle],int(s2[-1]))
            

        else:
            # on cherche a recuperer les expressions regulieres r1, r2 qui forment le Pos
        
            p1 = s11[0].split("Pos(",1)
            p22=[]
            if p1[1].rfind('TokenSeq') >=0:
                l = p1[1].rfind('TokenSeq')-1
                p11.append(p1[1][0:l]) #on recupere le premier TokenSeq() dans pos
                k = p1[1][l+1:len(p1[1])]
                n = k.index(')')
                p11.append(k[0:n+1]) # on recupere le premier TokenSeq() dans pos
                p11.append(k[n+2:len(k)-1])  # pas besoin car la valeur de c est remplace par x
                #obtenons l'expression reguliere contenue dans chaque TokenSeq
                p11[0] = p11[0].replace("TokenSeq(","")
                p11[0] = p11[0].replace(")","")
                r1 = p11[0].split(",")
                regexpression1 = ""

                #reconstruction de la deuxieme exp reguliere 
                for token  in r1:
                    regexpression1 = regexpression1 + self.ClasseC[token]
                    
                p11[1] = p11[1].replace("TokenSeq(","")
                p11[1] = p11[1].replace(")","")
                r2 = p11[1].split(",")
                regexpression2 = ""

                # reconstruction de la deuxieme exp reguliere 
                for token  in r2:
                    regexpression2 = regexpression2 + self.ClasseC[token]
                
                p1 = self.Pos(sigma[cle],regexpression1,regexpression2,int(p11[2]))  # indice de debut


        #recuperons l'indice de fin p2 de la chaine.
        if s11[1].startswith("Pos"):      
            p2 = s11[1].split("Pos(",1)

            p22=[]
        
        #The rfind() method finds the last occurrence of the specified value

            if p2[1].rfind('TokenSeq') >=0:
                l = p2[1].rfind('TokenSeq')-1
                p22.append(p2[1][0:l]) # on recupere le premier TokenSeq() dans pos
                k=p2[1][l+1:len(p2[1])]
                n = k.index(')')
                p22.append(k[0:n+1]) # on recupere le premier TokenSeq() dans pos
                p22.append(k[n+2:len(k)-1]) # on recupere c, troisieme parametre de pos()

                p22[0] = p22[0].replace("TokenSeq(","")
                p22[0] = p22[0] .replace(")","")
                r1 = p22[0] .split(",")
                regexpression1 = ""

                #reconstruction de la deuxieme exp reguliere 
                for token  in r1:
                    regexpression1 = regexpression1 + self.ClasseC[token]
                
                p22[1] = p22[1].replace("TokenSeq(","")
                p22[1] = p22[1].replace(")","")
                r2 = p22[1].split(",")
                regexpression2 = ""

                # reconstruction de la deuxieme exp reguliere 
                for token  in r2:
                    regexpression2 = regexpression2 + self.ClasseC[token]
                
                p2 = self.Pos(sigma[cle],regexpression1,regexpression2,int(p22[2]))
            
            #p2 = self.Pos(sigma[s1[0]],regexpression1,regexpression2,int(p22[2]))
        else:
            s2 =  s11[1].split(",")
            s2[-1]=s2[-1].replace(")","")
            p2 =  self.Cpos(sigma[cle],int(s2[-1]))
           
        
               
        if p2 == self.BOTTOM or p1 == self.BOTTOM or p2 > len(sigma[cle]):
            return self.BOTTOM


        else:
            
            return self.SubStr(sigma[cle],p1,p2)
    
    def ExecuteBaseCaseLoop(self,elt,sigma):
        finalResult = []
        lastindexcommat = elt[-1].rfind(',')
        elt[0] = elt[0].replace(" ", "")
        NombreIteration = int(elt[-1][lastindexcommat+1])
        elt[-1] = elt[-1][0:lastindexcommat]
        TraceExpression = "˅".join(elt)
        TraceExpression = TraceExpression.replace("Loop(","")
        lastindexclosebracket = TraceExpression.rfind(')')
        TraceExpression = self.replace_char_at_index(TraceExpression, lastindexclosebracket , "")
        TraceExpression = str(TraceExpression + ")")
        
        for i in range(NombreIteration):
            finalResult.append(self.ExecuteElement(sigma,copy.deepcopy(TraceExpression)))
            
        finalResult = list(self.flatten(finalResult))
        return "".join(finalResult)
    
    def ExecuteElement(self,sigma,TraceExpression):
        """ Execute une expression concatenate(trace expression)sur une chaine et retoune le resultat(Sous chaine) obtenu """
        # x est la variable entiere qui nous sert de compteur de boucle dans LoopR dont k
        Result = []
        AtomiqueExpression =  TraceExpression.split("˅")
        AtomiqueExpression[0] = AtomiqueExpression[0].replace("Concatenate(","",1)
        b = list(AtomiqueExpression[-1])
        b[-1] = ""
        AtomiqueExpression[-1] = "".join(b)

        for elt in AtomiqueExpression:
                
            if elt.startswith("SubStr("):
                y = self.ExecuteBaseCaseSubStr(elt,sigma)
                Result.append(y)

            elif elt.startswith("SubStr2("):
                y = self.ExecuteBaseCaseSubstr2(elt,sigma)
                Result.append(y)

            elif elt.startswith("ConstStr("):
                y = self.ExecuteBaseCaseConstStr(elt)
                Result.append(y)
            
            

        
        if self.BOTTOM in Result:
            return self.BOTTOM
        else:
            return Result  
        
    def GetTestExemaples(self,ExempleFileName):
        result = {}
        sigma = {}
        chemin = os.path.join(BASE_DIR, 'FlashFill/Algorithmes/DataTest/' + ExempleFileName)
        with open(chemin,"r", newline=None) as f:
            for line in f:
                line = line.replace("\n","")
                if line != "":
                    example =  line.split("+++")
                    for i in range(len(example)):
                        sigma["v"+str(i+1)]  = example[i]
                    result[json.dumps(sigma)] = ''
                    sigma = {}
        
        return result
                
    def ExecuteOnElements(self,ExempleFileName,FonctionExecution):
        result = {}
        result = self.GetTestExemaples(ExempleFileName)
        for elt in result:
            chainedig = json.loads(elt)
            result[elt] = "".join(self.ExecuteElement(chainedig,FonctionExecution))
        
        return result

    def TandformeToOrignalForm(self, DicoOfOutput):
        NewDicoOutput = {}
        
        for elt in DicoOfOutput:
            chainefinal = "+++".join(list(eval(elt).values()))
            NewDicoOutput[chainefinal] = DicoOfOutput[elt]
            
        
        return NewDicoOutput
            

    def GenerateStringProgram3(self,S):
        # sans loop
        """ 
        Prend un ensemble de paires d'exemples  (entree, sortie) et retourne l'ensemble des programmes coherents avec  les exemples
        i.e  retourne l'ensemble de programmes qui permettent d'obtenir les sorties s a partir des entrees
        """
        T = []
        B = {}  
        l = list()     

        
        for elt in S:
            Result = self.GenerateStr3(json.loads(elt[0]),elt[1])
            
            T.append((elt[0],Result))  # T est une liste de tuple (sigma, GenerateStrResult)          
        

        if len(T) > 0:
            Programs = self.ProgramsSet(T[0][1][1],T[0][1][0])
            #Programs = self.ProgramsSet(T[0][1][1],T[0][1][0],T[1][1][1],T[1][1][0])
            for i in range(1,len(T)):             
                Programs = Programs.intersection(self.ProgramsSet(T[i][1][1],T[i][1][0]))
                #Programs = self.ProgramsSet(Programs[1],Programs[0],T[i][1][1],T[i][1][0])

             
        return Programs

           
    def GenerateStringProgram2(self,S):
        """ 
        Prend un ensemble de paires d'exemples  (entree, sortie) et retourne l'ensemble des programmes coherents avec  les exemples
        i.e  retourne l'ensemble de programmes qui permettent d'obtenir les sorties s a partir des entrees
        """
        T = []
        B = {}  
        l = list()     

        
        for elt in S:
            Result = self.GenerateStr2(json.loads(elt[0]),elt[1])
            
            T.append((elt[0],Result))  # T est une liste de tuple (sigma, GenerateStrResult)          
        

        if len(T) > 0:
            Programs = self.ProgramsSet(T[0][1][1],T[0][1][0])
            #Programs = self.ProgramsSet(T[0][1][1],T[0][1][0],T[1][1][1],T[1][1][0])
            for i in range(1,len(T)):             
                Programs = Programs.intersection(self.ProgramsSet(T[i][1][1],T[i][1][0]))
                #Programs = self.ProgramsSet(Programs[1],Programs[0],T[i][1][1],T[i][1][0])

             
        return Programs
