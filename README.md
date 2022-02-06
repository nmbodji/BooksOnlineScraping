#Manuel d'utilisation de l'application BooksOnlineScraping

BooksOnlineScraping est une application de Books Online qui permet de récupérer certaines informations de tous les livres 
mis en ligne par Books To scrape : une [librairie en ligne](http://books.toscrape.com) .
Pour chaque catégorie de livres : 

1. **Un fichier csv** sera généré listant tous les livres et pour chacun, ces informations ci-dessous : 
   - L'URL de la page web présentant le livre (product_page_url)
   - Code universel de chaque produit (universal_ product_code (upc))
   - Le titre du livre (title)
   - Le prix avec la taxe inclus (price_including_tax)
   - Le prix sans la taxe (price_excluding_tax) 
   - La valeur du stock courant (number_available)
   - La description du livre (product_description)
   - La categorie du livre (category)
   - La note du livre par les acheteurs sur 5 étoiles (review_rating),
   - L'URL de l'image du livre (image_url)


2. **Un dossier** contenant **les images de tous les livres** qui constituent la catégorie, sera également créé.

Cette application permet de suivre les prix du concurrent Books To Scrape de façon efficace et rapide. 
Cette première version est une version bêta qui ne permet pas une surveillance en temps réel des prix sur la durée.En effet, 
il s'agit simplement d'une application exécutable à la demande visant à récupérer les prix au moment de son exécution.

#Première étape : Ouvrir un terminal 

Un terminal est une application permettant de dialoguer avec son ordinateur via l’écriture de lignes de commande.
C'est par cette application que vous allez demander à l'ordinateur d'excécuter BooksOnlineScraping

##Si vous êtes sur linux
Vous pouvez directement ouvrir un terminal en suivant les instructions suivantes :
```
Cliquez sur Applications > Accessoires > Terminal.
```
Vous pouvez également utiliser le raccourci : Ctrl + Alt + T

##Si vous êtes sur Mac
Vous pouvez accéder à un terminal via :
```
Applications > Utilitaires > Terminal.app
```

##Si vous êtes sur Windows
Vous devez télécharger l'application via deux options :
- soit  "Cygwin", que vous pouvez télécharger et installer en suivant les instructions du [site officiel](https://www.cygwin.com/install.html)
- soit Le shell Bash pour Windows, que vous pouvez installer en suivant  (en français).[les instructions officielles de Microsoft](https://www.cygwin.com/install.html)

#Deuxième étape : Télécharger python
L'application BooksOnlineScraping a été codé avec Python 3.9.7
Vous pouvez télécharger cette version de python via ce [lien](https://www.python.org/downloads/)
Si vous avez déjà python, et que vous voulez voir quelle version vous avez, tapez la commande ci-dessous : 
```
> python --version
Python 3.9.7
```
#Troisième étape : Télécharger BooksOnlineScraping dans le dossier que vous souhaitez
## 1. Créer un dossier qui va acceuillir l'application
- Ouvrir un terminal 
- Taper la commande ci-dessous pour savoir où vous vous trouvez dans l'arborescence des fichiers : 
```
> pwd
/Users/najatmbodji
```

- Puis, taper la commande ls pour savoir que contient ce repertoire : 
```
> ls
Applications		Documents		Library			Music			Pictures		gretl			setuptools-33.1.1.zip
Desktop			Downloads		Movies			OneDrive		Public			opt

```
- Créer un nouveau dossier où vous allez récupérer l'application : 
```
> mkdir Documents/WebScraping
```
- Déplacer-vous dans ce dossier à l'aide de la commande ci-dessous :
```
> cd Documents/WebScraping 
```
- Enfin, vérifier bien que vous êtes dans ce dossier en utilisant de nouveau la commande pwd : 
```
> pwd 
/Users/najatmbodji/Documents/WebScraping
```
## 2. Télécharger git : le gestionnaire de versions

- Choisisser et télécharger la [version](https://git-scm.com/downloads) de Git qui correspond à votre système d'exploitation  : MacOS, Windows ou Linux/Unix.

- Exécuter le fichier que vous venez de télécharger. 

- Appuyer sur Suivant à chaque fenêtre puis sur Installer. Lors de l’installation, laissez toutes les options par défaut, elles conviennent bien.

***Si vous êtes sous Windows : cochez ensuite Launch Git Bash. Pour les utilisateurs de Mac ou Linux, votre terminal suffira amplement.
Git Bash est l’interface permettant d’utiliser Git en ligne de commande.***

## 3. Télécharger BooksOnlineScraping en utilisant git clone

- Vérifier que vous êtes dans le dossier que vous avez créé pour acceuillir l'application, dans notre exemple : Webscraping (voir étape 1)

- Excécuter la commande ci-dessous : 
```
> git clone https://github.com/nmbodji/BooksOnlineScraping.git
Clonage dans 'BooksOnlineScraping'...
remote: Enumerating objects: 42, done.
remote: Counting objects: 100% (42/42), done.
remote: Compressing objects: 100% (27/27), done.
remote: Total 42 (delta 15), reused 37 (delta 10), pack-reused 0
Réception d'objets: 100% (42/42), 9.38 Kio | 1.04 Mio/s, fait.
Résolution des deltas: 100% (15/15), fait.
```

- Si vous excécutez la commande ls, vous aurez un dossier Projet2BooksOnline
```
> ls
BooksOnlineScraping
```

#Quatrième étape : Creer un environnement virtuel 
## 1. Creer un environnement virtuel

- Aller dans le dossier de l'application
```
>cd BooksOnlineScraping
```
- Vérifier que vous êtes bien dans le dossier avec la commande pwd 
```
>pwd

```
- Creer un nouvel environnement virtuel avec la commande. C'est l'environnement dans lequel l'application BooksOlineScraping
va s'excécuter
```
>python -m venv env

```
- Un dossier env est créé. Vérifier cela avec la commande ls
```
>ls

```

## 2. Activez un environnement virtuel

- Activer l'environnement viruel que vous avez créé à l'étape précédente : 
```
>source env/bin/activate
```

## 3. Installer les paquets indispensables pour le lancement de l'application BooksOnlineScraping
- Installer les paquets nécessaires à l'excécution de l'application
```
>pip install -r requirements.txt
```

#Cinquième étape : Lancer l'application BooksOnlineScraping

Vous pouvez lancer l'application en tapant cette commande : 
```
>python code_sources/main.py


```

L'application se lancera et vous dira à chaque fois quelle catégorie de livres il est entrain de traiter.
Il aura terminé une fois que vous verrez ceci dans le terminal : 
```
Web scraping done for the web page :  https://books.toscrape.com/index.html
```
Ensuite, quand vous lancerez la commande ls, vous verrez un dossier output. Dans ce dossier output, vous aurez plusieurs dossiers. 
Chaque dossier a pour nom une catégorie de livres du site internet de Books To scrape et à l'intérieur de chaque dossier vous aurez :
- Un fichier csv qui a pour nom le nom de la catégorie
- Toutes les images des livres de cette catégorie.




