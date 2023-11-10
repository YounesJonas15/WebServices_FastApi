## WebServices

### Exécution du programme :

1. Lancez tous les serveurs et le listener du répertoire.
2. Lancez l'application cliente.
3. Une interface graphique s'affichera pour permettre la saisie des informations.

Pour une exécution correcte sans erreur, assurez-vous que le client existe dans la base de données `banque.json` et que les informations sur les biens immobiliers se trouvent dans la base de données `ventes_recentes`.

Exemples de clients :

1. Nom : "Amrane"
   Prénom : "Younes"
   Email : "younesamrane01@gmail.com" 
   Ville : "Lyon"
   Type : "appartement"
   Nombre de pièces : 3

2. Nom : "Maziz"
   Prénom : "Yassine"
   Email : "mazizBg@kakachi.com"
   Ville : "Velizy"
   Type : "maison"
   Nombre de pièces : 4

La réponse sera envoyée par email. Veuillez mettre votre propre adresse email dans l'un de ces exemples et n'oubliez pas de la modifier également dans `banque.json`.
Sinon vous pouvez voir le résultat directement dans le répertoire "ResultatDemandes"
 
NB :Assurez-vous qu'aucune demande portant le même nom et prénom n'existe déjà dans le répertoire "demandes" avant l'exécution, sinon le listener ne pourra pas la détecter.  