DELIMITER $$

#trigger pour vérifier si la fiche du personnage existe avant de faire un insert
CREATE TRIGGER resultat_before_insert
    BEFORE INSERT on fiche_personnage 
    FOR EACH ROW 
    BEGIN 

        IF NOT EXISTS (SELECT id FROM fiche_personnage WHERE id = NEW.id) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Le id de la fiche est inconnu';
        END IF;

    END$$

DELIMITER ;


#procedure pour aller chercher les information de la fiche du personnage
DELIMITER $$

CREATE PROCEDURE RecupererInfoFiche()
BEGIN
	SELECT *  FROM fiche_personnage;
end $$

DELIMITER ;



#creer un nouveau user
CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY '1234';

GRANT SELECT, INSERT, UPDATE, DELETE
ON livre_dont_vous_etes_le_hero.*
TO user@localhost;
