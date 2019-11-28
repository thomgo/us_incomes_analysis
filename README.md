# Analyse de revenu des foyers américains par état et par ethnie
 Il s'agit d'une application développée dans le cadre de mon poste de formateur en programmation. L'objectif est que les apprenants produisent une micro-application web à l'aide du framework Flask afin de présenter une analyse des données du bureau du recensement américain à l'aide des librairies Pandas et Matplotlib. Ils se familiarisent ainsi avec le traitement de données, l'analyse de données et leur intégration dans une application web en python.

 Au travers de ce projet les étudiants apprennent à :
 - Utiliser la librairie Pandas et Matplotlib
 - Evaluer la pertinence des données collectées
 - Traiter un fichier CSV
 - Enrichir un fichier de données
 - Travailler avec des dataframes
 - Produire des graphiques sous formes d'images ou de tableaux HTML
 - Mettre en forme des des données
 - Présenter une analyse de données
 - Argumenter en anglais
 - Produire rapidement une micro-application avec Flask

 ## Consignes

 Vous travaillez pour une agence d'étude qui a été contactée par un représentant d'une association de lutte contre les inégalités et la pauvreté. Cette association a récupéré un fichier de données sur le site du bureau du recensement américain et elle souhaiterait en avoir une analyse afin d'évaluer la pertinence de ces données et leur éventuelle utilité dans son champ d'action.

 Afin que les données puissent facilement être rendues publiques, elle vous a demandé de les mettre en ligne sous la forme d'un site internet simple.

 Le fichier d'origine du bureau du recensement vous a été fourni par cette association. Attention en l'état le fichier n'est pas exploitable ou alors très difficilement, il vous faudra réaliser quelques ajustements afin d'en tirer le maximum d'informations :
 - Retirer manuellement les informations périphériques (titres et autres)
 - Renommer les colonnes qui sont très longues
 - Supprimer les données qui ne vous semblent pas pertinentes et justifier pourquoi dans votre analyse
 - Transformer les données en chiffres exploitables car en l'état tout est sous forme de strings
 - Ajouter des colonnes avec pour chaque état, le revenu le plus haut, l'ethnie la plus riche, le revenu le plus bas et l'ethnie la plus pauvre
 - Ajouter une colonne avec la localisation de l'état aux Etats-Unis (sud, nord ou ouest). Une liste des états nommée geographical_information vous est donnée.

  Afin de vous aiguiller dans votre analyse qui pourrait être très longue, l'association a défini des questions auxquelles elle aimerait avoir une réponse :
  - Comment se répartissent les revenus entre les communautés ?
  - Des communautés sont-elles plus riches/plus pauvres que d'autres ?
  - Les revenus sont-ils influencés selon la localisation de l'état ?
  - Peut-on voir une corrélation entre la localisation de l'état et le fait d'être riche ou pauvre ?
  - Certains états sont-ils plus inégalitaires que d'autres ?
  - Les données sont-elles fiables considérant les marges d'erreur mesurées ?

 Spécifications fonctionnelles :
 - Une page d'accueil présentant le tableau de données
 - Une page d'analyse présentant l'analyse des données
 - L'analyse doit être agrémentée d'indicateurs et de graphiques
 - L'utilisateur peut naviguer entre les données et l'analyse à l'aide d'un menu
 - L'analyse est organisée en titres et en sous-titres
 - Une mise en forme simple qui ne supplante pas les données mais les valorise est appliquée

 Spécifications techniques:
 - Python3
 - Flask
 - Pandas
 - Matplotlib
