# Projet de Fin d'Etudes

Projet de Fin d'Etudes réalisé pour Advalo sur la détermination de parcours client.

## Qu'est-ce qu'il y a dans ce repo

Pour le moment il y a 3 fichiers dans ce repository :
- README.md que vous êtes en train de lire,
- config.sample.yml qui est un fichier de configuration en YAML,
- script.py qui est le fichier contenant le code Python,

Dans le script.py il y a les premières étapes d'importation des données, de leur exploration et du nettoyage de ces dernières.

## Configuration File

Dans ce repository il y a un fichier de configuration écrit en YAML (version "human readable" de JSON).
Ce fichier contient des informations nécessaires au script pour s'éxecuter mais qui sont dépendantes de l'environnement d'éxecution.
Par exemple le fichier de configuration contient actuellement le dossier contenant les données : ce chemin est différent pour chacun d'entre nous.
En revanche vous devez posséder sur votre machine un autre config.yml qui sera utilisé pour le script. Celui ci ne dois pas être push (.gitignore) car il contient des données qui vous sont propres. Le config.sample.yml est juste un patron qui est utilisé pour créer le véritable config.yml.

## Dépendances

Ce script utilise Python 3.5.

Voici une liste des packages Python nécessaire pour éxecuter le script :
- PyYAML
- pandas
- matplotlib

Comment télécharger PyYAML :

wget http://pyyaml.org/download/pyyaml/PyYAML-3.12.tar.gz
tar -xvfz PyYAML-3.12.tar.gz
cd PyYAML-3.12/
python3 setup.py install
