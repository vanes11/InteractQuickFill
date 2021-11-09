<template>
  <div id="app">
    <div id="gridElement" height='270px'  style="display:none;">
      <strong><u>Contruction des blocs</u></strong> 
        <div>
              <ul>
                  <li v-for="bloc in ListeOfBlocs" :key="bloc.messagetoprint">
                    {{ bloc.messagetoprint }} <!-- Gestion du menu contextuelle dans la grille -->
                  </li>
              </ul>
            </div>
                  <button @click="SendDataQuickFill">Send</button>
                  <button @click="BackTosheat">Back</button>
            <div>
        </div>

      <hr>

      <ejs-grid ref='grid' id='gridcomp' :allowSelection='true' :allowPaging='true' height='100%' :contextMenuItems='contextMenuItems' :contextMenuOpen='contextMenuOpen' :contextMenuClick='contextMenuClick'> </ejs-grid>
    </div>
    
    <div id="spreedsheetcomponent">


      <ejs-spreadsheet ref="spreadsheet" :created="created" :openUrl="openUrl" :allowHyperlink="false" :allowImage="false" :allowSorting="false" :allowFiltering="false" :contextMenuBeforeOpen="contextMenuBeforeOpen">
      </ejs-spreadsheet>

    </div>



      <div id="resultatcomponent"> <!-- Affichage des programmes -->
              <hr>
              <strong><u>Liste des programmes</u></strong>
              
              <div>
                    <p> nombre de programme (s) : <span v-for="item in lenofprogrammes.slice(0, 1)" :key="item.valuse"> {{ item.valuse }} </span> , le programme choisi est à  la position numéro : <span v-for="item in idporgramme.slice(0, 1)" :key="item.valuse"> {{ item.valuse }} </span>  </p>
                  </div>
                        <button @click="VueProgramChoix">Programme executé</button>
                  <div>
              </div> 
            <ejs-grid ref='grid2' id='gridcomprresult' :allowSelection='true' :allowPaging='true'  :row-data-bound='rowDataBound' :rowSelected='rowSelected' height='100%'>
            </ejs-grid>

    </div>

  </div>
</template>

