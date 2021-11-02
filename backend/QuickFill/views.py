import copy
import re
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import OrderedDict
import QuickFill.Algorithmes.InteractQuickFill as IFF
import os
import time
import json
import psutil
import random
from backend.settings import BASE_DIR
from operator import itemgetter
from itertools import groupby




class QuickFillExecutionList(APIView):    
    def get(self, request, format=None):
            datas = {"Cette requetes montre que tu volais un peu experiment je te comprends mais cette application n'as pas de faille de securite ne pers pas ton temps"}
            return Response(datas)
        
        
    def post(self, request, format=None):

                DataEntreeBrute = eval(request.data.get("data").get("DataEntreeBrute"))
                DataGlobal = eval(request.data.get("data").get("DataGlobal"))
                Test = IFF.InteractQuickFill()
                Test.GetClassC()
                Entrer = DataGlobal[0]["Entrer"]
                IndiceColoneSortie = len(Entrer.keys())+1
                ListeEntreFormeAtraiter = {}
                MonElment  = {}
                Maformuledecoupe = []
                programme = []
                s = []
                ListeDesElementsPourProgramme = {}
                ClesPourProgrammeDejaTraiter = []
                NewListOfStructureElements = []
                TraiementEntrer = []

            
            
        
                for elt in DataGlobal:
                        if json.dumps(elt["Entrer"]) in ClesPourProgrammeDejaTraiter:
                                continue
                        else:
                                newListe = []
                                for ett in DataGlobal:
                                        if ett["Entrer"] == elt["Entrer"]:
                                                newListe.append(ett)
                                                ElementToAdd = {}
                                                ElementToAdd[list(ett.keys())[0]] = ett[list(ett.keys())[0]]
                                
                        
                                ListeDesElementsPourProgramme[json.dumps(elt)] = newListe
                                ClesPourProgrammeDejaTraiter.append(json.dumps(elt["Entrer"]))
                            
            
            
                for elt in ListeDesElementsPourProgramme:
                        ListeDesElementsPourProgramme[elt] = sorted(ListeDesElementsPourProgramme[elt], key = lambda i: list(i.keys())[0])
            

            
            
            
            
                MonElment = ListeDesElementsPourProgramme[list(ListeDesElementsPourProgramme.keys())[0]]

            
                for ett in MonElment:

                        key = list(ett.keys())[0]
                        if ett[key] == "ConstStr":
                                
                                decoupekeyval = key.split("***")
                                Formuletest = "ConstStr(" + decoupekeyval[1] + ")"
                                
                        else:
                                Formuletest = Test.ExpressionConcatenateAbsolute3(ett["Entrer"],ett[key],ett["KeyOfElement"])
                                
                                


                        Maformuledecoupe.append(Formuletest)


        
           
           
           
           



                for elt in DataEntreeBrute:
                        Traite1 = {}
                        i = 0
                        chaineRetire = []
                        for ett in Maformuledecoupe:
                                i=i+1

                                if(ett.startswith("ConstStr")):
                                        Traite1["b"+str(i)] = ett
                                else:
                                        TraiementEntrer = elt["Entrer"]
                                

                                Traite1["b"+str(i)] = Test.ExecuteFonctionDecoupe(ett,TraiementEntrer)
                        


                        ListeEntreFormeAtraiter[json.dumps(elt)] = [elt["position"],Traite1,elt["Entrer"]]
     

            
           
            
                chemin = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/interactData.txt')
                chemin1 = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/resultdata1.txt')
            
            
                for elt in ListeDesElementsPourProgramme:
                        newdict1 = {}
                        NewEntrer = []
                        NewSortie = []
                        for elt2 in ListeDesElementsPourProgramme[elt]:
                                newdict1[list(elt2.keys())[0]] = elt2[list(elt2.keys())[0]]
                                NewEntrer = elt2["Entrer"]
                                NewSortie = elt2["Output"]
                        
                        
                        NewListOfStructureElements.append([newdict1,NewEntrer,NewSortie])
                    
                with open(chemin, 'w') as f:
                        for elt in NewListOfStructureElements:
                                f.write(str((json.dumps(elt[0]) ,json.dumps(elt[1]) , elt[2])) +'\n')
                        
                            
                datas = {}
                start = time.time()
                pid = os.getpid()
                ps = psutil.Process(pid)


                s = Test.GetInteractData()[0]
                programme = list(Test.GenerateStringProgram(s))



                FilteringOutPut = list(s)
                dicsept1 = {}
                dicsept2 = {}

                for elt in FilteringOutPut:
                        dicsept1[json.dumps(elt[1])] = elt[2]
                        dicsept2[json.dumps(elt[1])] = elt[0]


                if len(dicsept1.keys()) > 0 :
                        programme = Test.FilterProgrammesExecution(1,dicsept1,dicsept2,programme)





                random_index = random.randint(0,len(programme)-1)
                datas["NombreExemples"] = len(programme)
                datas["IndiceColoneSortie"] = IndiceColoneSortie
            
            
            
                for elt in DataEntreeBrute:
                        elt["Output"] = Test.ExecuteFonction(programme[random_index],ListeEntreFormeAtraiter[json.dumps(elt)][1])
                   
            
            
                datas["memoryQuickfill"] = ps.memory_info()[0]/1048576
                time.sleep(1)
                end = time.time()

                timewastQuickfill = end - start

                datas["timewastQuickfill"] = timewastQuickfill
                datas["DataFinalToBeReplace"] = DataEntreeBrute


                datas["indiceduprogrammechoisi"] = random_index
                datas["listedesprogrammes"] = programme


                with open(chemin1, 'w') as f:
                        f.write("Temps d'execution : " + str(datas["timewastQuickfill"]) + "\n")
                        f.write("Taille de la memoire : " + str(datas["memoryQuickfill"]) + "\n")


                return Response(datas)
    
    
    @classmethod
    def get_extra_actions(cls):
        return []









