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
        


class InteractQuickFill:
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


    def GetClassC(self):
        """
        Defintion de la classe de token C,
        Il s'agit d'un dico dont les cles st les noms de tokens et
        les valeurs st les expressions regulieres correspondantes 
        """ # a present on a 23 tokens dans ClassC
        self.ClasseC = {}
        chemin = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/classeC.csv')
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





    def ExpressionConcatenateAbsolute3(self,entree,s,KeyToFind):
        """ retourne la formule concatenate(de SubStr2) basee sur les blocs et concatenate(de ConstStr) qui permet d'obtenir s a partir de entree 
        entree represente le bloc entrant, s la sous-partie recherche dans le bloc, id l'identifiant de ce bloc"""
        k1 = 0
        r1 = []
        Tokens = []
        ExpressionExecuteFormule = []
        P1 = []
        P2 = []

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
            
            
            elt = list(elt) # elt est un tuple, on le convertir en  liste
            chaine = elt[3]
            expression = elt[1]
            Tokenname = elt[2]
            TokenComp = re.compile(expression)
            Test = TokenComp.findall(entree[KeyToFind]) # Test est une liste


            if chaine in Test:
                p = Test.index(chaine)
                booleen = booleen or True

                
            else:
                booleen = booleen or False    

            
            
            if booleen:
                ExpressionExecuteFormule .append("SubStr2(" + KeyToFind + "," + "TokenSeq(" + Tokenname + ")," +str(p+1)+ ")")
            else:
                return self.BOTTOM
        
        
        return "Concatenate(" + "˅".join(ExpressionExecuteFormule) + ")"
    
    
        
    def ExpressionConcatenateAbsolute2(self,entree,s):
        """ retourne la formule concatenate(de SubStr2) basee sur les blocs et concatenate(de ConstStr) qui permet d'obtenir s a partir de entree 
        entree represente le bloc entrant, s la sous-partie recherche dans le bloc, id l'identifiant de ce bloc"""
        k1 = 0
        r1 = []
        Tokens = []
        ExpressionExecuteFormule = []
        P1 = []
        P2 = []


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


                if chaine in Test:

                    p = Test.index(chaine)
                    booleen = booleen or True

                    
                else:
                    booleen = booleen or False    

                
                
                if booleen:
                    ExpressionExecuteFormule .append("SubStr2(" + key + "," + "TokenSeq(" + Tokenname + ")," +str(p+1)+ ")")
                    break
                else:
                    return self.BOTTOM
        
        
        return "Concatenate(" + "˅".join(ExpressionExecuteFormule) + ")"
    
    
    
    
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


    def ExpressionConcatenate(self,entree,s,id):

        """ retourne la formule concatenate(de SubStr2) basee sur les blocs et concatenate(de ConstStr) qui permet d'obtenir s a partir de entree 
        entree represente le bloc entrant, s la sous-partie recherche dans le bloc, id l'identifiant de ce bloc"""
        k1 = 0
        r1 = []
        Tokens = []
        """ ExpressionExecute = []
        ExpressionExecuteFormule = [] """
        P1 = []
        P2 = []


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
                
            elt = list(elt) # elt est un tuple, on le convertir en  liste
            chaine = elt[3]
            expression = elt[1]
            Tokenname = elt[2]
            TokenComp = re.compile(expression)
            Test = TokenComp.findall(entree) # Test est une liste


            if chaine in Test:

                p = Test.index(chaine)
                booleen = booleen or True

                
            else:
                booleen = booleen or False    

            
            
            if booleen:
                ExpressionExecute = (id,expression,p)
                ExpressionExecuteFormule = ("SubStr2(" + id + "," + "TokenSeq(" + Tokenname + ")," +str(p+1)+ ")")
                
                return (ExpressionExecute,ExpressionExecuteFormule)

            else:
                return self.BOTTOM
        


    def GeneratePosition(self,s,k):
        
        """ retourne l'ensemble des differentes facons de representer une position
        donnee dans une chaine donnee avec les primitives du langage  """
        POsList = []  # variable de formatage 
        PosChain = ""
        #result = set()
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

    
    def GenerateSubstring(self,entree,s,bi):
        # entree et s represente les blocs d'entree et les blocs du cote de la sortie.
        """ On va retourner les expressions SubStr avec uniquement les expressions Pos, car elles sont basee sur les expressions regulieres ??? revoir ce commentaire """
        result = set()

        
        if s in entree:     
            k = entree.index(s)         
            k1 = len(s)+k-1
            Y1 = self.GeneratePosition(entree,k) # Y1 est un tuple car GeneratePosition retourne un tuple
          
            Y1 = Y1[1]  # ensemble de facons de retourner l'indince de debut de s sans entree
            Y1 = list(Y1)

            


            for i in range(len(Y1)):
                if entree.isdigit():
                    listeofnumlelements = re.finditer(r'-*\d+', Y1[i])
                    for elt in listeofnumlelements:
                        if int(elt.group()) == int(entree)  and elt.group() == entree:
                             Y1[i] = Y1[i][:elt.span()[0]] + bi + Y1[i][elt.span()[1]:]
                else:
                    Y1[i] = Y1[i].replace(entree,bi,10)
            
            Y2 = self.GeneratePosition(entree, k1)
            Y2 = Y2[1]
            Y2 = list(Y2)


            #print("Conditon  : " , Y2)
           
            for i in range(len(Y2)):
                if entree.isdigit():
                    listeofnumlelements = re.finditer(r'-*\d+', Y2[i])
                    for elt in listeofnumlelements:
                        if int(elt.group()) == int(entree) and elt.group() == entree :
                            Y2[i] = Y2[i][:elt.span()[0]] + bi + Y2[i][elt.span()[1]:]
                else:
                    Y2[i]  = Y2[i].replace(entree,bi,10) 
            


            #print("Conditon  : " , Y2)
            SubResult = self.SubStrs(bi,Y1,Y2) # le resultat de Substrs est deja un set            
            result = result.union(SubResult) 
                                    
        return result


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


  
    def ListOfAllCancatenateExpression(self,EtaTilda , W):
        """ Fonction permettant de d'avoir la liste de toutes les expressions concatenate """
        
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
    

    def GenerateBlocksPrograms(self,Correspondance,entree,s,Blocks):
        """prend le dictionnaire de correspondance en block pour un (sigma,s) et construit l'ensemble de formules 
        pour chaque blocks, construit le Dag correspondant pour l'exemple (sigma,s)
        les parametres entree et s vont nous servir pour construire la formule de base si elle existe"""
       
        #Correspondance = eval(Correspondance)
        inter = [] # pour contenir le resultat de Expression concatenate
        EtaTilda = []; PsiTilda = []; b =[] # b contient les identiants des blocks
        W = {}    # table de transition, pour chaque arrete (i,j) associe l'etique qui est un ensemble d'expressions at0mique
        #Le nombre de noeuds dans le graphe est fonction du nombre de blocs dans la sortie s.
        
        for key in Blocks.keys():
            b.append(key)

        for i in range(len(Correspondance)+1):      
            EtaTilda.append(i)# construction de l'ensemble des noeuds

        #construction de l'ensemble d'aretes
        for i in range(len(Correspondance)):      
            PsiTilda.append((i,i+1))
    
        i = 0 # variable qui nous permet de recuperer les aretes dans PsiTilda
        for key in Correspondance.keys():
            inter = []
            if  i <= len(PsiTilda):
                if str(Correspondance[key]) == "ConstStr":
                    t = key.split("***") # recuperation du block
                    t = t[1]
                    x = "ConstStr("+str(t)+")"
                    ConstString = set([x])
                    W[PsiTilda[i]] = ConstString
                    i += 1 
                else:
                    t = key.split("***") # recuperation du block
                    t = t[1]
                    #print("Voici  SubString :" , str(Correspondance[key]),str(t),b[i])
                    SubString = self.GenerateSubstring(str(Correspondance[key]),str(t),b[i])
                    
                    SubString = set(SubString)  

                    SubStr2 = self.ExpressionConcatenate(str(Correspondance[key]),str(t),b[i])
                    SubStr2 = SubStr2[-1] 

                    
                   
                    if self.BOTTOM not in SubStr2:
                        inter.append(SubStr2)
                        SubString = SubString.union(inter)

                    W[PsiTilda[i]] =  SubString
                    i += 1                  
                
        ProgramsResult = self. ListOfAllCancatenateExpression(EtaTilda ,W)
        # ajout de la formule de base, contenant les formules SubStr2
       
        """  baseformule = self.ExpressionConcatenate(entree,s)
        baseformule = baseformule[-1][0]

        if baseformule != [] :
            
            baseformule = "Concatenate(" + "˅".join(baseformule) + ")"
        ProgramsResult.append(baseformule)
         """
        
        return ProgramsResult



    def GenerateStringProgram(self,S):
        """ 
        S est un ensemble de triplets(x,y,z) : x est le dictionnaire correspondant a
        l'exemple (y,z). Le but de cette fonction est de retourner l'ensemble des programmes 
        coherents avec tous les exemple de S
        """
        # pour plusieurs decoupage en blocs
        #print("Voici le type de S : " , type(S))
        T = []
        Blocks = {}
        if type(S) == tuple:
           
            for key in eval(S[0]).keys():
                decoupe = key.split("***")
                decoupe = decoupe[0]
                Blocks[str(decoupe)] = eval(S[0])[key]
               
            Result = self.GenerateBlocksPrograms(eval(S[0]),eval(S[1]),S[2], Blocks)
            T.append(Result)

        else:
            for elt in S:
                
                for key in eval(elt[0]).keys():
                    decoupe = key.split("***")
                    decoupe = decoupe[0]
                    Blocks[str(decoupe)] = eval(elt[0])[key]
                

                #print("voici les element envoyer  : " , eval(elt[0]),eval(elt[1]),elt[2], Blocks)
                Result = self.GenerateBlocksPrograms(eval(elt[0]),eval(elt[1]),elt[2], Blocks)
            
                T.append(Result)  # T la liste contenant l'ensemble de programmes pour chaque exemple de S              

        """    for t in T:
            print(len(t)) """

        if len(T) > 0:
            Programs = set(T[0])
            
            for i in range(1,len(T)):
                
                Programs = Programs.intersection(set(T[i]))
       
        return Programs
    



    def GenerateStringProgramFilter(self,exemple,S):
        """ 
        exemple est un triplet(x,y,z) : x est le dictionnaire correspondant a
        l'exemple (y,z). Le but de cette fonction est de retourner l'ensemble des programmes 
        coherents avec  le triplet exemple et l'ensemble de triplets S
        """

        Result = self.GenerateStringProgram(exemple)
    
        for elt in S:
            Result = self.FilterPrograms(Result,S[elt][0],S[elt][1])


        return Result

        

    def GetInteractData(self):
        S =[]
        s = set()
        chemin = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/interactData.txt')
        with open(chemin,"r", newline=None) as f:
            for line in f:
                line = line.replace("\n", "")

                if line == "***":
                    S.append(s)
                    s = set()

                else: 
                    if line != "":         
                        x = eval(line)
                        s = s.union(set([x]))
            f.close() 
        if(len(S) == 0):
            S.append(s)
            
        return S
    

