## Ajout du chemin vers src pour l'utiliser comme package

import os, sys, inspect
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
cmd_folder = cmd_folder[0:cmd_folder.find("notebooks")]
sys.path.append(cmd_folder)
sys.path.append(cmd_folder+"src/")

from src import buyer_history

## First model with Density

#Maintenant essayons de calculer les densités d'évenements par rapport au moment de l'achat:
#On importe le dataframe density_data
from model_density import density_data
#Pour calculer la densité on prend donc que les valeures avant le dernier achat de chaque acheteur.
#On calcule donc la difference entre timestamp et last_purchase_timestamp pour cacluler la densité : timestamp_difference

import matplotlib.pyplot as plt
plt.style.use('ggplot')

#Premier résultat avec des histogrammes stacked
for event in density_data["event"].unique():
    (density_data["timestamp_difference"][density_data["event"]==event]).apply(timedelta.total_seconds).hist(stacked=True,bins=20).set_xlim(-20000000,0)
plt.show()

#Le nombre d'évenements différents est trop important pour tout étudier comme ça, on regroupe les "crm", les "iadvize" et les "demande" ensemble.
#On retire aussi les évenements qui sont évidents tel que l'achat du projet et le passage en magasin le jour J.

from src.model_density import density_data_cleaned

#Résultats avec des densités
from matplotlib import cm
from numpy import linspace

colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_data_cleaned["event"].unique().size) ]

for i,event in enumerate(density_data_cleaned["event"].unique()):
    (density_data_cleaned["timestamp_difference"][density_data_cleaned["event"]==event]).apply(timedelta.total_seconds).plot(kind="density",use_index=False,legend='reverse',label=event,c=colors[i]).set_xlim(-30000000,0)

plt.legend(loc=2,prop={'size':6})
plt.show()