class QuickFillExecutionListWithFilter(APIView):    
    def get(self, request, format=None):
            datas = {"Cette requetes montre que tu volais un peu experiment je te comprends mais cette application n'as pas de faille de securite ne pers pas ton temps"}
            return Response(datas)
        
        
    def post(self, request, format=None):
            
            
                DataEntreeBrute = eval(request.data.get("data").get("DataEntreeBrute"))
                DataGlobal = eval(request.data.get("data").get("DataGlobal"))
                MesSorties = eval(request.data.get("data").get("MesSorties"))
                Test = IFF.InteractQuickFill()
                Test.GetClassC()
                Entrer = DataGlobal[0]["Entrer"]
                IndiceColoneSortie = len(Entrer.keys())+1
                ListeEntreFormeAtraiter = {}
                MonElment  = {}
                Maformuledecoupe = []
                programme = []
                s = []
                ListeDesElementsPourProgramme = {}
                ClesPourProgrammeDejaTraiter = []
                NewListOfStructureElements = []
                ListeFilterFormetraiter= {}

            
        
                for elt in DataGlobal:
                        
                        if json.dumps(elt["Entrer"]) in ClesPourProgrammeDejaTraiter:
                                continue
                        else:
                                newListe = []
                                for ett in DataGlobal:
                                        if ett["Entrer"] == elt["Entrer"]:
                                                newListe.append(ett)
                                                ElementToAdd = {}
                                                ElementToAdd[list(ett.keys())[0]] = ett[list(ett.keys())[0]]
                                
                        
                                ListeDesElementsPourProgramme[json.dumps(elt)] = newListe
                                
                                ClesPourProgrammeDejaTraiter.append(json.dumps(elt["Entrer"]))
                            
            
            
                for elt in ListeDesElementsPourProgramme:
                        ListeDesElementsPourProgramme[elt] = sorted(ListeDesElementsPourProgramme[elt], key = lambda i: list(i.keys())[0])
            

            
            
            
                MonElment = ListeDesElementsPourProgramme[list(ListeDesElementsPourProgramme.keys())[0]]

            
                for ett in MonElment:

                        key = list(ett.keys())[0]
                        if ett[key] == "ConstStr":
                                
                                decoupekeyval = key.split("***")
                                Formuletest = "ConstStr(" + decoupekeyval[1] + ")"
                                
                        else:
                                Formuletest = Test.ExpressionConcatenateAbsolute3(ett["Entrer"],ett[key],ett["KeyOfElement"])
                                
                                
                        Maformuledecoupe.append(Formuletest)
        
           
           
           





                for elt in DataEntreeBrute:
                        Traite1 = {}
                        i = 0
                        chaineRetire = []
                        for ett in Maformuledecoupe:
                                i=i+1
                                if(ett.startswith("ConstStr")):
                                        Traite1["b"+str(i)] = ett
                                else:
                                        TraiementEntrer = elt["Entrer"]
                                        Traite1["b"+str(i)] = Test.ExecuteFonctionDecoupe(ett,TraiementEntrer)
                        

                        
                        ListeEntreFormeAtraiter[json.dumps(elt)] = [elt["position"],Traite1,elt["Entrer"]]
     

            
            
            
                chemin = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/interactData.txt')
                chemin1 = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/resultdata2.txt')
            

                for elt in ListeDesElementsPourProgramme:
                        newdict1 = {}
                        NewEntrer = []
                        NewSortie = []
                        for elt2 in ListeDesElementsPourProgramme[elt]:
                                newdict1[list(elt2.keys())[0]] = elt2[list(elt2.keys())[0]]
                                NewEntrer = elt2["Entrer"]
                                NewSortie = elt2["Output"]
                        
                        
                        NewListOfStructureElements.append([newdict1,NewEntrer,NewSortie])

                    
                with open(chemin, 'w') as f:
                        for elt in NewListOfStructureElements:
                                f.write(str((json.dumps(elt[0]) ,json.dumps(elt[1]) , elt[2])) +'\n')
                                break


       
                for elt in MesSorties:
                        Traite1 = {}
                        i = 0
                        for ett in Maformuledecoupe:
                                i=i+1
                                if(ett.startswith("ConstStr")):
                                        Traite1["b"+str(i)] = ett
                                else:
                                        Traite1["b"+str(i)] = Test.ExecuteFonctionDecoupe(ett,elt["Entrer"])
                        

                        ListeFilterFormetraiter[json.dumps(elt)] = [Traite1,elt["Output"]]
                                   


                datas = {}
                start = time.time()
                pid = os.getpid()
                ps = psutil.Process(pid)
                s = Test.GetInteractData()[0]
                programme = list(Test.GenerateStringProgramFilter(s,ListeFilterFormetraiter))


                random_index = random.randint(0,len(programme)-1)
                datas["NombreExemples"] = len(programme)
                datas["IndiceColoneSortie"] = IndiceColoneSortie
            
            
            
                for elt in DataEntreeBrute:
                        elt["Output"] = Test.ExecuteFonction(programme[random_index],ListeEntreFormeAtraiter[json.dumps(elt)][1])
                        
            

                datas["memoryQuickfill"] = ps.memory_info()[0]/1048576
                time.sleep(1)
                end = time.time()

                timewastQuickfill = end - start

                datas["timewastQuickfill"] = timewastQuickfill
                datas["DataFinalToBeReplace"] = DataEntreeBrute


                datas["indiceduprogrammechoisi"] = random_index
                datas["listedesprogrammes"] = programme

                with open(chemin1, 'w') as f:
                        f.write("Temps d'execution : " + str(datas["timewastQuickfill"]) + "\n")
                        f.write("Taille de la memoire : " + str(datas["memoryQuickfill"]) + "\n")


                return Response(datas)
    
    
    @classmethod
    def get_extra_actions(cls):
        return []






