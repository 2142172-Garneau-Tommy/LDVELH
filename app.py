import sys

import mysql.connector as mysql
from PyQt5.QtCore import QFileInfo, QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp

# Importer la classe Ui_MainWindow du fichier MainWindow.py
from LivreInterface import Ui_MainWindow

db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'mysql',
    'database' : 'livre_dont_vous_etes_le_hero'
}

def restorer(self):

        connection = mysql.connect(**db_config)
        cursor = connection.cursor()
        query_discipline = "SELECT type from discipline"

        cursor.execute(query_discipline)

        self.discipline_text_box.setText(query_discipline)
        self.arme_text_box.setText()
        self.repas_text_box.setText()
        self.objet_text_box.setText()
        self.objet_speciaux_text_box.setText()
        self.bourse.setText()

        connection.commit()

# En paramêtre de la classe MainWindow on va hériter des fonctionnalités
# de QMainWindow et de notre interface Ui_MainWindow
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # On va créer la fenêtre avec cette commande
        self.setupUi(self)

    #Function pour modifier la fiche
    def modifierFiche(self):
        """
        Modifie une fiche
        Arguments:
            discipline_kai: un string
            arme: un string
            repas: un integer
            objet: un string
            objet_speciaux: un string
            bourse: un int
        """
    
        displine_kai = self.discipline_text_box
        arme = self.arme_text_box
        repas = self.repas_text_box
        objet = self.objet_text_box
        objet_speciaux = self.objet_speciaux_text_box
        bourse = self.bourse


        query_fiche = """ UPDATE fiche_personnage
                SET repas = %(repas)s, 
                objet = %(objet)s, 
                objet_speciaux = %(objet_speciaux)s;"""

        parametres_fiche = (repas, objet, objet_speciaux)

        query_arme = """ UPDATE arme
                SET type = %(type)s;"""

        parametres_arme = (arme)

        query_discipline = """ UPDATE discipline
                SET type = %(type)s;"""

        parametres_discipline = (displine_kai)
      

        result = ()
        try:
            connection = mysql.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(query_fiche, parametres_fiche)
            cursor.execute(query_arme, parametres_arme)
            cursor.execute(query_discipline, parametres_discipline)
            result = cursor.fetchone()
        except mysql.Error as erreur:
            print(erreur)
        finally:
            cursor.close() 
            connection.close()


    #function pour sauvegarder la fiche
    def sauvegarder(self):
        """
        Ajoute une fiche
        Arguments:
            discipline_kai: un string
            arme: un string
            repas: un integer
            objet: un string
            objet_speciaux: un string
            bourse: un int
    """
        try:

            connection = mysql.connect(**db_config)
            cursor = connection.cursor()

            discipline = self.discipline_text_box.text()
            arme = self.arme_text_box.text()
            repas = self.repas_text_box.text()
            objet = self.objet_text_box.text()
            objet_speciaux = self.objet_speciaux_text_box.text()
            bourse = self.bourse_text_box_text_box.text()
            progression_arme = "SELECT id from arme"

            query_fiche = "INSERT INTO fiche_personnage (repas, objet, objet_speciaux) VALUES (%s, %s, %s)"
            val_fiche = (repas, objet, objet_speciaux)
            query_arme = "INSERT INTO arme (type) VALUES (%s)"
            val_arme = (arme)
            query_discipline = "INSERT INTO discipline (type) VALUES (%s)"
            val_discipline = (discipline)
            query_progression = "INSERT INTO progression (id_chapitre, id_fiche_personnage, id_livre) VALUES (%i, %i, %i)"
            val_progression = ()
 
            cursor.execute(query_fiche, val_fiche)
            cursor.execute(query_arme, (val_arme,))
            cursor.execute(query_discipline, (val_discipline,))
            cursor.execute(query_discipline, (val_discipline,))
 
            connection.commit()
 
        except mysql.Error as erreur:
            print(erreur)

    #function pour supprimer la sauvegarde
    def supprimerSauvegarde(self):
        """
        Supprime la fiche
        Arguments:
            discipline_kai: un string
            arme: un string
            repas: un integer
            objet: un string
            objet_speciaux: un string
            bourse: un int
            no_chapitre: un int
        """

        connection = mysql.connect(**db_config)
        cursor = connection.cursor()
        
        query_fiche = "DELETE FROM fiche_personnage"
        query_arme = "DELETE FROM arme"
        query_discipline = "DELETE FROM discipline"
        query_progression = "DELETE FROM progression"
        query_naviguation = "DELETE FROM navigation"
     
        try:
     
            cursor.execute(query_fiche)
            cursor.execute(query_arme)
            cursor.execute(query_discipline)
            cursor.execute(query_progression)
            cursor.execute(query_naviguation)
       
            connection.commit()
        except mysql.Error as erreur:
            print(erreur)
            
            print(cursor.fetchall())

            cursor.close()
            connection.close()
            
    #function pour récupérer le chapitre
    def getChapitre(self, no_chapitre):
        """
        Sélectionne le chapitre d'un livre
        Arguments:
            id: le id du citoyen (integer)
        Returns:
            le texte du chapitre
        """

        query = "select texte from chapitre c where c.no_chapitre = %(no_chapitre)s;"
        parametres = {
            'no_chapitre' : no_chapitre
         }
        result = ()
        try:
            connection = mysql.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(query, parametres)
            result = cursor.fetchone()
        except mysql.Error as erreur:
            print(erreur)
        finally:
            cursor.close() 
            connection.close()

        return result

    #function pour afficher le prochain chapitre
    def changerChapitre(self):
        chapitre_suivant = self.chapitre_text.text()
        #query = "SELECT "
        #try:
            #cursor.execute(query_chapPos)
        #except mysql.Error as erreur:
            #print(erreur)
        #if chapitre_suivant
        resultat = self.getChapitre(chapitre_suivant)
        chapitre_texte = "Le chapitre n'existe pas"
        if resultat is not None:
            texte = resultat
        self.chapitre_text_box.setText(texte[0])
  
app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()