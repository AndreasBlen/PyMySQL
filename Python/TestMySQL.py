#! usr/bin/env python3

# =================================== #
# DB-Routinen mit PyMySQL
# Konfig-File, try/except-Blöcke
# =================================== #

import datetime as dt
import os 
import pymysql.cursors
import sys

# --------------------------
# Properties-Datei einlesen
# --------------------------
def load_properties(filepath, sep='=', comment_char='#'):
    """
    Einlesen einer Properties-Datei mit Key-Value-Paaren.
    Kommentare und Leerzeilen überlsen.
    Rückgabe der Properties als Python-Dictionary. 
    """
    props = {}
    
    try:
        with open(filepath, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"') 
                    props[key] = value 
                    
    except FileNotFoundError:
        print("Datei", filepath, "nicht vorhanden!")
        exit(1); 
    except: 
        print("Fehler beim Zugriff auf Properties-Datei:", filepath)
        exit(1); 

    return props


# -----------------------------
# Datenbankverbindung aufbauen 
# -----------------------------
def get_connection(dbprops):
    """
    Verbindung zu MySQL aufbauen anhand der Properties, 
    und Verbindungsobjekt zurückgeben
    """
    try:
        host = dbprops["host"]
        user = dbprops["user"]
        password=dbprops["password"]
        cursorclass = dbprops["cursorclass"]


        conn = pymysql.connect(host=dbprops["host"], 
                user=dbprops["user"], 
                password=dbprops["password"], 
                db=dbprops["db"],
                charset=dbprops["charset"], 
                # cursorclass=dbprops["cursorclass"])
                cursorclass=pymysql.cursors.DictCursor)
    except BaseException as ex: 
        print("Fehler bei DB-Zugriff:\n", ex)
        exit(1)

    return conn


# -----------------------------------------------------------------------
# norm_string: String (der "None" sein kann) mit genau n Zeichen ausgeben
# Grund für die Funktion:  Formatieren auf n Stellen schneidet nicht ab, 
#                          wenn der String länger ist 
# -----------------------------------------------------------------------
def norm_string(s, length, NoneDarstellung = ""):
    if s == None: s = NoneDarstellung   # für None entsprechende Darstellung ausgeben 
    if len(s) > length:                 # längere Strings abschneiden mit Slicing-Syntax
        s = s[:length]
    
    s = s.ljust(length, " ")            # kürzere Strings auffüllen (alternativ über format() ) 
    return s
    


# -----------------------------
# Insert 
# -----------------------------
def do_insert(conn):

    # Einlesen
    print("Bitte für neuen Datensatz in Tab. MEDIUM Werte eingeben:")
    print("(leere Eingabe --> null)")
    titel = input("Titel:")
    verfasser = input("Verfasser:")
    medientyp = input("Medientyp (int):"); 
    kategorie = input("Kategorie (int):"); 
    signatur = input("Signatur:"); 
    erscheinungsdatum = input("Erscheinungsdatum (TT.MM.JJJJ):")
    
    auflage = input("Auflage (int):")
    verlag = input("Verlag:")
    einstandspreis = input("Einstandspreis (max. 2 NK):").replace(",", ".") 
    anschaffungsdatum = input("Anschaffungsdatum (TT.MM.JJJJ):")
    inhalt=input("Inhalt:")
    anmerkung=input("Anmerkung:")

    # Aufbereiten
    if titel == "": titel = None
    if verfasser == "": verfasser = None
    if medientyp == "": medientyp = None
    if kategorie == "": kategorie = None
    if signatur == "": signatur = None
    if erscheinungsdatum == "": erscheinungsdatum = None
    elif erscheinungsdatum.count(".") == 2: erscheinungsdatum = dt.datetime.strptime(erscheinungsdatum, "%d.%m.%Y").date()

    if auflage == "": auflage = None
    if verlag == "": verlag = None
    einstandspreis = einstandspreis.replace(",", ".")  # bleibt String
    if anschaffungsdatum == "": anschaffungsdatum = None
    elif anschaffungsdatum.count(".") == 2: anschaffungsdatum = dt.datetime.strptime(anschaffungsdatum, "%d.%m.%Y").date()

    if inhalt == "": inhalt = None
    if anmerkung == "": anmerkung = None

    # Speichern 
    with conn.cursor() as csr:
        sql = ( "INSERT INTO `medium`(`titel`, `verfasser`, `medientyp`, `kategorie`, `signatur`, `erscheinungsdatum`, "
                                   "  `auflage`, `verlag`, `einstandspreis`, `anschaffungsdatum`, `inhalt`, `anmerkung`, " 
                                   "   ts_last_update, `ts_created`) " 
                                   "   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " ) 

        curr_ts = dt.datetime.now()
        csr.execute(sql, (titel, verfasser, medientyp, kategorie, signatur, erscheinungsdatum, 
                    auflage, verlag, einstandspreis, anschaffungsdatum, inhalt, anmerkung, curr_ts, curr_ts)) 
        conn.commit()
        print("Hinzugefügt: ID Nr.", csr.lastrowid)

# -----------------------------
#  Select
# -----------------------------
def do_select(conn):
    i = input("Gib Satznummer:")
    try:
        with conn.cursor() as csr:
            sql = ( "SELECT `id`, `titel`, `verfasser`, `medientyp`, `kategorie`, `signatur`, `erscheinungsdatum`, "
                "  `auflage`, `verlag`, `einstandspreis`, `anschaffungsdatum`, `inhalt`, `anmerkung`, " 
                "   ts_last_update, `ts_created`, `ts_upd_internal` " 
                " FROM medium WHERE id = %s " ) 
            csr.execute(sql, i)
            result = csr.fetchone()
            if not result:
                print("Satz Nr.", i, "nicht gefunden!")
                return
            
           
    except BaseException as ex: 
        print("Fehler bei DB-Zugriff:\n", ex)

    # print("Satz in Dictionary-Form:")        
    # print(result) 
    f_id = f"{i}" ; l_id = len(f_id); 
    f_titel=result["titel"] if result["titel"] != None else "(null)"; l_titel = len(f_titel)  
    f_verfasser=result["verfasser"] if result["verfasser"] != None else "(null)"; l_verfasser = len(f_verfasser) 
    f_medientyp="{0:d}".format(result["medientyp"]) if result["medientyp"] != None else "(null)";  l_medientyp = len(f_medientyp) 
    f_kategorie="{0:d}".format(result["kategorie"]) if result["kategorie"] != None else "(null)";  l_kategorie = len(f_kategorie) 
    f_signatur=result["signatur"] if result["signatur"] != None else "(null)"; l_signatur = len(f_signatur)  
    f_erscheinungsdatum=result["erscheinungsdatum"].strftime("%d.%m.%Y") if result["erscheinungsdatum"] != None else "(null)"; l_erscheinungsdatum = len(f_erscheinungsdatum)  # Formatiert mit str.strftime()
    f_auflage="{0:d}".format(result["auflage"]) if result["auflage"] != None else "(null)";  l_auflage = len(f_auflage) 
    f_verlag=result["verlag"] if result["verlag"] != None else "(null)"; l_verlag = len(f_verlag)  
    f_einstandspreis="{0:.2f}".format(result["einstandspreis"]) if result["einstandspreis"] != None else "(null)";  l_einstandspreis = len(f_einstandspreis) ; print(f_einstandspreis, l_einstandspreis)
    f_anschaffungsdatum="{:%d.%m.%Y}".format(result["anschaffungsdatum"]) if result["anschaffungsdatum"] != None else "(null)"; l_anschaffungsdatum = len(f_anschaffungsdatum)  # Formatiert mit str.format() 
    f_inhalt=result["inhalt"] if result["inhalt"] != None else "(null)"; l_inhalt = len(f_inhalt)  
    f_anmerkung=result["anmerkung"] if result["anmerkung"] != None else "(null)"; l_anmerkung = len(f_anmerkung)  
    f_ts_last_update = "{:%Y-%m-%d %H:%M:%S}".format(result["ts_last_update"]) if result["ts_last_update"] != None else "(null)"; l_ts_last_update = len(f_ts_last_update) 
    f_ts_created = "{:%Y-%m-%d %H:%M:%S}".format(result["ts_created"]) if result["ts_created"] != None else "(null)"; l_ts_created = len(f_ts_created) 
    f_ts_upd_internal = "{:%Y-%m-%d %H:%M:%S}".format(result["ts_upd_internal"]); l_ts_upd_internal = len(f_ts_upd_internal) 
    
    max_feldlaenge = max(20, len(f_id), 
                                len(f_titel), 
                                len(f_verfasser), 
                                len(f_medientyp), 
                                len(f_kategorie), 
                                len(f_signatur), 
                                len(f_erscheinungsdatum), 
                                len(f_auflage), 
                                len(f_verlag), 
                                len(f_einstandspreis), 
                                len(f_anschaffungsdatum), 
                                len(f_inhalt), 
                                len(f_anmerkung), 
                                len(f_ts_last_update), 
                                len(f_ts_created), 
                                len(f_ts_upd_internal)) ; print(max_feldlaenge) 
    print("+", "-"*20, "+", "-" * (max_feldlaenge + 4), "+", sep="")
    print("I  ID ...............:",   " " * (max_feldlaenge - len(f_id)), f_id, " I") 
    print("I  Titel ............:",   " " * (max_feldlaenge - len(f_titel)), f_titel, " I") 
    print("I  Verfasser ........:",   " " * (max_feldlaenge - len(f_verfasser)), f_verfasser, " I") 
    print("I  Medientyp ........:",   " " * (max_feldlaenge - len(f_medientyp)), f_medientyp, " I") 
    print("I  Kategorie ........:",   " " * (max_feldlaenge - len(f_kategorie)), f_kategorie, " I") 
    print("I  Signatur .........:",   " " * (max_feldlaenge - len(f_signatur)),  f_signatur,  " I") 
    print("I  Ersch.-Datum .....:",   " " * (max_feldlaenge - len(f_erscheinungsdatum)), f_erscheinungsdatum, " I") 
    print("I  Auflage ..........:",   " " * (max_feldlaenge - len(f_auflage)), f_auflage, " I") 
    print("I  Verlag ...........:",   " " * (max_feldlaenge - len(f_verlag)),  f_verlag,  " I") 
    print("I  Einstandspreis ...:",   " " * (max_feldlaenge - len(f_einstandspreis)), f_einstandspreis, " I") 
    print("I  Anschaff.-Datum ..:",   " " * (max_feldlaenge - len(f_anschaffungsdatum)), f_anschaffungsdatum, " I") 
    print("I  Inhalt ...........:",   " " * (max_feldlaenge - len(f_inhalt)), f_inhalt, " I") 
    print("I  Anmerkungen ......:",   " " * (max_feldlaenge - len(f_anmerkung)), f_anmerkung, " I") 
    print("I  Letzte Änderung ..:",   " " * (max_feldlaenge - len(f_ts_last_update)), f_ts_last_update, " I") 
    print("I  TS der Anlage ....:",   " " * (max_feldlaenge - len(f_ts_created)), f_ts_created, " I") 
    print("I  TS internal update:",   " " * (max_feldlaenge - len(f_ts_upd_internal)), f_ts_upd_internal, " I") 
    print("+", "-"*20, "+", "-" * (max_feldlaenge + 4), "+", sep="")
    
 
# -----------------------------
#  Count
# -----------------------------
def do_count(conn):
    try:
        with conn.cursor() as csr:
            sql = "SELECT COUNT(*) AS anz FROM MEDIUM"
            csr.execute(sql)
            result = csr.fetchone()

        print("Tabelle MEDIUM hat zur Zeit", result["anz"], "Sätze.")
            
    except BaseException as ex: 
        print("Fehler bei DB-Zugriff:\n", ex)

 

# -----------------------------
#  Overview
# -----------------------------
def do_overview(conn):
    i = input("Nr. des Satzes, ab dem Daten (10 Sätze) angezeigt werden werden sollen - Default: ab Anfang:")
    if i.strip() == "": i = "0" 
    try:
        with conn.cursor() as csr:
            sql = ( "SELECT m.id, titel, verfasser, mt.medientyp_bez mt_bez, kat.kategorie_bez kat_bez,  "
                "  auflage, verlag, erscheinungsdatum, anmerkung, m.ts_last_update last_upd " 
                " FROM medium m" 
                " LEFT JOIN medientyp mt ON mt.id = m.medientyp " 
                " LEFT JOIN kategorie kat ON kat.id = m.kategorie " 
                " WHERE m.id >= %s "
                " ORDER BY m.id "
                " LIMIT 10" ) 
                
                
            csr.execute(sql, i)
            result = csr.fetchall()
            if not result:
                print("keine Daten gefunden!")
                return
            
            # print(result)
            titel = ("\n  ID  Verfasser             Titel                      Typ des Mediums       Kategorie    Auflage  Verlag                     " 
                    "Ersch.Dat.  Anmerkung                                 Letzte Änderung" ) 
            print(titel) 
            print("-" * 199) 
            for rec in result:
                f_id = f'{rec["id"]:4d}'
                f_verfasser = norm_string(rec["verfasser"], 20)
                f_auflage = rec["auflage"]
                if f_auflage == None: 
                    f_auflage = "   " 
                else:
                    f_auflage = f'{f_auflage:3d}' 
                
                hilf = rec["erscheinungsdatum"]
                if hilf == None:
                    f_erscheinungsdatum = " "*10;
                else:
                    f_erscheinungsdatum = hilf.strftime("%d.%m.%Y")
                print(f_id, 
                        norm_string(rec["verfasser"], 20),
                        norm_string(rec["titel"], 25),
                        norm_string(rec["mt_bez"], 20),
                        norm_string(rec["kat_bez"], 15),
                        f_auflage, 
                        norm_string(rec["verlag"], 25),  
                        f_erscheinungsdatum,
                        norm_string(rec["anmerkung"], 40), 
                        rec["last_upd"],
                        sep = "  ")
            
           
    except BaseException as ex: 
        print("Fehler bei DB-Zugriff:\n", ex)

 

# -----------------------------
#  Update
# -----------------------------
def do_update(conn):
    i = input("Nr. des Satzes, für den Felder geändert werden sollen:")
    try:
        with conn.cursor() as csr:
            sql = ( "SELECT `id`, `titel`, `verfasser`, `medientyp`, `kategorie`, `signatur`, `erscheinungsdatum`, "
                "  `auflage`, `verlag`, `einstandspreis`, `anschaffungsdatum`, `inhalt`, `anmerkung`, " 
                "   ts_last_update, `ts_created`, `ts_upd_internal` " 
                " FROM medium WHERE id = %s " ) 
            csr.execute(sql, i)
            result = csr.fetchone()
            if not result:
                print("Satz Nr.", i, "nicht gefunden!")
                return
            
           
    except BaseException as ex: 
        print("Fehler bei DB-Zugriff:\n", ex)

    print("-------------------------------------------") 
    print("Anm.: Eingaben für Updates:") 
    print("      leere Eingabe:  unverändert lassen") 
    print("      Blank:          Feld leeren") 
    print("      \"null\":         auf NULL setzen") 
    print("      sonstiger Wert: Feld entsprechend ändern") 
    print("-------------------------------------------") 
    i_titel             = input("Titel: ..........: ")  
    i_verfasser         = input("Verfasser .......: ")
    i_medientyp         = input("Medientyp .......: ")
    i_kategorie         = input("Kategorie .......: ")
    i_signatur          = input("Signatur ........: ")
    i_erscheinungsdatum = input("Erscheinungsdatum: ")
    i_auflage           = input("Auflage .........: ")
    i_verlag            = input("Verlag ..........: ")
    i_einstandspreis    = input("Einstandspreis ..: ")
    i_anschaffungsdatum = input("Anschaffungsdatum: ")
    i_inhalt            = input("Inhalt ..........: ")
    i_anmerkung         = input("Anmerkung .......: ")

    mod_titel = True
    if len(i_titel) == 0:    mod_titel = False      # keine Eingabe -> keine Änderung 
    elif len(i_titel.strip()) == 0: i_titel = ""    # Blank(s) eingegeben -> leeren String setzen
    
    mod_verfasser = True
    if len(i_verfasser) == 0:    mod_verfasser = False      # keine Eingabe -> keine Änderung 
    elif len(i_verfasser.strip()) == 0: i_verfasser = ""    # Blank(s) eingegeben -> leeren String setzen
    
    mod_medientyp = True
    i_medientyp = i_medientyp.strip()
    if len(i_medientyp) == 0:    mod_medientyp = False      # keine Eingabe -> keine Änderung 
        
    mod_kategorie = True
    i_kategorie = i_kategorie.strip()
    if len(i_kategorie) == 0:    mod_kategorie = False      # keine Eingabe -> keine Änderung 
    
    mod_signatur = True
    if len(i_signatur) == 0:    mod_signatur = False      # keine Eingabe -> keine Änderung 
    elif len(i_signatur.strip()) == 0: i_signatur = ""    # Blank(s) eingegeben -> leeren String setzen
    
    mod_erscheinungsdatum = True
    if len(i_erscheinungsdatum) == 0:    mod_erscheinungsdatum = False      # keine Eingabe -> keine Änderung 
    elif i_erscheinungsdatum.count(".") == 2: i_erscheinungsdatum = str(dt.datetime.strptime(i_erscheinungsdatum, "%d.%m.%Y").date()) # deutsche Formatierung umsetzen auf Std. 
    
    mod_auflage = True
    i_auflage = i_auflage.strip()
    if len(i_auflage) == 0:    mod_auflage = False      # keine Eingabe -> keine Änderung 

    mod_verlag = True
    if len(i_verlag) == 0:    mod_verlag = False      # keine Eingabe -> keine Änderung 
    elif len(i_verlag.strip()) == 0: i_verlag = ""    # Blank(s) eingegeben -> leeren String setzen
    
    mod_einstandspreis = True
    if len(i_einstandspreis) == 0:    mod_einstandspreis = False      # keine Eingabe -> keine Änderung 
    else: i_einstandspreis = i_einstandspreis.replace(",", ".")        # ggf. deutsche Formatierung umsetzen (Dez.komma auf Punkt)

    mod_anschaffungsdatum = True
    if len(i_anschaffungsdatum) == 0:    mod_anschaffungsdatum = False      # keine Eingabe -> keine Änderung 
    elif i_anschaffungsdatum.count(".") == 2: i_anschaffungsdatum = str(dt.datetime.strptime(i_anschaffungsdatum, "%d.%m.%Y").date())  # deutsche Formatierung umsetzen auf Std. 

    mod_inhalt = True
    if len(i_inhalt) == 0:    mod_inhalt = False      # keine Eingabe -> keine Änderung 
    elif len(i_inhalt.strip()) == 0: i_inhalt = ""    # Blank(s) eingegeben -> leeren String setzen
    
    mod_anmerkung = True
    if len(i_anmerkung ) == 0:    mod_anmerkung  = False      # keine Eingabe -> keine Änderung 
    elif len(i_anmerkung .strip()) == 0: i_anmerkung  = ""    # Blank(s) eingegeben -> leeren String setzen
    
    sql = "UPDATE MEDIUM SET " 
    if mod_titel: sql = sql + " titel = '" + i_titel + "', " 
    if mod_verfasser: sql = sql + " verfasser = '" + i_verfasser + "', " 
    if mod_medientyp: sql = sql + " medientyp = " + i_medientyp + ", " 
    if mod_kategorie: sql = sql + " kategorie = " + i_kategorie + ", " 
    if mod_signatur: sql = sql + " signatur = '" + i_signatur + "', " 
    if mod_erscheinungsdatum: sql = sql + " erscheinungsdatum = '" + i_erscheinungsdatum + "', " 
    if mod_auflage: sql = sql + " auflage = " + i_auflage + ", " 
    if mod_verlag: sql = sql + " verlag = '" + i_verlag + "', " 
    if mod_einstandspreis: sql = sql + " einstandspreis = " + i_einstandspreis + ", " 
    if mod_anschaffungsdatum: sql = sql + " anschaffungsdatum = '" + i_anschaffungsdatum + "', " 
    if mod_inhalt: sql = sql + " inhalt = '" + i_inhalt + "', " 
    if mod_anmerkung: sql = sql + " anmerkung = '" + i_anmerkung + "', " 
    if len(sql) < 20:
        print("\n\nKeine Feldänderung vorgenommen.\nEs wird kein Update durchgeführt.") 
        return 
        
    sql = sql.replace("'null'", "null")     # don't ask
    sql = sql + " ts_last_update = CURRENT_TIMESTAMP \nWHERE id = " + i 
    print(sql)     
    try:
        with conn.cursor() as csr:
            csr.execute(sql)
            conn.commit()
    except BaseException as ex: 
        print("Fehler bei Update auf Satz Nr.", i, ":\n", ex)
        return
        
    print("\nUpdate ausgeführt.")
    
# -----------------------------
#  Delete
# -----------------------------   
def do_delete(conn):
    i = input("Nr. des Satzes, der gelöscht werden soll:")
    try:
        with conn.cursor() as csr:
            sql = ( "DELETE FROM medium WHERE id = %s " ) 
            csr.execute(sql, i)
            if csr.rowcount < 1:
                print("Satz Nr.", i, "nicht gefunden!")
                return
            conn.commit()
           
    except BaseException as ex: 
        print("Fehler bei DB-Zugriff:\n", ex)

    print("\nSatz Nr.", i, "gelöscht.")
    
    
# -----------------------------
#  Clear Screen
# -----------------------------
def clear_screen():
    # print("OS:", os.name); 
    # print("sys.platform:", sys.platform, "\n\n\n")

    if os.name == "nt":
        _ = os.system("cls")  # Konvention: "_" enthält letzten rc
    elif os.name == 'posix':
        _ = os.system("clear")
    else:
        print("unbekanntes OS:", os.name); 
        print("sys.platform:", sys.platform, "\n\n\n")    
    


# =================================== #
# Beginn Hauptprogramm  
# =================================== #
propsfile = "mysql.properties"
dbprops=load_properties(propsfile)     

conn = get_connection(dbprops) 

answer = ""
ende = False
auswahlprompt = """\n
Bitte eine Option auswählen:
10:  Insert
20:  Update
30:  Delete
40:  Select
41:  Übersicht - 10 Sätze ab Nr. x
50:  Sätze zählen
90:  Clear screen
99:  Ende\n
"""

while not ende: 
    answer = input(auswahlprompt); 

    if   answer == "10":    do_insert(conn) 
    elif answer == "20":    do_update(conn) 
    elif answer == "30":    do_delete(conn) 
    elif answer == "40":    do_select(conn) 
    elif answer == "41":    do_overview(conn) 
    elif answer == "50":    do_count(conn) 
    elif answer == "90":    clear_screen() 
    elif answer == "99":    ende = True; 
 

      
conn.close()
print("*** bye ****")

