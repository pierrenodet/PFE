# Projet de Fin d'Etudes

Projet de Fin d'Etudes réalisé pour Advalo sur la détermination de parcours client.

## Qu'est-ce qu'il y a dans ce repository

Pour le moment il y a 2 dossiers importants :
- src : un package Python qui contient tout le code nécessaire pour la pipeline du projet,
- notebooks : un recueil de notebooks permettant d'illustrer le code du src (graphiques, stat desc, ...)

Le code du notebook est un code Python succinct parfait pour de l'exploration de données ou de la data visualisation.

Néanmoins ce n'est pas fait pour du gros traitement de données. Ainsi tout le data preprocessing ou tout code redondant doit se trouver dans le src.

En fait à la fin du projet seul le src devra être nécessaire pour pouvoir trouver la modélisation attendu (indépendamment des notebooks). Il faudra toutefois éviter de faire un code trop lourd dans le src (pas de tests, pas de brouillon, pas de commentaires, ...)

Enfin le dossier src est struturé comme un package python classique avec un éxecutable contenu dans le main. Lorsque celui ci est executé, tous les résultats (tableaux, chiffres ou images) du rapports doivent être générés ainsi que toutes les données transformées.

Cette organisation de projet est fortement inspiré de ce site :
https://drivendata.github.io/cookiecutter-data-science/

Je vous laisse donc consulter les détails dessus.

## Configuration File

Dans ce repository il y a un fichier de configuration écrit en YAML (version "human readable" de JSON).

Ce fichier contient des informations nécessaires au script pour s'éxecuter mais qui sont dépendantes de l'environnement d'éxecution.
Par exemple le fichier de configuration contient actuellement le dossier contenant les données : ce chemin est différent pour chacun d'entre nous.

En revanche vous devez posséder sur votre machine un autre config.yml qui sera utilisé pour le script. Celui ci ne dois pas être push (.gitignore) car il contient des données qui vous sont propres. Le config.sample.yml est juste un patron qui est utilisé pour créer le véritable config.yml.

Dans notre cas il contient les données relatives au ftp. L'example sur le github montre tous les paramètres qui doivent être renseignés, sauf pour le mot de passe.

## Dépendances

Ce github utilise Python 3.5.

La liste des packages Python nécessaire pour ce github est dans requirements.txt

Comment télécharger PyYAML :

wget http://pyyaml.org/download/pyyaml/PyYAML-3.12.tar.gz  
tar -xvfz PyYAML-3.12.tar.gz  
cd PyYAML-3.12/  
python3 setup.py install  

Comment télécharger Jupyter Notebook :

pip3 install jupyter  
pip3 install ipython

## Authors

* **Pierre NODET** - [Pierre](https://github.com/PierreNodet)

* **Jérémy LE GALL** - [Jérémy](https://github.com/JeremyLG)

* **Laure NICOLLET** - [Laure](https://github.com/laurenicollet)
