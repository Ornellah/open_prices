# **Remarques**
    
## **Compréhension des données**
     
Lors de la pré-analyse des variables catégorielles et numériques, il a été remarqué que certaines colonnes de type `object` était en fait des listes (`list`).<br>
Les listes empêchent d'utiliser les fonctions "nunique" et "unique" sur ces dernières.<br>
La solution a été de créer une fonction qui détecte et transforme les colonnes de type `list` en colonnes de type `string` (chaîne de charactères).<br>
    
Il n'y a pas d'analyse sur la corrélation catégorielle car le dataset contient 29 variables catégorielles.<br>
Or les tests de khi-deux et le V de Cramer ne sont utilisables que sur 2 variables à la fois (une seule corrélation étudiable à chaque fois).<br>
Le fait de devoir refaire un test entre chaque variable coûte trop de ressources donc il a été décidé de ne voir/faire aucune corrélation catégorielle.<br>
     
Il n'y a pas d'analyse temporelle pour la même raison qu'il n'y en a pas pour l'analyse catégorielle.<br>
Les test de Dickey-Fuller et ARIMA ne sont utilisables que sur une seule série temporelle à chaque fois (1 variable temporelle + 1 variable) donc les ressources consommées sont beaucoup trop élevées par rapport aux gains.<br>
     
Il n'y a pas d'analyse géographique car représenter visuellement (notamment avec Folium et GeoPy) des lieux consomment beaucoup trop de ressources.<br>   
     
## **Préparation des données**   
     
Les colonnes `location_website_url` et `location_source` ont été supprimées car elles ne contenaient que des valeurs nulles (manquantes).<br>
     
Aucun remplacement de valeurs n'a été prévu car même les valeurs nulles apportent des informations.<br>
      
Les colonnes avec une majorité (pas une entièreté) de nulles doivent être gardées car le peut d'information contenue peut être essentielle pour comprendre un enregistrement (une ligne).<br>
     
La colonne `origins_tags` est un doublon en terme d'information de la colonne `location_osm_address_country` en moins complet (plus de valeurs nulles).<br>
   
Les colonnes `proof_source` et `source` contiennent les mêmes informations (même nombre de lignes) donc une des deux a été supprimée (proof_source) pour éviter la redondance.<br>
  
Les colonnes `proof_created`, `proof_updated`, `location_id`, `proof_file_path`, `proof_mimetype`, `location_created` et `location_updated` ont été supprimées car elles ne sont pas utilisées.<br>
  
Les lignes qui avaient les colonnes `product_name` et `category_tag` vides ont été supprimées.<br>

La regex `[a-z]{2}:` a été utilisée sur la colonne `category_tag` pour enlever la partie `en:` présente au début de chaque valeur non nulle.      
Exemple :     
valeur initiale = `en:broccoli`
valeur après changement = `broccoli`

La regex `^\[\'\w{2}:(\w+)\']$` a été utilisée sur la colonne `labels_tag` pour enlever la partie `['en:{...}']` en isolant l'information qui avait de l'importance ici représentée par `{...}`.    
Exemple :    
valeur initiale = `['en:organic']`  
valeur après changement = `organic`  

Un split a été appliquée sur la colonne `location_osm_display_name` pour créer une nouvelle colonne nommée `store_name` qui contient le nom des magasins.   
La colonne `location_osm_display_name` a été supprimée par la suite car toutes les informations importantes ont été extraites.  