######################### Eriture de la fonction des programmes


    def ExecuteBaseCaseConstStr(self,s):

        s = s.replace("ConstStr(","")
        s = s.replace(")","")
        #s = s.split("***")
        return s
        


    def ExecuteBaseCaseSubstr2(self,elt,valeur):
        

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
        Test = TokenComp.findall(valeur[elt[0]])


        if Test != None :
            return Test[c-1] 

        else:
            regexpression = regexpression + self.ClasseC[temp1]
            return self.BOTTOM




    def FilterProgrammesExecution(self,casekey , Sorties , Entrers, ListOfProgrammes):
        """ Filtre les programes par rapport a liste des entree sorties """

        Result = ListOfProgrammes
        NewResult  = []
        compteur = 0
        RepValue = ""

        for elt in Entrers:

            if compteur < casekey:
                for prog in Result:
                    RepValue = self.ExecuteFonction(prog,eval(Entrers[elt]))
                    if RepValue == Sorties[elt]:
                        NewResult.append(prog)
                    
                Result = NewResult
                NewResult = []
                compteur = compteur + 1
            else:
                break
        

        return Result



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




    def ExecuteBaseCaseDecoupeSubstr2(self,elt,sigma):
       
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



    def ExecuteFonctionDecoupe(self,TraceExpression,entree):
        """ execute un programme sur une entree sigma pour trouver sa sortie correspondante """

        Result = []
        AtomiqueExpression =  TraceExpression.split("˅")
        AtomiqueExpression[0] = AtomiqueExpression[0].replace("Concatenate(","",1)
        b = list(AtomiqueExpression[-1])
        b[-1] = "" #  on remplace la derniere parenthese fermente par ""
        AtomiqueExpression[-1] = "".join(b)
       

        for elt in AtomiqueExpression:

            if elt.startswith("SubStr2"):
                y = self.ExecuteBaseCaseDecoupeSubstr2(elt,entree)
                Result.append(y)
                

        if self.BOTTOM in Result:
            return self.BOTTOM
        else:
            Result = "".join(Result)
            return Result
        

    
    def ExecuteFonction(self,TraceExpression,entree):
        # entree c'est sigma en dictionnaire, valeur c'est la chaine sigma
        """ execute un programme sur une entree sigma pour trouver sa sortie correspondante """
        sigma = {}
        for key in entree.keys():
            t = key.split("***")
            t = t[0]
            sigma[t] = entree[key]

        Result = []
        AtomiqueExpression =  TraceExpression.split("˅")
        AtomiqueExpression[0] = AtomiqueExpression[0].replace("Concatenate(","",1)
        b = list(AtomiqueExpression[-1])
        b[-1] = "" #  on remplace la derniere parenthese fermente par ""
        AtomiqueExpression[-1] = "".join(b)
        

        for elt in AtomiqueExpression:
            if elt.startswith("SubStr("):
                y = self.ExecuteBaseCaseSubStr(elt,sigma)               
                Result.append(y)

            elif elt.startswith("SubStr2"):
                y = self.ExecuteBaseCaseSubstr2(elt,sigma)
                Result.append(y)


            elif elt.startswith("ConstStr"):
                y = self.ExecuteBaseCaseConstStr(elt)
                Result.append(y)
                          

        if self.BOTTOM in Result:
            return self.BOTTOM
        else:
            Result = "".join(Result)
            return Result



    def FilterPrograms(self,P,valeur,s):
        """ prend un ensemble de programmes P et un exemple d'entree-sortie sigma, s
        et retourne les programmes de P qui permettent de trouver s a partir de sigma. """
        programResult = []

        for program in P:
            test = self.ExecuteFonction(program,valeur)
            if test == s:
                programResult.append(program)

               
        return programResult


