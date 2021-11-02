from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import FlashFill.Algorithmes.UniformQuickFill as UFF
import os
import time
import psutil
import random
import json
from backend.settings import BASE_DIR




class FlashFillExecutionList(APIView):    
    def get(self, request, format=None):
            datas = {"Cette requetes montre que tu volais un peu experiment je te comprends mais cette application n'as pas de faille de securite ne pers pas ton temps"}
            return Response(datas)
        
        
    def post(self, request, format=None):
        
        datas = {}
        DonneAtraiter = request.data.get("data").get("DataEntree")
        ListOfElements = eval(DonneAtraiter)
        timewastFlasfill = 0
        
        DataTestExemples = {}
        DataFinalToBeReplace = {}
        DataExperience = []
        IndiceColoneSortie = ""
        MessageCles = ""
        NombreExemples = 0
        random_index =0 
        i = 0
        for etl in ListOfElements:
            decoupe =  etl[0].split("***")
            IndiceExemple = decoupe[0]
            valeurSortie = decoupe[1]
            
            if valeurSortie != "":

                if etl[1] != "":
                    ChaineEntrainement = etl[1] + "---" + valeurSortie
                    DataExperience.append(ChaineEntrainement)
                    IndiceColoneSortie = len(etl[1].split("+++"))
            else:
                
                if etl[1] != "":
                    DataTestExemples[etl[1]] = IndiceExemple
                    
                
        
        

    
    
        if len(DataExperience) != 0:
            
            spetResultOne = {}
            chemin = os.path.join(BASE_DIR, 'FlashFill/Algorithmes/data.txt')
            chemin2 = os.path.join(BASE_DIR, 'FlashFill/Algorithmes/DataTest/dataTest.txt')
            chemin3  = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/resultdata.txt')
            with open(chemin, 'w') as f:
                f.write('\n'.join(DataExperience))
                
            with open(chemin2, 'w') as f:
                f.write('\n'.join(list(DataTestExemples.keys())))
            
            start = time.time()
            pid = os.getpid()
            ps = psutil.Process(pid)
            filename = 'dataTest.txt'
            Test = UFF.UniformQuickFill()
            Test.GetClassC()
            ListeOfProgrammes = list(Test.GenerateStringProgram2(Test.GetExamples()[0]))
            if len(ListeOfProgrammes) != 0:
                NombreExemples = len(ListeOfProgrammes)
                random_index = random.randint(0,len(ListeOfProgrammes)-1)
                spetResultOne = Test.ExecuteOnElements(filename,ListeOfProgrammes[random_index])
                spetResultOne = Test.TandformeToOrignalForm(spetResultOne)
                
                for elt2 in spetResultOne:
                    DataFinalToBeReplace[DataTestExemples[elt2]] = spetResultOne[elt2]
                    
                MessageCles = "OK"
                
            else:
                MessageCles = "False"
            
            datas["memoryFlasfill"] = ps.memory_info()[0]/1048576   
            time.sleep(1)
            end = time.time()
            
            timewastFlasfill = end - start
        else:
            MessageCles = "False"
        
        
        datas["MessageCles"]    = MessageCles
        datas["DataFinalToBeReplace"] = DataFinalToBeReplace
        datas["IndiceColoneSortie"] = IndiceColoneSortie
        datas["timewastFlasfill"] = timewastFlasfill
        datas["NombreExemples"] = NombreExemples
        
        datas["indiceduprogrammechoisi"] = random_index
        datas["listedesprogrammes"] = ListeOfProgrammes
                
        
        with open(chemin3, 'w') as f:
                f.write("Temps d'execution : " + str(datas["timewastFlasfill"]) + "\n")
                f.write("Taille de la memoire : " + str(datas["memoryFlasfill"]) + "\n")           
                
        
        
        



        return Response(datas)

    @classmethod
    def get_extra_actions(cls):
        return []





class FlashFillExecutionFreeLoopList(APIView):    
    def get(self, request, format=None):
            datas = {"Cette requetes montre que tu volais un peu experiment je te comprends mais cette application n'as pas de faille de securite ne pers pas ton temps"}
            return Response(datas)
        
        
    def post(self, request, format=None):
        
        datas = {}
        DonneAtraiter = request.data.get("data").get("DataEntree")
        ListOfElements = eval(DonneAtraiter)
        timewastFlasfill = 0
        
        DataTestExemples = {}
        DataFinalToBeReplace = {}
        DataExperience = []
        IndiceColoneSortie = ""
        MessageCles = ""
        NombreExemples = 0
        random_index =0
        i = 0
        for etl in ListOfElements:
            decoupe =  etl[0].split("***")
            IndiceExemple = decoupe[0]
            valeurSortie = decoupe[1]
            
            if valeurSortie != "":

                if etl[1] != "":
                    ChaineEntrainement = etl[1] + "---" + valeurSortie
                    DataExperience.append(ChaineEntrainement)
                    IndiceColoneSortie = len(etl[1].split("+++")) 
            else:
                
                if etl[1] != "":
                    DataTestExemples[etl[1]] = IndiceExemple
                    
                
        
        

    
    
        if len(DataExperience) != 0:
            
            spetResultOne = {}
            chemin = os.path.join(BASE_DIR, 'FlashFill/Algorithmes/data.txt')
            chemin2 = os.path.join(BASE_DIR, 'FlashFill/Algorithmes/DataTest/dataTest.txt')
            chemin3  = os.path.join(BASE_DIR, 'QuickFill/Algorithmes/resultdata.txt')
            with open(chemin, 'w') as f:
                f.write('\n'.join(DataExperience))
                
            with open(chemin2, 'w') as f:
                f.write('\n'.join(list(DataTestExemples.keys())))
            
            start = time.time()
            pid = os.getpid()
            ps = psutil.Process(pid)
            filename = 'dataTest.txt'
            Test = UFF.UniformQuickFill()
            Test.GetClassC()
            ListeOfProgrammes = list(Test.GenerateStringProgram3(Test.GetExamples()[0]))
            if len(ListeOfProgrammes) != 0:
                NombreExemples = len(ListeOfProgrammes)
                random_index = random.randint(0,len(ListeOfProgrammes)-1)
                spetResultOne = Test.ExecuteOnElements(filename,ListeOfProgrammes[random_index])
                spetResultOne = Test.TandformeToOrignalForm(spetResultOne)
                
                for elt2 in spetResultOne:
                    DataFinalToBeReplace[DataTestExemples[elt2]] = spetResultOne[elt2]
                


                    
                MessageCles = "OK"
                
            else:
                MessageCles = "False"
            
            datas["memoryFlasfill"] = ps.memory_info()[0]/1048576   
            time.sleep(1)
            end = time.time()
            
            timewastFlasfill = end - start
        else:
            MessageCles = "False"
        
        
        datas["MessageCles"]    = MessageCles
        datas["DataFinalToBeReplace"] = DataFinalToBeReplace
        datas["IndiceColoneSortie"] = IndiceColoneSortie
        datas["timewastFlasfill"] = timewastFlasfill
        datas["NombreExemples"] = NombreExemples
        datas["indiceduprogrammechoisi"] = random_index
        if NombreExemples >  1000000:
            datas["listedesprogrammes"] = ListeOfProgrammes[:1000000]
        else:
            datas["listedesprogrammes"] = ListeOfProgrammes

        with open(chemin3, 'w') as f:
                f.write("Temps d'execution : " + str(datas["timewastFlasfill"]) + "\n")
                f.write("Taille de la memoire : " + str(datas["memoryFlasfill"]) + "\n")                

        


        return Response(datas)

    @classmethod
    def get_extra_actions(cls):
        return []