# InteractQuickFill
InteractQuickFill est une implémentation de deux algorithmes de synthèse de programmes (FlashFill (simplified), QuickFill) avec  une interface associée.
Ces algorithmes prennent en entrée  un ensemble  d’exemples de couples (entrée, sortie) et retourne des programmes (dans un DSL de manipulation des chaînes de caractères) P tel que P(entrée) = sortie pour chaque couple (entrée, sortie).

- FlashFill (simplified) une version simplifiée de l'algorithme FlashFill existant.

- QuickFill est approche d’implémentation de FlashFill qui vise à élaguer l'espace de programmes de ce dernier. En effet, FlashFill explore un grand espace de programmes.
L’intuition de QuickFill est que si l’utilisateur affine les spécifications (exemple entrée-sortie) en faisant des associations entre les sous-parties de la sortie et de l'entrée, ceci permettra de réduire l’espace de programmes de FlashFill. Dans certains cas, ceci permettra de réduire le nombre d’exemples entrée-sortie et par conséquent le temps d'exécution et l’utilisation mémoire. 
 
-> Installation sur unbuntu

Installation de pip3,python3, nodejs et npm : 

- sudo apt update
- sudo apt install python3-pip python3
- sudo apt install nodejs npm

- Se deplacer vers le dossier frontend et exécuter la commande : npm install
- Se deplacer dans le dossier backend et exécuter la commande : pip3 install -r requirements.txt

-> Exectution : lancer les serveurs du frontend et du backend dans deux consoles differentes.

- Se deplacer dans le dossier backend et exécuter la commande : python3 manage.py runserver
- Se deplacer dans le dossier frontend et exécuter la commande : npm run serve
- Cliquer sur le lien de la forme : http://localhost:8080/ 


Voir video suivante https://youtu.be/I9TW8AsSpRQ pour la démo sur l’utilisation de l’interface.