<script>
  import Vue from "vue";
  import { SpreadsheetPlugin,getRangeAddress} from "@syncfusion/ej2-vue-spreadsheet";
  import { GridPlugin, ContextMenu, Page } from '@syncfusion/ej2-vue-grids';
  import axios from "axios";
  import VueSweetalert2 from 'vue-sweetalert2';





  Vue.use(SpreadsheetPlugin); 
  Vue.use(VueSweetalert2); /* pour la gestion des modals */
  Vue.use(GridPlugin);





  export default{
    name: 'App',
    data :  function(){  /* la fonction data retourne les variables dynamique (variables reactives) */
        return {


              idporgramme : [

              ], /* Le numero de programme choisi. */

              lenofprogrammes : [

              ], /* Nombre de programmes obtenues apres execution de flashfill ou quickfill */

              ElementToUpdate : 0,  /* variable de comptage des blocs: bvloc b1, b2 ..... */

              listeElementToupdate:[


              ], /* liste des evolution des id des blocs*/

              ChoiseQuickFill : {
                choix : 1
              }, /*permet de determiner quel variante de QuickFill utilisé */

              idsortieselectionner :{
                  id:1
              }, /* Identifier l'exemple sur lequel on cree le bloc*/

              IndiceColoneSortie:{
                  id:1
              },/*Contient le numero de la colone de sortie*/

              idColoneUtiliser:{

                id:0
              },/* Contient id de la colonne courrente */

              ListeDesProgrammesRetourner : [

              ], /* Contient la liste de programmes retourner par flashfill ou quickfilll */


              ListeElementsEnvoyerQuickFill:[



              ],  /* tableau contenant les donées (bloc de sortie + correspondance) à envoyer à QuickFill */


              ListeDesSortiesQuickFill:[



              ], /*Liste de toutes les sorties à envoyer à Quick Fill*/

              LesEntreeQuickFill :
              [


              ], /* tableau qui stocke les chaines d'entrée sigma de quickfill */
              

              ListeOfBlocs: 
              [


              ], /* contient les blocs de la chaine de sortie */


              contextMenuItems: 
              [
                  
                  {text: 'Make a bloc', target: '.e-content', id: 'makeblock'},
                  {text: 'Make a constant', target: '.e-content', id: 'makeconst'},
        
              ], /* Contient les items du menu contextuel de lq grid */


              ListeOfIdOfCotextMenu:
              [

              ], /* Contient les ids des nouveau items du menu contextuel crée par utilisation des item "make a bloc", "make a constant" */



              ListeMessagesOfCotextMenu:
              [

              ], /* Contient les messages des nouveau items du menu contextuel crée par utilisation des item "make a bloc", "make a constant" */


              listeSorties : 
              [


              ], /* tableau contenant les chaines de sorties s */

              listeEntres:
              [


              ], /* tableau contenant les chaines d'entrée sigma pour flashFill */

              IndiceDeLaColonneDeSortie:
              {

                id:1
              }, /* Contient indice de la colonne de sortie */

              openUrl: 'https://ej2services.syncfusion.com/production/web-services/api/spreadsheet/open',
              //saveUrl: 'https://ej2services.syncfusion.com/production/web-services/api/spreadsheet/save',
              
          
          };

    },

    methods: 
    {


      contextMenuOpen:function (args) 
      {

        var grid = document.getElementsByClassName("e-grid")[0].ej2_instances[0];
        var that =  this;
        var numeroIdColonne =  args.rowInfo.cellIndex;
        var numeroDeLigne = args.rowInfo.rowIndex;


        Vue.set(that.idColoneUtiliser,'id',numeroIdColonne);
        Vue.set(that.idsortieselectionner,'id', numeroDeLigne);



            if(numeroIdColonne == that.IndiceColoneSortie.id)
            {

                grid.contextMenuModule.contextMenu.showItems(['Make a bloc']);
                grid.contextMenuModule.contextMenu.showItems(['Make a constant']);

                if(that.ListeMessagesOfCotextMenu.length > 0)
                {
                        that.ListeMessagesOfCotextMenu.forEach(function (item) {
                            if((item.text != 'Make a bloc') && (item.text != 'Make a constant'))
                            {
                              grid.contextMenuModule.contextMenu.hideItems([item.text]);

                            }

                      });
                  }


            }
            else
            {
              grid.contextMenuModule.contextMenu.hideItems(['Make a bloc']);
              grid.contextMenuModule.contextMenu.hideItems(['Make a constant']);

              if(that.ListeMessagesOfCotextMenu.length > 0)
              {

                  that.ListeMessagesOfCotextMenu.forEach(function (item) {
                            if((item.text != 'Make a bloc') && (item.text != 'Make a constant') && (numeroDeLigne == item.idligne))
                            {

                              grid.contextMenuModule.contextMenu.showItems([item.text]);

                            }
                            else
                            {
                              grid.contextMenuModule.contextMenu.hideItems([item.text]);
                            }

                  });


              }



            }
          
      },


        rowSelected : function(args)
        {
          /* Gestion et affichage du programme choisi en interface. */
                var that = this;
                var index = args.data.ID;
                Vue.swal.fire({
                      title: '<strong><u>Programme ayant ID ' + index + '</u></strong>',
                      icon: 'info',
                      width: 400,
                      html:
                      '<p>' + that.ListeDesProgrammesRetourner[index] +'</p>' ,

                      showCloseButton: true,
                      showCancelButton: true,
                      focusConfirm: false,
                      confirmButtonText:
                      '<i class="fa fa-thumbs-up"></i> Great!',
                });

        },




        BackTosheat: function()
        {

            /*gestion du button retour */
            var that = this; 

            var spreedsheetcomponent = document.getElementById("spreedsheetcomponent");
            spreedsheetcomponent.style.display = "block";


            var gridElement = document.getElementById("gridElement");
            gridElement.style.display = "none"; 


            Object.assign(that.$data, that.$options.data());



        },

        VueProgramChoix: function() 
        {    
                /*Affichage du programme executé*/
                var that = this;
                var index = that.idporgramme.slice(0, 1);
                Vue.swal.fire({
                      title: '<strong><u>Programme executé</u></strong>',
                      icon: 'info',
                      width: 400,
                      html:
                      '<p>' + that.ListeDesProgrammesRetourner[index[0].valuse] +'</p>' ,

                      showCloseButton: true,
                      showCancelButton: true,
                      focusConfirm: false,
                      confirmButtonText:
                      '<i class="fa fa-thumbs-up"></i> Great!',
                });
        },

        SendDataQuickFill : function()
        {

              /*Envoie de données à QuickFill*/

              var that =  this;
              var listeofObjectElement =  new Array();
              var newObject = new Map();
              var grid2 = document.getElementsByClassName("e-grid")[1].ej2_instances[0];
              var resultcomponent = document.getElementById("resultatcomponent");
              


              if(that.ChoiseQuickFill.choix == 1)
              {

                  setTimeout(function cb() {


                        var jsonText1 = JSON.stringify(Array.from(that.listeEntres));
                        var jsonText3 = JSON.stringify(Array.from(that.ListeElementsEnvoyerQuickFill));

                        
                        
                        axios.post("http://localhost:8000/QuickFill/sessions/QuickExs", {

                        headers: {
                            'Content-Type': 'application/json',
                        },
                        data: {
                          
                          DataEntreeBrute : jsonText1, 
                          DataGlobal : jsonText3,

                        }
                      })
                      .then((response) => {



                              
                              var DataFinalToBeReplace = response.data["DataFinalToBeReplace"];
                              var IndiceColoneSortie = response.data["IndiceColoneSortie"];
                              var timewastQuickfill = response.data["timewastQuickfill"];
                              var memoryQuickfill = response.data["memoryQuickfill"];
                              var NombreExemples = response.data["NombreExemples"];
                              var listedesprogrammes = response.data["listedesprogrammes"];
                              var indiceduprogrammechoisi = response.data["indiceduprogrammechoisi"];
                              var AddElement =new Map();
                              var AddElement2 =new Map();
                              var Indiceline = 0;
                              var Arange= ""
                              var spreadsheet = that.$refs.spreadsheet;
                              
                              

                              that.listeSorties.forEach(function(item) {
                                  var newElement = new Array();
                                  Indiceline = parseInt(item.position);
                                  newElement.push(item.Output);
                                  Arange = getRangeAddress([Indiceline-1, IndiceColoneSortie-1])
                                  spreadsheet.updateCell({ value: newElement },Arange);

                              });


                              DataFinalToBeReplace.forEach(function(item) {
                                  var newElement = new Array();
                                  Indiceline = parseInt(item.position);
                                  newElement.push(item.Output);
                                  Arange = getRangeAddress([Indiceline-1, IndiceColoneSortie-1])
                                  spreadsheet.updateCell({ value: newElement },Arange);

                              });



                              var spreedsheetcomponent = document.getElementById("spreedsheetcomponent");
                              spreedsheetcomponent.style.display = "block";


                              var gridElement = document.getElementById("gridElement");
                              gridElement.style.display = "none"; 

                              Vue.swal.fire({
                                title: '<strong><u>Statistic of QuickFill execution</u></strong>',
                                icon: 'info',
                                width: 400,
                                html:
                                  '<p> execution time :' + timewastQuickfill + 's <br>' + 'Memory use :' + memoryQuickfill + 'Mo <br>' +'Number of programs :' +  NombreExemples + ' program(s)</p> ',

                                showCloseButton: true,
                                showCancelButton: true,
                                focusConfirm: false,
                                confirmButtonText:
                                  '<i class="fa fa-thumbs-up"></i> Great!',
                              });

                            
                              





                              

                            Object.assign(that.$data, that.$options.data());
                            
                            
                            AddElement.set('valuse',NombreExemples);
                            AddElement2.set('valuse',indiceduprogrammechoisi);

                            let obj = Array.from(AddElement).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});
                            let obj2 = Array.from(AddElement2).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});

                              Vue.set(that.lenofprogrammes,0, obj);
                              Vue.set(that.idporgramme,0, obj2);

                              listedesprogrammes.forEach((element,index) =>{
                                  

                              newObject.set('ID' , index)
                              newObject.set('programme' , element)
                              let obj3 = Array.from(newObject).reduce((obj, [key, value]) => (
                                              Object.assign(obj, { [key]: value })
                                            ), {});
                              listeofObjectElement.push(obj3)

                              Vue.set(that.ListeDesProgrammesRetourner, that.ListeDesProgrammesRetourner.length, element);

                            });

                            grid2.dataSource = listeofObjectElement;

                              
                            resultcomponent.style.display = "block";
                                    



                        
                        
                        
                      })
                      .catch((e) => {
                        console.log(e);
                      });
                  });




              }
              else if(that.ChoiseQuickFill.choix == 2)
              {




                  setTimeout(function cb() {

                        var jsonText1 = JSON.stringify(Array.from(that.listeEntres));
                        var jsonText3 = JSON.stringify(Array.from(that.ListeElementsEnvoyerQuickFill));
                        var jsonText4 = JSON.stringify(Array.from(that.listeSorties));
                        
                        axios.post("http://localhost:8000/QuickFill/filter/QuickExsFilter", {

                        headers: {
                            'Content-Type': 'application/json',
                        },
                        data: {
                          
                          DataEntreeBrute : jsonText1, 
                          DataGlobal : jsonText3,
                          MesSorties : jsonText4
                        }
                      })
                      .then((response) => {



                              
                              var DataFinalToBeReplace = response.data["DataFinalToBeReplace"];
                              var IndiceColoneSortie = response.data["IndiceColoneSortie"];
                              var timewastQuickfill = response.data["timewastQuickfill"];
                              var memoryQuickfill = response.data["memoryQuickfill"];
                              var NombreExemples = response.data["NombreExemples"];
                              var listedesprogrammes = response.data["listedesprogrammes"];
                              var indiceduprogrammechoisi = response.data["indiceduprogrammechoisi"];
                              var AddElement =new Map();
                              var AddElement2 =new Map();
                              var Indiceline = 0;
                              var Arange= ""
                              var spreadsheet = that.$refs.spreadsheet;
                              
                              

                              that.listeSorties.forEach(function(item) {
                                  var newElement = new Array();
                                  Indiceline = parseInt(item.position);
                                  newElement.push(item.Output);
                                  Arange = getRangeAddress([Indiceline-1, IndiceColoneSortie-1])
                                  spreadsheet.updateCell({ value: newElement },Arange);

                              });


                              DataFinalToBeReplace.forEach(function(item) {
                                  var newElement = new Array();
                                  Indiceline = parseInt(item.position);
                                  newElement.push(item.Output);
                                  Arange = getRangeAddress([Indiceline-1, IndiceColoneSortie-1])
                                  spreadsheet.updateCell({ value: newElement },Arange);

                              });



                              var spreedsheetcomponent = document.getElementById("spreedsheetcomponent");
                              spreedsheetcomponent.style.display = "block";


                              var gridElement = document.getElementById("gridElement");
                              gridElement.style.display = "none"; 

                              Vue.swal.fire({
                                title: '<strong><u>Statistic of QuickFill execution</u></strong>',
                                icon: 'info',
                                width: 400,
                                html:
                                  '<p> Time execution :' + timewastQuickfill + 's <br>' + 'Memory use :' + memoryQuickfill + 'Mo <br>' +'Number of programs :' +  NombreExemples + ' program(s)</p> ',

                                showCloseButton: true,
                                showCancelButton: true,
                                focusConfirm: false,
                                confirmButtonText:
                                  '<i class="fa fa-thumbs-up"></i> Great!',
                              });

                            
                              





                              

                            Object.assign(that.$data, that.$options.data());
                            
                            
                            AddElement.set('valuse',NombreExemples);
                            AddElement2.set('valuse',indiceduprogrammechoisi);

                            let obj = Array.from(AddElement).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});
                            let obj2 = Array.from(AddElement2).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});

                              Vue.set(that.lenofprogrammes,0, obj);
                              Vue.set(that.idporgramme,0, obj2);

                              listedesprogrammes.forEach((element,index) =>{
                                  

                              newObject.set('ID' , index)
                              newObject.set('programme' , element)
                              let obj3 = Array.from(newObject).reduce((obj, [key, value]) => (
                                              Object.assign(obj, { [key]: value })
                                            ), {});
                              listeofObjectElement.push(obj3)

                              Vue.set(that.ListeDesProgrammesRetourner, that.ListeDesProgrammesRetourner.length, element);

                            });

                            grid2.dataSource = listeofObjectElement;

                              
                            resultcomponent.style.display = "block";
                                    



                        
                        
                        
                      })
                      .catch((e) => {
                        console.log(e);
                      });
                  });

              }
              else if(that.ChoiseQuickFill.choix == 3)
              {





                  setTimeout(function cb() {


                        var jsonText1 = JSON.stringify(Array.from(that.listeEntres));
                        var jsonText3 = JSON.stringify(Array.from(that.ListeElementsEnvoyerQuickFill));
                        
                        axios.post("http://localhost:8000/QuickFill/manyblocs/QuickExsManyBlock", {

                        headers: {
                            'Content-Type': 'application/json',
                        },
                        data: {
                          
                          DataEntreeBrute : jsonText1, 
                          DataGlobal : jsonText3
                        }
                      })
                      .then((response) => {



                              
                              var DataFinalToBeReplace = response.data["DataFinalToBeReplace"];
                              var IndiceColoneSortie = response.data["IndiceColoneSortie"];
                              var timewastQuickfill = response.data["timewastQuickfill"];
                              var memoryQuickfill = response.data["memoryQuickfill"];
                              var NombreExemples = response.data["NombreExemples"];
                              var listedesprogrammes = response.data["listedesprogrammes"];
                              var indiceduprogrammechoisi = response.data["indiceduprogrammechoisi"];
                              var AddElement =new Map();
                              var AddElement2 =new Map();
                              var Indiceline = 0;
                              var Arange= ""
                              var spreadsheet = that.$refs.spreadsheet;
                              
                              
                              that.listeSorties.forEach(function(item) {
                                  var newElement = new Array();
                                  Indiceline = parseInt(item.position);
                                  newElement.push(item.Output);
                                  Arange = getRangeAddress([Indiceline-1, IndiceColoneSortie-1])
                                  spreadsheet.updateCell({ value: newElement },Arange);

                              });


                              DataFinalToBeReplace.forEach(function(item) {
                                  var newElement = new Array();
                                  Indiceline = parseInt(item.position);
                                  newElement.push(item.Output);
                                  Arange = getRangeAddress([Indiceline-1, IndiceColoneSortie-1])
                                  spreadsheet.updateCell({ value: newElement },Arange);

                              });



                              var spreedsheetcomponent = document.getElementById("spreedsheetcomponent");
                              spreedsheetcomponent.style.display = "block";


                              var gridElement = document.getElementById("gridElement");
                              gridElement.style.display = "none"; 

                              Vue.swal.fire({
                                title: '<strong><u>Statistic of QuickFill execution</u></strong>',
                                icon: 'info',
                                width: 400,
                                html:
                                  '<p> Time execution :' + timewastQuickfill + 's <br>' + 'Memory use :' + memoryQuickfill + 'Mo <br>' +'Number of programs :' +  NombreExemples + ' program(s)</p> ',

                                showCloseButton: true,
                                showCancelButton: true,
                                focusConfirm: false,
                                confirmButtonText:
                                  '<i class="fa fa-thumbs-up"></i> Great!',
                              });

                            
                              





                              

                            Object.assign(that.$data, that.$options.data());
                            
                            
                            AddElement.set('valuse',NombreExemples);
                            AddElement2.set('valuse',indiceduprogrammechoisi);

                            let obj = Array.from(AddElement).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});
                            let obj2 = Array.from(AddElement2).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});

                              Vue.set(that.lenofprogrammes,0, obj);
                              Vue.set(that.idporgramme,0, obj2);

                              listedesprogrammes.forEach((element,index) =>{
                                  

                              newObject.set('ID' , index)
                              newObject.set('programme' , element)
                              let obj3 = Array.from(newObject).reduce((obj, [key, value]) => (
                                              Object.assign(obj, { [key]: value })
                                            ), {});
                              listeofObjectElement.push(obj3)

                              Vue.set(that.ListeDesProgrammesRetourner, that.ListeDesProgrammesRetourner.length, element);

                            });

                            grid2.dataSource = listeofObjectElement;

                              
                            resultcomponent.style.display = "block";
                                    



                        
                        
                        
                      })
                      .catch((e) => {
                        console.log(e);
                      });
                  });

              }

 

        },
        contextMenuClick: function(args) 
        {


              var that = this;
              var grid = document.getElementsByClassName("e-grid")[0].ej2_instances[0];

              if(that.ChoiseQuickFill.choix == 3)
              {


                    if(args.item.id === 'makeblock') 
                    {       

                          
                            

                            document.execCommand("copy");

                            setTimeout(async () => 
                            {
                                  const text = await navigator.clipboard.readText();
                                  var AddBloc =new Map();
                                  var InfoBlocMenuDistingue = new Map();
                                  var AddtoContexMenu = new Map();
                                  var EtsPresent =  false;
                                  var idEstPresent = false;



                                 



                                  that.ListeOfIdOfCotextMenu.forEach(function (item) {

                                      
                                      if(item == text)
                                      {

                                          EtsPresent =  true;
                                      }
                                  });

                                  if(EtsPresent)
                                  {

                                    alert(' Bloc dejà creer')
                                  }
                                  else
                                  {
                                        


                                        that.listeElementToupdate.forEach(function (item,index) {
                                            if(index == parseInt(that.idsortieselectionner.id, 10))
                                            {
                                              idEstPresent = true;
                                            }
                                        });

                                        if(idEstPresent == false)
                                        {
                                              Vue.set(that.listeElementToupdate,parseInt(that.idsortieselectionner.id, 10), 1);
                                              


                                              AddBloc.set('message',text);
                                              AddBloc.set('messagetoprint',text + ' est un bloc');
                                              AddBloc.set('NameBloc','b'+that.listeElementToupdate[parseInt(that.idsortieselectionner.id, 10)]+'***'+text);

                                              AddtoContexMenu.set('text' , 'Contient le bloc ' + text);
                                              AddtoContexMenu.set('target' , '.e-content');
                                              AddtoContexMenu.set('id' , text);

                                              InfoBlocMenuDistingue.set('text' , 'Contient le bloc ' + text);
                                              InfoBlocMenuDistingue.set('idligne' , parseInt(that.idsortieselectionner.id, 10));

                                              let obj = Array.from(AddBloc).reduce((obj, [key, value]) => (
                                                                          Object.assign(obj, { [key]: value })
                                                                        ), {});
                                              let obj2 = Array.from(AddtoContexMenu).reduce((obj, [key, value]) => (
                                                                          Object.assign(obj, { [key]: value }) 
                                                                        ), {});
                                              
                                              let obj3 = Array.from(InfoBlocMenuDistingue).reduce((obj, [key, value]) => (
                                                                          Object.assign(obj, { [key]: value }) 
                                                                        ), {});

                                              grid.contextMenuModule.contextMenu.insertAfter( 
                                                  [obj2], that.contextMenuItems[that.contextMenuItems.length-1].id, true); 
                                            
                                              
                                              

                                              Vue.set(that.ListeOfBlocs,that.ListeOfBlocs.length, obj);
                                              Vue.set(that.ListeOfIdOfCotextMenu,that.ListeOfIdOfCotextMenu.length, text);
                                              Vue.set(that.ListeMessagesOfCotextMenu,that.ListeMessagesOfCotextMenu.length, obj3);
                                              


                                        }
                                        else
                                        {


                                             Vue.set(that.listeElementToupdate,parseInt(that.idsortieselectionner.id, 10), that.listeElementToupdate[parseInt(that.idsortieselectionner.id, 10)] + 1);

                                              AddBloc.set('message',text);
                                              AddBloc.set('messagetoprint',text + ' est un bloc');
                                              AddBloc.set('NameBloc','b'+that.listeElementToupdate[parseInt(that.idsortieselectionner.id, 10)]+'***'+text);

                                              AddtoContexMenu.set('text' , 'Contient le bloc ' + text);
                                              AddtoContexMenu.set('target' , '.e-content');
                                              AddtoContexMenu.set('id' , text);

                                              InfoBlocMenuDistingue.set('text' , 'Contient le bloc ' + text);
                                              InfoBlocMenuDistingue.set('idligne' , parseInt(that.idsortieselectionner.id, 10));

                                              let obj = Array.from(AddBloc).reduce((obj, [key, value]) => (
                                                                          Object.assign(obj, { [key]: value })
                                                                        ), {});
                                              let obj2 = Array.from(AddtoContexMenu).reduce((obj, [key, value]) => (
                                                                          Object.assign(obj, { [key]: value }) 
                                                                        ), {});
                                              
                                              let obj3 = Array.from(InfoBlocMenuDistingue).reduce((obj, [key, value]) => (
                                                                          Object.assign(obj, { [key]: value }) 
                                                                        ), {});

                                              grid.contextMenuModule.contextMenu.insertAfter( 
                                                  [obj2], that.contextMenuItems[that.contextMenuItems.length-1].id, true); 
                                            
                                              
                                              

                                              Vue.set(that.ListeOfBlocs,that.ListeOfBlocs.length, obj);
                                              Vue.set(that.ListeOfIdOfCotextMenu,that.ListeOfIdOfCotextMenu.length, text);
                                              Vue.set(that.ListeMessagesOfCotextMenu,that.ListeMessagesOfCotextMenu.length, obj3);



                                        }


                                  }

                            }, 200);
                        
                          
                    }
                    else if(args.item.id === 'makeconst')
                    {




                          document.execCommand("copy");

                            setTimeout(async () => 
                            {

                                  var AddBloc =new Map();
                                  var EtsPresent =  false;
                                  var element = new Map();
                                  var idEstPresent = false;

                                  const text = await navigator.clipboard.readText();

                                  that.ListeOfIdOfCotextMenu.forEach(function (item) {

                                          
                                          if(item == text)
                                          {

                                              EtsPresent =  true;
                                          }
                                      });

                                      if(EtsPresent)
                                      {

                                        alert(' Bloc deja creer')
                                      }
                                      else
                                      {
                                            that.listeElementToupdate.forEach(function (item,index) {
                                                if(index == parseInt(that.idsortieselectionner.id, 10))
                                                {
                                                  idEstPresent = true;
                                                }
                                            });
                                          if(idEstPresent == false)
                                          {                            
                                                Vue.set(that.listeElementToupdate,parseInt(that.idsortieselectionner.id, 10), 1);                
                                            
                                                
                                                
                                                element = new Map();

                                                AddBloc.set('message','Le bloc ' + text + ' est une  constante');
                                                AddBloc.set('messagetoprint','Le bloc ' + text + ' est une  constante');
                                                AddBloc.set('NameBloc','b'+that.listeElementToupdate[parseInt(that.idsortieselectionner.id, 10)]+'***'+text);

                                                  element.set('b'+that.listeElementToupdate[parseInt(that.idsortieselectionner.id, 10)]+'***'+text,"ConstStr");
                                                  element.set('Entrer' , that.listeSorties[parseInt(that.idsortieselectionner.id, 10)].Entrer);
                                                  element.set('Output' , that.listeSorties[parseInt(that.idsortieselectionner.id, 10)].Output);
                                                


                                                let obj = Array.from(AddBloc).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});
                                                let obj2 = Array.from(element).reduce((obj2, [key, value]) => (
                                                                              Object.assign(obj2, { [key]: value })
                                                                            ), {});


                                              
                                                Vue.set(that.ListeOfBlocs,that.ListeOfBlocs.length, obj);
                                                Vue.set(that.ListeElementsEnvoyerQuickFill, that.ListeElementsEnvoyerQuickFill.length, obj2);
                                          }
                                          else
                                          {


                                                    Vue.set(that.listeElementToupdate,parseInt(that.idsortieselectionner.id, 10), that.listeElementToupdate[parseInt(that.idsortieselectionner.id, 10)] + 1);
                                                
                                                    
                                                    
                                                    element = new Map();

                                                    AddBloc.set('message','Le bloc ' + text + ' est une  constante');
                                                    AddBloc.set('messagetoprint','Le bloc ' + text + ' est une  constante');
                                                    AddBloc.set('NameBloc','b'+that.listeElementToupdate[parseInt(that.idsortieselectionner.id, 10)]+'***'+text);

                                                      element.set('b'+that.listeElementToupdate[parseInt(that.idsortieselectionner.id, 10)]+'***'+text,"ConstStr");
                                                      element.set('Entrer' , that.listeSorties[parseInt(that.idsortieselectionner.id, 10)].Entrer);
                                                      element.set('Output' , that.listeSorties[parseInt(that.idsortieselectionner.id, 10)].Output);
                                                    


                                                    let obj = Array.from(AddBloc).reduce((obj, [key, value]) => (
                                                                                Object.assign(obj, { [key]: value })
                                                                              ), {});
                                                    let obj2 = Array.from(element).reduce((obj2, [key, value]) => (
                                                                                  Object.assign(obj2, { [key]: value })
                                                                                ), {});


                                                  
                                                    Vue.set(that.ListeOfBlocs,that.ListeOfBlocs.length, obj);
                                                    Vue.set(that.ListeElementsEnvoyerQuickFill, that.ListeElementsEnvoyerQuickFill.length, obj2);
                                          
                                          }
                                            




                                      }




                                
                                  
                            }, 200);

                    }
                    else if(that.ListeOfIdOfCotextMenu.some(e => e === args.item.id))
                    { 


                          document.execCommand("copy");
                         



                            setTimeout(async () => 
                            {

                                  const text = await navigator.clipboard.readText();

                                  that.ListeOfBlocs.forEach(function (item) {

                                      
                                      if(item.message == args.item.id)
                                      {

                                          var element = new Map();
                                          item.messagetoprint = item.message + " => " + text;

                                          element.set(item.NameBloc,text);
                                          
                                          element.set('Entrer' , that.listeSorties[parseInt(that.idsortieselectionner.id, 10)].Entrer);
                                          element.set('Output' , that.listeSorties[parseInt(that.idsortieselectionner.id, 10)].Output);
                                          console.log("test des test  : " , args.event.target);
                                          element.set('KeyOfElement' , "v" + (parseInt(that.idColoneUtiliser.id)+1));

                                          console.log("fffffffffffffffffffffffff : " , element);
                                          let obj = Array.from(element).reduce((obj, [key, value]) => (
                                                                      Object.assign(obj, { [key]: value })
                                                                    ), {});

                                          Vue.set(that.ListeElementsEnvoyerQuickFill, that.ListeElementsEnvoyerQuickFill.length, obj);

                                          
                                      }
                                  });

                                
                                  
                            }, 200);


                    




                    }



              }
              else
              {

              
                    if(args.item.id === 'makeblock') 
                    {       

                            
                            

                            document.execCommand("copy");

                            setTimeout(async () => 
                            {
                                  const text = await navigator.clipboard.readText();
                                  var AddBloc =new Map();
                                  var InfoBlocMenuDistingue = new Map();
                                  var AddtoContexMenu = new Map();
                                  var EtsPresent =  false;





                                  that.ListeOfIdOfCotextMenu.forEach(function (item) {

                                      
                                      if(item == text)
                                      {

                                          EtsPresent =  true;
                                      }
                                  });

                                  if(EtsPresent)
                                  {

                                    alert(' Bloc deja creer')
                                  }
                                  else
                                  {
                                        that.ElementToUpdate = that.ElementToUpdate +1 ;

                                        AddBloc.set('message',text);
                                        AddBloc.set('messagetoprint',text + ' est un bloc');
                                        AddBloc.set('NameBloc','b'+that.ElementToUpdate+'***'+text);
                                        InfoBlocMenuDistingue.set('text' , 'Contient le bloc ' + text);
                                        InfoBlocMenuDistingue.set('idligne' , parseInt(that.idsortieselectionner.id, 10));
                                        

                                        AddtoContexMenu.set('text' , 'Contient le bloc ' + text);
                                        AddtoContexMenu.set('target' , '.e-content');
                                        AddtoContexMenu.set('id' , text);

                                        let obj = Array.from(AddBloc).reduce((obj, [key, value]) => (
                                                                    Object.assign(obj, { [key]: value })
                                                                  ), {});
                                        let obj2 = Array.from(AddtoContexMenu).reduce((obj, [key, value]) => (
                                                                    Object.assign(obj, { [key]: value }) 
                                                                  ), {});
                                        
                                        let obj3 = Array.from(InfoBlocMenuDistingue).reduce((obj, [key, value]) => (
                                                                          Object.assign(obj, { [key]: value }) 
                                                                        ), {});

                                        grid.contextMenuModule.contextMenu.insertAfter( 
                                            [obj2], that.contextMenuItems[that.contextMenuItems.length-1].id, true); 
                                      
                                        
                                        

                                        Vue.set(that.ListeOfBlocs,that.ListeOfBlocs.length, obj);
                                        Vue.set(that.ListeOfIdOfCotextMenu,that.ListeOfIdOfCotextMenu.length, text);
                                        Vue.set(that.ListeMessagesOfCotextMenu,that.ListeMessagesOfCotextMenu.length, obj3);



                                  }

                            }, 200);
                        
                          
                    }
                    else if(args.item.id === 'makeconst')
                    {




                          document.execCommand("copy");

                            setTimeout(async () => 
                            {

                                  var AddBloc =new Map();
                                  var EtsPresent =  false;

                                  const text = await navigator.clipboard.readText();

                                  that.ListeOfIdOfCotextMenu.forEach(function (item) {

                                          
                                          if(item == text)
                                          {

                                              EtsPresent =  true;
                                          }
                                      });

                                      if(EtsPresent)
                                      {

                                        alert(' Bloc deja creer')
                                      }
                                      else
                                      {
                                        
                                        that.ElementToUpdate = that.ElementToUpdate +1 ;
                                        var element = new Map();

                                        AddBloc.set('message','Le bloc ' + text + ' est une  constante');
                                        AddBloc.set('messagetoprint','Le bloc ' + text + ' est une  constante');
                                        AddBloc.set('NameBloc','b'+that.ElementToUpdate+'***'+text);

                                          element.set('b'+that.ElementToUpdate+'***'+text,"ConstStr");
                                          element.set('Entrer' , that.listeSorties[0].Entrer);
                                          element.set('Output' , that.listeSorties[0].Output);
                                        


                                        let obj = Array.from(AddBloc).reduce((obj, [key, value]) => (
                                                                    Object.assign(obj, { [key]: value })
                                                                  ), {});
                                        let obj2 = Array.from(element).reduce((obj2, [key, value]) => (
                                                                      Object.assign(obj2, { [key]: value })
                                                                    ), {});


                                      
                                        Vue.set(that.ListeOfBlocs,that.ListeOfBlocs.length, obj);
                                        Vue.set(that.ListeElementsEnvoyerQuickFill, that.ListeElementsEnvoyerQuickFill.length, obj2);

                                        




                                      }




                                
                                  
                            }, 200);

                    }

                    else if(that.ListeOfIdOfCotextMenu.some(e => e === args.item.id))
                    {

                          document.execCommand("copy");





                            setTimeout(async () => 
                            {

                                  const text = await navigator.clipboard.readText();

                                  that.ListeOfBlocs.forEach(function (item) {



                                      
                                      if(item.message == args.item.id)
                                      {

                                         

                                         item.messagetoprint = item.message + " => " + text;
                                          var element = new Map();
                                          element.set(item.NameBloc,text);
                                          element.set('Entrer' , that.listeSorties[0].Entrer);
                                          element.set('Output' , that.listeSorties[0].Output);
                                          element.set('KeyOfElement' , "v" + (parseInt(that.idColoneUtiliser.id)+1));
                                           
                                          let obj = Array.from(element).reduce((obj, [key, value]) => (
                                                                      Object.assign(obj, { [key]: value })
                                                                    ), {});

                                          Vue.set(that.ListeElementsEnvoyerQuickFill, that.ListeElementsEnvoyerQuickFill.length, obj);

                                          
                                      }
                                  });

                                
                                  
                            }, 200);


                    




                    }


              }





        },
        contextMenuBeforeOpen: function () 
        {    
                var spreadsheet = this.$refs.spreadsheet;
                spreadsheet.removeContextMenuItems(['Paste Special'], false);
        },  /* Fonction qui s'execute avant l'ouverture du menu contextuel de la page d'accueil(spreadsheet) */
        rowDataBound: function (args) {
          
           var that = this;
           
           var index = JSON.parse(JSON.stringify(that.idporgramme.slice(0, 1)));

           
           if (args.data.ID == index[0].valuse)
           {
              
              args.row.style.backgroundColor = "MistyRose";
              //args.row.css("backgroundColor", "#F3C3C3");/*custom css applied to the row */
           }

               
   
       },
       created: function () 
       {
                    var that = this;  /* permet de manipuler les variables que retourne la fonction data */
                    var spreadsheet = that.$refs.spreadsheet;
                    var usedRange = 0;
                    var indicelignemax = 0;
                    var indicedecolenmax = 0;
                    var septsept = 0;
                    var sheetName = 0; /* nom de la feuille de calcul active */
                    var IndiceEvolue = 0; 
                    var ChainePlusTest = "";
                    var DataExpDemo =new Map(); /* Contient le jeu de données (entrée, sortie) */
                    var resultcomponent = document.getElementById("resultatcomponent"); /* Recupere la grille des resultats */
                    resultcomponent.style.display = "none";




                    spreadsheet.hideRibbonTabs(['Home' , 'Formulas' , 'Data','Insert' , 'View']); /* masque les elements pris en argument sur le ruban */
                    spreadsheet.addRibbonTabs([  /* ajout les nouveaux menu sur le ruban */
                          
                          { header: { text: 'GenerateResult' }, content: 
                            [
                              
                                  
                                /*{ text: 'FLashFill', tooltipText: 'FlashFill',
                                  click : function() {
                                    var resultcomponent = document.getElementById("resultatcomponent");
                                    resultcomponent.style.display = "none";

                                      indicedecolenmax = 0;
                                      indicedecolenmax = 0;
                                      septsept = 1;
                                      ChainePlusTest = "";
                                      DataExpDemo =new Map();
                                      usedRange = spreadsheet.ej2Instances.getActiveSheet().usedRange; //contient la plage activev(indice la derniere ligne, indice derniere colone)
                                      indicelignemax = usedRange.rowIndex;
                                      indicedecolenmax = usedRange.colIndex;
                                      sheetName = spreadsheet.ej2Instances.getActiveSheet().name;

                                      spreadsheet.ej2Instances.getData(sheetName + "!"+ getRangeAddress([0, 0, indicelignemax, indicedecolenmax])).then( (cells)=> // recupere les données de la plage active et effetue un traitement popur chaque cellule
                                      {

                                              cells.forEach((cell)=>{ // cells contient l'ensemble de toutes les cellules

                                                if(IndiceEvolue == indicedecolenmax) // IndiceEvolue permet de parcourir les colones 
                                                {
                                                  
                                                    // Recuperation de la chaine de sortie s : elle peut etre vide ou non
                                                    ChainePlusTest = ChainePlusTest.substring(0, ChainePlusTest.length-3) // on surpime la derniere chaine "+++" 

                                                    if(typeof(cell.value) == "undefined")
                                                    {
                                                      DataExpDemo = DataExpDemo.set(septsept.toString()+'***'+'' , ChainePlusTest);
                                                      //septsept contient l'indice de la ligne en cours de traitement

                                                    }
                                                    else
                                                    {
                                                      DataExpDemo = DataExpDemo.set(septsept.toString()+'***'+cell.value,ChainePlusTest);
                                                      // DataExpDemo est un dico qui contient les exemple d'entree sortie , stockés sur une certaine forme prenqnt en compte le numero de ligne de chaque exp 
                                                    }
                                                    
                                                    ChainePlusTest = '';
                                                    IndiceEvolue = 0;
                                                    septsept = septsept + 1;
                                                }
                                                else
                                                {
                                                    // cette partie nous permet de recuperer la chaine d'entrée sigma. La recuperation se fait tant qu'on a pa atteint la deniere colone active.
                                                    if(typeof(cell.value) != "undefined")
                                                    {
                                                      ChainePlusTest = ChainePlusTest + cell.value + "+++"; 
                                                      IndiceEvolue = IndiceEvolue + 1;
                                                    }

                                                }

                                              });
            
                                          });

                                      setTimeout(function cb() {  // setTimeout indique que lq fonction cb() doit s'executer en derniere position 


                                          var jsonText = JSON.stringify(Array.from(DataExpDemo.entries()));
                                          
                                          axios.post("http://localhost:8000/FlashFill/sessions/FlashExs", {

                                          headers: {  // headers permet de definir le type de contenu qu'on veut envoyer : p il s'agit d'un contenu json dans notre cas 
                                              'Content-Type': 'application/json',
                                          },
                                          data: {
                                            
                                            DataEntree : jsonText  // DataEntree stocke nos donées json , qui sont ensuite traitées  au niveau du backend
                                          }
                                        })
                                        .then((response) => {



                                          if(response.data["MessageCles"] == "False")
                                          {
                                              Vue.swal.fire({
                                                    icon: 'error',
                                                    title: 'Oops...',
                                                    text: 'FlashFill Do not understant what you want!',
                                                    footer: '<p>It can be a condition execution problem : <br> Condition for good execution : <br> <ol><li>Your data most have the same structure</li><li>You most have a least one exemple with a output</li></ol><br></p>'
                                                  });

                                          }
                                          else
                                          {
                                              
                                                var DataFinalToBeReplace = response.data["DataFinalToBeReplace"];
                                                var IndiceColoneSortie = response.data["IndiceColoneSortie"];
                                                var timewastFlasfill = response.data["timewastFlasfill"];
                                                var NombreExemples = response.data["NombreExemples"];
                                                var memoryFlasfill = response.data["memoryFlasfill"];
                                                var Indiceline = 0;
                                                var Arange= ""
                                                


                                                Object.keys(DataFinalToBeReplace).forEach(function(prop) {
                                                  
                                                  Indiceline = parseInt(prop);
                                                  Arange = getRangeAddress([Indiceline-1, IndiceColoneSortie])
                                                  Arange = Arange.toString().split(":")[0]
                                                  spreadsheet.updateCell({ value: DataFinalToBeReplace[prop] },Arange);
                                                  
                                                }); 



                                                  Vue.swal.fire({
                                                    title: '<strong><u>Statistic of FlashFill execution</u></strong>',
                                                    icon: 'info',
                                                    width: 400,
                                                    html:
                                                      '<p> Time execution :' + timewastFlasfill + 's <br>' + 'Number of programmes :' + 'Memory use :' + memoryFlasfill + 'Mo <br>' + NombreExemples + ' programme(s)</p> ',

                                                    showCloseButton: true,
                                                    showCancelButton: true,
                                                    focusConfirm: false,
                                                    confirmButtonText:
                                                      '<i class="fa fa-thumbs-up"></i> Great!',
                                                  });
                                      
                                                



                                          }
                                          
                                          
                                        
                                        })
                                        .catch((e) => {
                                          console.log(e);
                                        });
                                      });

                                } },*/
                                
                                
                                { text: 'QuickFill', tooltipText: 'QuickFill',
                                click : function() 
                                {








                                              indicedecolenmax = 0;
                                              indicedecolenmax = 0;
                                              septsept = 1;
                                              ChainePlusTest = "";
                                              DataExpDemo =new Map();
                                              usedRange = spreadsheet.ej2Instances.getActiveSheet().usedRange;
                                              indicelignemax = usedRange.rowIndex;
                                              indicedecolenmax = usedRange.colIndex;
                                              Vue.set(that.IndiceColoneSortie , 'id' , indicedecolenmax);
                                              sheetName = spreadsheet.ej2Instances.getActiveSheet().name;

                                                        
                                              var grid = document.getElementsByClassName("e-grid")[0].ej2_instances[0]; // recuperation de la Grid
                                              var Initializer = new Array();


                                              var ElementMapInstanceEntree =  new Map();
                                              var ElementIntermediareMapInstanceEntree =  new Map();
                                              var ElementMapInstanceSortie =  new Map();
                                              var ElementMapInstanceSortie2 =  new Map();
                                              var listechoix = new Array();
                                              var decoupersortier = new Array();
                                              var decouperentree = new Array();
                                              var MessageCles = true;
                                              var resultcomponent = document.getElementById("resultatcomponent");
                                              resultcomponent.style.display = "none";

                                              grid.dataSource = Initializer;
                                              grid.columns = Initializer;

                                              spreadsheet.ej2Instances.getData(sheetName + "!"+ getRangeAddress([0, 0, indicelignemax, indicedecolenmax])).then( (cells)=>
                                              {

                                                    cells.forEach((cell)=>{

                                                      if(IndiceEvolue == indicedecolenmax)
                                                      {
                                                        
                                                        
                                                          ChainePlusTest = ChainePlusTest.substring(0, ChainePlusTest.length-3)

                                                          if(typeof(cell.value) == "undefined")
                                                          {
                                                              DataExpDemo.set(septsept.toString()+'***'+'' , ChainePlusTest);

                                                          }
                                                          else
                                                          {
                                                              DataExpDemo.set(septsept.toString()+'***'+cell.value, ChainePlusTest);
                                                          }
                                                          
                                                          ChainePlusTest = '';
                                                          IndiceEvolue = 0;
                                                          septsept = septsept + 1;
                                                      }
                                                      else
                                                      {
                                                          
                                                          if(typeof(cell.value) != "undefined")
                                                          {
                                                            ChainePlusTest = ChainePlusTest + cell.value + "+++"; 
                                                            IndiceEvolue = IndiceEvolue + 1;
                                                          }

                                                      }

                                                    });
          
                                              });

                                              setTimeout(function cb() {

                                                        
                                                        DataExpDemo.forEach((value, key) => {
                                                          
                                                          if(value === "")
                                                          {

                                                              Vue.swal.fire({
                                                                  icon: 'error',
                                                                  title: 'Oops...',
                                                                  text: 'QuickFill Do not understant what you want!',
                                                                  footer: '<p>It can be a condition execution problem : <br> Condition for good execution : <br> <ol><li>Your data most have the same structure</li><li>You most have a least one exemple with a output</li></ol><br></p>'
                                                                });


                                                              MessageCles = false;

                                                              return;

                                                          }
                                                          else
                                                          {


                                                                    ElementMapInstanceEntree = new Map();
                                                                    ElementMapInstanceSortie = new Map();
                                                                    ElementMapInstanceSortie2 = new Map();
                                                                    ElementIntermediareMapInstanceEntree =  new Map();
                                                                    decouperentree = value.split("+++");
                                                                    decoupersortier = key.split("***");
                                                                    
                                                                    

                                                                    if(decoupersortier.length >1 && decoupersortier[1] != "")
                                                                    {

                                                                        if(value != "")
                                                                        {

                                                                            decouperentree.forEach(function (item, index) {
                                                                              ElementIntermediareMapInstanceEntree.set("v"+(index+1).toString(), item);
                                                                              ElementMapInstanceSortie.set("v"+(index+1).toString(), item);
                                                                              
                                                                            });


                                                                            let obj = Array.from(ElementIntermediareMapInstanceEntree).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});


                                                                            ElementMapInstanceSortie2.set("Entrer" , obj);
                                                                            ElementMapInstanceSortie.set("Output" , decoupersortier[1]);
                                                                            ElementMapInstanceSortie2.set("Output" , decoupersortier[1]);
                                                                            ElementMapInstanceSortie2.set("position" , decoupersortier[0]);

                                                                            listechoix.push(ElementMapInstanceSortie);

                                                                            let obj2 = Array.from(ElementMapInstanceSortie2).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});


                                                                            Vue.set(that.listeSorties,that.listeSorties.length,obj2)

                                                                        }



                                                                    }
                                                                    else
                                                                    {

                                                                          if(value != "")
                                                                          {
                                                                            decouperentree.forEach(function (item, index) {
                                                                              ElementIntermediareMapInstanceEntree.set("v"+(index+1).toString(), item);
                                                                            });
                                                                            let obj = Array.from(ElementIntermediareMapInstanceEntree).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});
                                                                            ElementMapInstanceEntree.set("Entrer" , obj);
                                                                            ElementMapInstanceEntree.set("position" , decoupersortier[0]);
                                                                            let obj2 = Array.from(ElementMapInstanceEntree).reduce((obj, [key, value]) => (
                                                                            Object.assign(obj, { [key]: value })
                                                                          ), {});
                                                                            Vue.set(that.listeEntres ,that.listeEntres.length,obj2)
                                                                            
                                                                          }
                                                                          

                                                                    }


                                                          }

                                                        });





                                                          if(MessageCles)
                                                          {

                                                            if(listechoix.length == 1)
                                                            {


                                                                    setTimeout(function knr() {


                                                                                if(MessageCles)
                                                                                {

                                                                                      var test2 = new Array();
                                                                                    
                                                                                      
                                                                                      var sortieUtiliser = listechoix[0];
                                                                                      

                                                                                        let obj = Array.from(sortieUtiliser).reduce((obj, [key, value]) => (
                                                                                                  Object.assign(obj, { [key]: value }) // Be careful! Maps can have non-String keys; object literals can't.
                                                                                                ), {});
                                                                                      
                                                                                        test2.push(obj);                                                  
                                                                                                                                        
                                                                                        grid.dataSource = test2;

                                                                                        var spreedsheetcomponent = document.getElementById("spreedsheetcomponent");
                                                                                        spreedsheetcomponent.style.display = "none";


                                                                                        var gridElement = document.getElementById("gridElement");
                                                                                        gridElement.style.display = "block"; 
                                                                                }
                                                                    });
                                                              
                                                            }
                                                            else
                                                            {

                                                                Vue.swal.fire({
                                                                      title: 'Que desirer vous faire avec QuickFIll',
                                                                      html: `
                                                                                <div class="form-check">
                                                                                  <input class="form-check-input" type="radio" name="exampleRadios" id="exampleRadios1" value="option1" checked>
                                                                                  <label class="form-check-label" for="exampleRadios1">
                                                                                      Faire du filtrage
                                                                                  </label>
                                                                                </div>
                                                                                <div class="form-check">
                                                                                  <input class="form-check-input" type="radio" name="exampleRadios" id="exampleRadios2" value="option2">
                                                                                  <label class="form-check-label" for="exampleRadios2">
                                                                                    Faire des blocs sur pluiseurs exemples
                                                                                  </label>
                                                                                </div>
                                                                      `,
                                                                      focusConfirm: false,
                                                                      preConfirm: () => 
                                                                      {
                                                                        
                                                                            if (document.getElementById('exampleRadios1').checked)
                                                                            {
                                                                                  setTimeout(function knr() {


                                                                                                if(MessageCles)
                                                                                                {
                                                                                                    
                                                                                                      var test2 = new Array();
                                                                                                    
                                                                                                      
                                                                                                      var sortieUtiliser = listechoix[0];

                                                                                                      

                                                                                                      let obj = Array.from(sortieUtiliser).reduce((obj, [key, value]) => (
                                                                                                                  Object.assign(obj, { [key]: value }) // Be careful! Maps can have non-String keys; object literals can't.
                                                                                                                ), {});
                                                                                                      
                                                                                                      test2.push(obj);                                                  
                                                                                                                                                        
                                                                                                      grid.dataSource = test2;

                                                                                                      var spreedsheetcomponent = document.getElementById("spreedsheetcomponent");
                                                                                                      spreedsheetcomponent.style.display = "none";


                                                                                                      var gridElement = document.getElementById("gridElement");
                                                                                                      gridElement.style.display = "block"; 

                                                                                                      Vue.set(that.ChoiseQuickFill, 'choix' , 2);
                                                                                                }
                                                                                    });

                                                                            }
                                                                            else if(document.getElementById('exampleRadios2').checked)
                                                                            {
                                                                                

                                                                                    setTimeout(function knr2() {


                                                                                                if(MessageCles)
                                                                                                {

                                                                                                      var test2 = new Array();
                                                                                                      listechoix.forEach(function (item) 
                                                                                                      {
                                                                                                        let obj = Array.from(item).reduce((obj, [key, value]) => (
                                                                                                                  Object.assign(obj, { [key]: value }) // Be careful! Maps can have non-String keys; object literals can't.
                                                                                                                ), {});
                                                                                                        test2.push(obj);
                                                                                                      });
                                                
                                                                                                      grid.dataSource = test2;

                                                                                                      var spreedsheetcomponent = document.getElementById("spreedsheetcomponent");
                                                                                                      spreedsheetcomponent.style.display = "none";


                                                                                                      var gridElement = document.getElementById("gridElement");
                                                                                                      gridElement.style.display = "block"; 



                                                                                                      Vue.set(that.ChoiseQuickFill, 'choix' , 3);
                                                                                                }
                                                                                    });
                                                                            
                                                                            
                                                                            

                                                                            }
                                                                          
                                                                        
                                                                      }
                                                                  });




                                                            }




                                                          }

                                                                              

                                                    });








                                } } ,



                                { text: 'FLashFillL (simplified)', tooltipText: 'FLashFill (simplified)',
                                click : function() {

                                    indicedecolenmax = 0;
                                    indicedecolenmax = 0;
                                    septsept = 1;
                                    ChainePlusTest = "";
                                    DataExpDemo =new Map();
                                    var AddElement =new Map();
                                    var AddElement2 =new Map();
                                    var listeofObjectElement =  new Array();
                                    usedRange = spreadsheet.ej2Instances.getActiveSheet().usedRange;
                                    indicelignemax = usedRange.rowIndex;
                                    indicedecolenmax = usedRange.colIndex;
                                    sheetName = spreadsheet.ej2Instances.getActiveSheet().name;
                                    var resultcomponent = document.getElementById("resultatcomponent");
                                    resultcomponent.style.display = "none";

                                    spreadsheet.ej2Instances.getData(sheetName + "!"+ getRangeAddress([0, 0, indicelignemax, indicedecolenmax])).then( (cells)=>
                                    {

                                          

                                            cells.forEach((cell)=>{

                                              if(IndiceEvolue == indicedecolenmax)
                                              {
                                                
                                                
                                                  ChainePlusTest = ChainePlusTest.substring(0, ChainePlusTest.length-3)

                                                  if(typeof(cell.value) == "undefined")
                                                  {
                                                    DataExpDemo = DataExpDemo.set(septsept.toString()+'***'+'' , ChainePlusTest);

                                                  }
                                                  else
                                                  {
                                                    DataExpDemo = DataExpDemo.set(septsept.toString()+'***'+cell.value,ChainePlusTest);
                                                  }
                                                  
                                                  ChainePlusTest = '';
                                                  IndiceEvolue = 0;
                                                  septsept = septsept + 1;
                                              }
                                              else
                                              {
                                                  
                                                  if(typeof(cell.value) != "undefined")
                                                  {
                                                    ChainePlusTest = ChainePlusTest + cell.value + "+++"; 
                                                    IndiceEvolue = IndiceEvolue + 1;
                                                  }

                                              }

                                            });
          
                                        });

                                    setTimeout(function cb() {


                                        var jsonText = JSON.stringify(Array.from(DataExpDemo.entries()));
                                        
                                        axios.post("http://localhost:8000/FlashFill/sessions/FlashFreeLoopExs", {

                                        headers: {
                                            'Content-Type': 'application/json',
                                        },
                                        data: {
                                          
                                          DataEntree : jsonText
                                        }
                                      })
                                      .then((response) => {



                                        if(response.data["MessageCles"] == "False")
                                        {
                                            Vue.swal.fire({
                                                  icon: 'error',
                                                  title: 'Oops...',
                                                  text: 'FlashFill Do not understant what you want!',
                                                  footer: '<p>It can be a condition execution problem : <br> Condition for good execution : <br> <ol><li>Your data most have the same structure</li><li>You most have a least one exemple with a output</li></ol><br></p>'
                                                });

                                        }
                                        else
                                        {

                                            
                                              var DataFinalToBeReplace = response.data["DataFinalToBeReplace"];

                                              
                                              var IndiceColoneSortie = response.data["IndiceColoneSortie"];
                                              var timewastFlasfill = response.data["timewastFlasfill"];
                                              var NombreExemples = response.data["NombreExemples"];
                                              var memoryFlasfill = response.data["memoryFlasfill"];
                                              var listedesprogrammes = response.data["listedesprogrammes"];
                                              var indiceduprogrammechoisi = response.data["indiceduprogrammechoisi"];
                                              var Indiceline = 0;
                                              var Arange= "";
                                              var newObject = new Map();
                                              var grid2 = document.getElementsByClassName("e-grid")[1].ej2_instances[0];
                                              AddElement.set('valuse',NombreExemples);
                                              AddElement2.set('valuse',indiceduprogrammechoisi);

                                              

                                              Object.keys(DataFinalToBeReplace).forEach(function(prop) {
                                                
                                                Indiceline = parseInt(prop);
                                                Arange = getRangeAddress([Indiceline-1, IndiceColoneSortie])
                                                Arange = Arange.toString().split(":")[0]
                                                spreadsheet.updateCell({ value: DataFinalToBeReplace[prop] },Arange);
                                                
                                              }); 

                                                
                                              


                                               
                                                

                                                Vue.swal.fire({
                                                  title: '<strong><u>Statistic of FlashFill (simplified) execution</u></strong>',
                                                  icon: 'info',
                                                  width: 400,
                                                  html:
                                                    '<p> Execution time:' + timewastFlasfill + 's <br>' + 'Number of programs :' +NombreExemples + ' program(s)<br>'+ 'Memory use :' + memoryFlasfill + 'Mo</p>' ,

                                                  showCloseButton: true,
                                                  showCancelButton: true,
                                                  focusConfirm: false,
                                                  confirmButtonText:
                                                    '<i class="fa fa-thumbs-up"></i> Great!',
                                                });

                                                
                                            
                                              let obj = Array.from(AddElement).reduce((obj, [key, value]) => (
                                                                    Object.assign(obj, { [key]: value })
                                                                  ), {});
                                              let obj2 = Array.from(AddElement2).reduce((obj, [key, value]) => (
                                                                    Object.assign(obj, { [key]: value })
                                                                  ), {});
                                              
                                              Object.assign(that.$data, that.$options.data());
                                              Vue.set(that.lenofprogrammes,0, obj);
                                              Vue.set(that.idporgramme,0, obj2);
                                              listedesprogrammes.forEach((element,index) =>{
                                                  

                                                    newObject.set('ID' , index)
                                                    newObject.set('programme' , element)
                                                    let obj3 = Array.from(newObject).reduce((obj, [key, value]) => (
                                                                    Object.assign(obj, { [key]: value })
                                                                  ), {});
                                                    listeofObjectElement.push(obj3)

                                                    Vue.set(that.ListeDesProgrammesRetourner, that.ListeDesProgrammesRetourner.length, element);

                                                    




                                              });
                                              grid2.dataSource = listeofObjectElement;

                                              var resultcomponent = document.getElementById("resultatcomponent");
                                              resultcomponent.style.display = "block";
                                    
                                              



                                        }
                                        
                                        
                                      
                                      })
                                      .catch((e) => {
                                        console.log(e);
                                      });
                                    });

                                } },





                            ] 
                            
                          
                          
                          
                          
                          }
                          
                          
                          ,{ header: { text: 'Help' }, content: [{ text: 'QuickFill', tooltipText: 'QuickFill',
                          click : function() {

                                Vue.swal.fire({
                                      title: '<strong><u>QuicFill Usage example</u></strong>',
                                      icon: 'info',
                                      width: 900,
                                      html:
                                        '<iframe width="560" height="315" src="https://www.youtube.com/embed/d_elXY2Lcfk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                                      showCloseButton: true, /* pour la fermeture du modal */
                                      showCancelButton: true, /* bouton cancel */
                                      focusConfirm: false,
                                      confirmButtonText:
                                        '<i class="fa fa-thumbs-up"></i> Great!',
                                    });


                          } },
                          
                          
                          { text: 'FlashFill', tooltipText: 'FlashFill',
                          click : function() {


                              Vue.swal.fire({
                                      title: '<strong><u>FlashFill Usage example</u></strong>',
                                      icon: 'info',
                                      width: 900,
                                      html:
                                        '<iframe width="768" height="360" src="https://www.youtube.com/embed/A7-E6sf6JOc?list=RDQMuK_M4fl3Ds8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                                      showCloseButton: true,
                                      showCancelButton: true,
                                      focusConfirm: false,
                                      confirmButtonText:
                                        '<i class="fa fa-thumbs-up"></i> Great!',
                                    });

                          } },
                          
                          { text: 'About', tooltipText: 'About',
                          click : function() {


                              Vue.swal.fire({
                                      title: '<strong>About the project</strong>',
                                      icon: 'info',
                                      width: 900,
                                      html:
                                        '<p>QuicFill project is a project developper by Fokou Vanessa Laure (adress mail) base on the FlashFill algorithme  to test a idea of and iteractive approche using independant bloc approche to generate string progamme base on example</p>',
                                      showCloseButton: true,
                                      showCancelButton: true,
                                      focusConfirm: false,
                                      confirmButtonText:
                                        '<i class="fa fa-thumbs-up"></i> Great!',
                                    });
                          } },
                          
                          ] }]
                      );
                        
                
            },
      
        },




    provide: /* defintion des elements presentes dans la grille */
    { 
      grid: [ContextMenu, Page], 
    }, 



  }
</script>

<style>
  @import "../node_modules/@syncfusion/ej2-vue-spreadsheet/styles/material.css";
  @import '../node_modules/@syncfusion/ej2-base/styles/material.css';  
  @import '../node_modules/@syncfusion/ej2-buttons/styles/material.css';
  @import '../node_modules/@syncfusion/ej2-calendars/styles/material.css';    
  @import '../node_modules/@syncfusion/ej2-dropdowns/styles/material.css';  
  @import '../node_modules/@syncfusion/ej2-inputs/styles/material.css';  
  @import '../node_modules/@syncfusion/ej2-navigations/styles/material.css';
  @import '../node_modules/@syncfusion/ej2-popups/styles/material.css';
  @import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css';
  @import '../node_modules/@syncfusion/ej2-grids/styles/material.css';
  @import "../node_modules/@syncfusion/ej2-spreadsheet/styles/material.css";
  @import "../node_modules/sweetalert2/dist/sweetalert2.min.css";
  @import "../node_modules/@syncfusion/ej2-vue-grids/styles/material.css";
</style>
