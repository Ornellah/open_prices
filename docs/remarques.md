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