class QuickFillExecutionListManyBlock(APIView):    
    def get(self, request, format=None):
            datas = {"Cette requetes montre que tu volais un peu experiment je te comprends mais cette application n'as pas de faille de securite ne pers pas ton temps"}
            return Response(datas)
        
        
    def post(self, request, format=None):
            
            
                DataEntreeBrute = eval(request.data.get("data").get("DataEntreeBrute"))
                DataGlobal = eval(request.data.get("data").get("DataGlobal"))
                Test = IFF.InteractQuickFill()
                Test.GetClassC()
                Entrer = DataGlobal[0]["Entrer"]
                IndiceColoneSortie = len(Entrer.keys())+1
                ListeEntreFormeAtraiter = {}
                MonElment  = {}
                Maformuledecoupe = []
                programme = []
                s = []
                ListeDesElementsPourProgramme = {}
                ClesPourProgrammeDejaTraiter = []
                NewListOfStructureElements = []

            
            
        
                for elt in DataGlobal:
                        
                        if json.dumps(elt["Entrer"]) in ClesPourProgrammeDejaTraiter:
                                continue
                        else:
                                newListe = []
                                for ett in DataGlobal:
                                        if ett["Entrer"] == elt["Entrer"]:
                                                newListe.append(ett)
                                                ElementToAdd = {}
                                                ElementToAdd[list(ett.keys())[0]] = ett[list(ett.keys())[0]]
                                
                        
                                ListeDesElementsPourProgramme[json.dumps(elt)] = newListe
                                
                                ClesPourProgrammeDejaTraiter.append(json.dumps(elt["Entrer"]))
                            
            
            
                for elt in ListeDesElementsPourProgramme:
                        ListeDesElementsPourProgramme[elt] = sorted(ListeDesElementsPourProgramme[elt], key = lambda i: list(i.keys())[0])
            

            
            
            
            
                MonElment = ListeDesElementsPourProgramme[list(ListeDesElementsPourProgramme.keys())[0]]

            
                for ett in MonElment:

                        key = list(ett.keys())[0]
                        if ett[key] == "ConstStr":
                                
                                decoupekeyval = key.split("***")
                                Formuletest = "ConstStr(" + decoupekeyval[1] + ")"
                                
                        else:
                                Formuletest = Test.ExpressionConcatenateAbsolute3(ett["Entrer"],ett[key],ett["KeyOfElement"])
                        
                        


                        Maformuledecoupe.append(Formuletest)
        
           
           
           
           


                for elt in DataEntreeBrute:
                        Traite1 = {}
                        i = 0
                        chaineRetire = []
                        for ett in Maformuledecoupe:
                                i=i+1
                                if(ett.startswith("ConstStr")):
                                        Traite1["b"+str(i)] = ett
                                else:
                                        TraiementEntrer = elt["Entrer"]
                                        Traite1["b"+str(i)] = Test.ExecuteFonctionDecoupe(ett,TraiementEntrer)
                        

                        
                        ListeEntreFormeAtraiter[json.dumps(elt)] = [elt["position"],Traite1,elt["Entrer"]]
     

            
            
            
                chemin = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/interactData.txt')
                chemin1 = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/resultdata3.txt')
            
            
                for elt in ListeDesElementsPourProgramme:
                        newdict1 = {}
                        NewEntrer = []
                        NewSortie = []
                        for elt2 in ListeDesElementsPourProgramme[elt]:
                                newdict1[list(elt2.keys())[0]] = elt2[list(elt2.keys())[0]]
                                NewEntrer = elt2["Entrer"]
                                NewSortie = elt2["Output"]
                        
                        
                        NewListOfStructureElements.append([newdict1,NewEntrer,NewSortie])
                    
                with open(chemin, 'w') as f:
                        for elt in NewListOfStructureElements:
                                f.write(str((json.dumps(elt[0]) ,json.dumps(elt[1]) , elt[2])) +'\n')
                        
                            
                datas = {}
                start = time.time()
                pid = os.getpid()
                ps = psutil.Process(pid)
                s = Test.GetInteractData()[0]
                programme = list(Test.GenerateStringProgram(s))

                FilteringOutPut = list(s)
                dicsept1 = {}
                dicsept2 = {}

                for elt in FilteringOutPut:
                        dicsept1[json.dumps(elt[1])] = elt[2]
                        dicsept2[json.dumps(elt[1])] = elt[0]


                if len(dicsept1.keys()) > 0 :
                        programme = Test.FilterProgrammesExecution(len(dicsept1.keys()),dicsept1,dicsept2,programme)


                random_index = random.randint(0,len(programme)-1)
                datas["NombreExemples"] = len(programme)
                datas["IndiceColoneSortie"] = IndiceColoneSortie
            
            
            
                for elt in DataEntreeBrute:
                        elt["Output"] = Test.ExecuteFonction(programme[random_index],ListeEntreFormeAtraiter[json.dumps(elt)][1])
                        
            
            
                datas["memoryQuickfill"] = ps.memory_info()[0]/1048576
                time.sleep(1)
                end = time.time()

                timewastQuickfill = end - start

                datas["timewastQuickfill"] = timewastQuickfill
                datas["DataFinalToBeReplace"] = DataEntreeBrute
                datas["indiceduprogrammechoisi"] = random_index
                datas["listedesprogrammes"] = programme


                with open(chemin1, 'w') as f:
                        f.write("Temps d'execution : " + str(datas["timewastQuickfill"]) + "\n")
                        f.write("Taille de la memoire : " + str(datas["memoryQuickfill"]) + "\n")


                return Response(datas)
    
    
    @classmethod
    def get_extra_actions(cls):
        return []