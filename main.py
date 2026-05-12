"""
Trainingsapplikation – Modul 319
Autor: [Dein Name]
Beschreibung: CLI-App zur Dokumentation von Trainingseinheiten und persönlichem Mindset.
"""

import json
import os
from datetime import datetime

# ──────────────────────────────────────────────────────────────
# KONSTANTEN
# ──────────────────────────────────────────────────────────────
DATEN_ORDNER = "data"
TRAININGS_DATEI = os.path.join(DATEN_ORDNER, "trainings.json")
UEBUNGEN_DATEI = os.path.join(DATEN_ORDNER, "uebungen.json")
BENUTZER_DATEI = os.path.join(DATEN_ORDNER, "benutzer.json")

STIMMUNGEN = {
    "1": "😄 Sehr gut",
    "2": "😐 Neutral",
    "3": "😫 Schlecht",
}

TRENNLINIE = "=" * 50


# ──────────────────────────────────────────────────────────────
# DATEI-OPERATIONEN (Persistenz)
# ──────────────────────────────────────────────────────────────

def daten_laden(dateipfad: str) -> list:
    """Lädt JSON-Daten aus einer Datei. Gibt leere Liste zurück wenn nicht vorhanden."""
    try:
        with open(dateipfad, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"⚠️  Fehler beim Lesen von {dateipfad}. Starte mit leeren Daten.")
        return []


def daten_speichern(dateipfad: str, daten: list) -> None:
    """Speichert Daten als JSON in eine Datei."""
    os.makedirs(DATEN_ORDNER, exist_ok=True)
    with open(dateipfad, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)


def benutzer_laden() -> dict:
    """Lädt den gespeicherten Benutzer (Login-Status)."""
    try:
        with open(BENUTZER_DATEI, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def benutzer_speichern(benutzer: dict) -> None:
    """Speichert Benutzerdaten."""
    os.makedirs(DATEN_ORDNER, exist_ok=True)
    with open(BENUTZER_DATEI, "w", encoding="utf-8") as f:
        json.dump(benutzer, f, indent=2, ensure_ascii=False)


# ──────────────────────────────────────────────────────────────
# HILFSFUNKTIONEN
# ──────────────────────────────────────────────────────────────

def eingabe_zahl(prompt: str, min_wert: float = None, max_wert: float = None, erlaubt_leer: bool = False) -> float:
    """
    Liest eine Zahl vom Benutzer ein und validiert sie.

    Args:
        prompt (str): Eingabeaufforderung
        min_wert (float): Minimaler erlaubter Wert (optional)
        max_wert (float): Maximaler erlaubter Wert (optional)
        erlaubt_leer (bool): Falls True, wird leere Eingabe als None zurückgegeben

    Returns:
        float: Eingegebene Zahl
    """
    while True:
        eingabe = input(prompt).strip()
        if erlaubt_leer and eingabe == "":
            return None
        try:
            zahl = float(eingabe)
            if min_wert is not None and zahl < min_wert:
                print(f"⚠️  Bitte mindestens {min_wert} eingeben.")
                continue
            if max_wert is not None and zahl > max_wert:
                print(f"⚠️  Bitte maximal {max_wert} eingeben.")
                continue
            return zahl
        except ValueError:
            print("⚠️  Ungültige Eingabe. Bitte eine Zahl eingeben.")


def eingabe_text(prompt: str, pflicht: bool = True) -> str:
    """
    Liest einen Text vom Benutzer ein.

    Args:
        prompt (str): Eingabeaufforderung
        pflicht (bool): Falls True, darf die Eingabe nicht leer sein

    Returns:
        str: Eingegebener Text
    """
    while True:
        eingabe = input(prompt).strip()
        if pflicht and eingabe == "":
            print("⚠️  Eingabe darf nicht leer sein.")
        else:
            return eingabe


def trennlinie_ausgeben() -> None:
    """Gibt eine Trennlinie aus."""
    print(TRENNLINIE)


def datum_jetzt() -> str:
    """Gibt das aktuelle Datum und die Uhrzeit als String zurück."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ──────────────────────────────────────────────────────────────
# LOGIN / GASTMODUS
# ──────────────────────────────────────────────────────────────

def nutzerstatus_pruefen() -> dict:
    """
    Prüft ob ein Benutzer eingeloggt ist.

    Returns:
        dict: Benutzerdaten oder leeres Dict für Gast
    """
    benutzer = benutzer_laden()
    if benutzer.get("eingeloggt"):
        return benutzer
    return {}


def login_oder_gastmodus() -> dict:
    """
    Zeigt Login/Gastmodus-Auswahl an.

    Returns:
        dict: Benutzerdaten
    """
    trennlinie_ausgeben()
    print("🏋️  TRAININGSAPP – ANMELDUNG")
    trennlinie_ausgeben()
    print("1 – Einloggen / Registrieren")
    print("2 – Als Gast fortfahren")
    trennlinie_ausgeben()

    wahl = eingabe_text("Wahl: ")

    if wahl == "1":
        return benutzer_anmelden()
    else:
        print("👤 Du bist als Gast eingeloggt.")
        return {"name": "Gast", "eingeloggt": False}


def benutzer_anmelden() -> dict:
    """
    Einfacher Login/Registrierung.

    Returns:
        dict: Benutzerdaten
    """
    name = eingabe_text("Dein Name: ")
    benutzer = {
        "name": name,
        "eingeloggt": True,
        "seit": datum_jetzt()
    }
    benutzer_speichern(benutzer)
    print(f"✅ Willkommen, {name}!")
    return benutzer


def abmelden() -> None:
    """Setzt den Login-Status zurück."""
    benutzer = benutzer_laden()
    benutzer["eingeloggt"] = False
    benutzer_speichern(benutzer)
    print("👋 Erfolgreich abgemeldet.")


# ──────────────────────────────────────────────────────────────
# ÜBUNGEN VERWALTEN
# ──────────────────────────────────────────────────────────────

def uebungen_anzeigen(uebungen: list) -> None:
    """Zeigt alle gespeicherten Übungen an."""
    trennlinie_ausgeben()
    print("📋 ÜBUNGSLISTE")
    trennlinie_ausgeben()
    if not uebungen:
        print("Noch keine Übungen gespeichert.")
        return
    for i, uebung in enumerate(uebungen, 1):
        typ = uebung.get("typ", "mit Gewicht")
        print(f"  {i}. {uebung['name']}  [{typ}]")


def uebung_hinzufuegen(uebungen: list) -> list:
    """
    Fügt eine neue Übung zur Übungsliste hinzu.

    Args:
        uebungen (list): Bestehende Übungsliste

    Returns:
        list: Aktualisierte Übungsliste
    """
    print("\n➕ NEUE ÜBUNG")
    name = eingabe_text("Übungsname: ")

    # Prüfen ob Übung bereits existiert
    for u in uebungen:
        if u["name"].lower() == name.lower():
            print("⚠️  Diese Übung existiert bereits.")
            return uebungen

    print("Typ der Übung:")
    print("  1 – mit Gewicht (z.B. Bankdrücken)")
    print("  2 – Zwischenübung ohne Gewicht (z.B. Stretching, Plank)")
    typ_wahl = eingabe_text("Wahl (1/2): ")
    typ = "mit Gewicht" if typ_wahl == "1" else "ohne Gewicht"

    uebungen.append({"name": name, "typ": typ})
    daten_speichern(UEBUNGEN_DATEI, uebungen)
    print(f"✅ Übung '{name}' gespeichert.")
    return uebungen


def uebung_loeschen(uebungen: list) -> list:
    """
    Löscht eine Übung aus der Liste.

    Args:
        uebungen (list): Bestehende Übungsliste

    Returns:
        list: Aktualisierte Übungsliste
    """
    uebungen_anzeigen(uebungen)
    if not uebungen:
        return uebungen

    eingabe = eingabe_zahl("Nummer der Übung zum Löschen (0 = Abbrechen): ", min_wert=0)
    index = int(eingabe) - 1

    if eingabe == 0:
        return uebungen

    if 0 <= index < len(uebungen):
        entfernt = uebungen.pop(index)
        daten_speichern(UEBUNGEN_DATEI, uebungen)
        print(f"✅ Übung '{entfernt['name']}' gelöscht.")
    else:
        print("⚠️  Ungültige Nummer.")

    return uebungen


def uebungen_verwalten() -> None:
    """Menü zur Übungsverwaltung."""
    uebungen = daten_laden(UEBUNGEN_DATEI)

    while True:
        trennlinie_ausgeben()
        print("🗂️  ÜBUNGEN VERWALTEN")
        trennlinie_ausgeben()
        uebungen_anzeigen(uebungen)
        print("\n1 – Neue Übung hinzufügen")
        print("2 – Übung löschen")
        print("0 – Zurück zum Hauptmenü")
        trennlinie_ausgeben()

        wahl = eingabe_text("Wahl: ")

        if wahl == "1":
            uebungen = uebung_hinzufuegen(uebungen)
        elif wahl == "2":
            uebungen = uebung_loeschen(uebungen)
        elif wahl == "0":
            break
        else:
            print("⚠️  Ungültige Wahl.")


# ──────────────────────────────────────────────────────────────
# TRAINING EINTRAGEN
# ──────────────────────────────────────────────────────────────

def uebung_erfassen(uebungen: list) -> dict:
    """
    Erfasst eine einzelne Übung für die Trainingseinheit.

    Args:
        uebungen (list): Liste aller verfügbaren Übungen

    Returns:
        dict: Erfasste Übungsdaten
    """
    uebungen_anzeigen(uebungen)
    print("\nÜbung auswählen (Nummer) oder 0 für neue Übung:")
    auswahl = eingabe_zahl("Auswahl: ", min_wert=0)
    index = int(auswahl) - 1

    if auswahl == 0:
        uebungen = uebung_hinzufuegen(uebungen)
        daten_speichern(UEBUNGEN_DATEI, uebungen)
        index = len(uebungen) - 1

    if not (0 <= index < len(uebungen)):
        print("⚠️  Ungültige Auswahl.")
        return None

    ausgewaehlte_uebung = uebungen[index]
    print(f"\n📌 {ausgewaehlte_uebung['name']} ({ausgewaehlte_uebung['typ']})")

    eintrag = {"uebung": ausgewaehlte_uebung["name"]}

    if ausgewaehlte_uebung["typ"] == "mit Gewicht":
        eintrag["gewicht_kg"] = eingabe_zahl("Gewicht (kg): ", min_wert=0)
        eintrag["wiederholungen"] = int(eingabe_zahl("Wiederholungen: ", min_wert=1))
        eintrag["saetze"] = int(eingabe_zahl("Sätze: ", min_wert=1))
        eintrag["rpe"] = eingabe_zahl("RPE (1–10, leer = überspringen): ", min_wert=1, max_wert=10, erlaubt_leer=True)
    else:
        # Zwischenübung ohne Gewicht
        dauer = input("Dauer (z.B. '30 Sek', '2 Min', leer = überspringen): ").strip()
        eintrag["dauer"] = dauer if dauer else None

    return eintrag


def mindset_erfassen() -> dict:
    """
    Erfasst die Mindset-Daten (Stimmung, Energielevel, Freitext).

    Returns:
        dict: Mindset-Daten
    """
    trennlinie_ausgeben()
    print("🧠 MINDSET ERFASSEN")
    trennlinie_ausgeben()

    print("Stimmung:")
    for key, wert in STIMMUNGEN.items():
        print(f"  {key} – {wert}")
    stimmung_wahl = eingabe_text("Deine Stimmung (1/2/3): ")
    stimmung = STIMMUNGEN.get(stimmung_wahl, "😐 Neutral")

    energielevel = int(eingabe_zahl("Energielevel (1–5): ", min_wert=1, max_wert=5))

    print("Wie lief das Training? (Freitext, leer = überspringen)")
    freitext = input("→ ").strip()

    return {
        "stimmung": stimmung,
        "energielevel": energielevel,
        "freitext": freitext if freitext else None
    }


def training_eintragen() -> None:
    """Erfasst eine komplette Trainingseinheit mit Übungen und Mindset."""
    uebungen = daten_laden(UEBUNGEN_DATEI)
    trainings = daten_laden(TRAININGS_DATEI)

    trennlinie_ausgeben()
    print("🏋️  NEUE TRAININGSEINHEIT")
    trennlinie_ausgeben()

    if not uebungen:
        print("ℹ️  Noch keine Übungen vorhanden. Füge zuerst Übungen hinzu.")
        uebungen = uebung_hinzufuegen(uebungen)

    erfasste_uebungen = []

    # Iteration: mehrere Übungen hinzufügen (Schleife)
    weitere_uebungen = True
    while weitere_uebungen:
        eintrag = uebung_erfassen(uebungen)
        if eintrag:
            erfasste_uebungen.append(eintrag)
            print(f"✅ '{eintrag['uebung']}' erfasst.")

        # Selektion: weitere Übungen hinzufügen?
        antwort = eingabe_text("\nWeitere Übung hinzufügen? (j/n): ").lower()
        weitere_uebungen = antwort == "j"

    # Notizen
    print("\n📝 Notizen (optional, leer = überspringen):")
    notizen = input("→ ").strip()

    # Mindset erfassen
    mindset = mindset_erfassen()

    # Datum automatisch setzen
    datum = datum_jetzt()

    # Training zusammenstellen
    neues_training = {
        "datum": datum,
        "uebungen": erfasste_uebungen,
        "notizen": notizen if notizen else None,
        "mindset": mindset
    }

    # Speichern
    trainings.append(neues_training)
    daten_speichern(TRAININGS_DATEI, trainings)

    trennlinie_ausgeben()
    print(f"✅ Training vom {datum} gespeichert!")
    print(f"   Übungen: {len(erfasste_uebungen)}")
    print(f"   Stimmung: {mindset['stimmung']}")
    print(f"   Energielevel: {mindset['energielevel']}/5")
    trennlinie_ausgeben()


# ──────────────────────────────────────────────────────────────
# VERLAUF ANSEHEN
# ──────────────────────────────────────────────────────────────

def training_details_anzeigen(training: dict) -> None:
    """
    Zeigt die Details einer einzelnen Trainingseinheit an.

    Args:
        training (dict): Trainingseinheit
    """
    trennlinie_ausgeben()
    print(f"📅 {training['datum']}")
    trennlinie_ausgeben()

    print("🏋️  Übungen:")
    for u in training["uebungen"]:
        if "gewicht_kg" in u:
            rpe = f"  RPE: {u['rpe']}" if u.get("rpe") else ""
            print(f"  • {u['uebung']}: {u['gewicht_kg']} kg × {u['wiederholungen']} Wdh. × {u['saetze']} Sätze{rpe}")
        else:
            dauer = f" – {u['dauer']}" if u.get("dauer") else ""
            print(f"  • {u['uebung']}{dauer}")

    if training.get("notizen"):
        print(f"\n📝 Notizen: {training['notizen']}")

    mindset = training.get("mindset", {})
    if mindset:
        print(f"\n🧠 Mindset:")
        print(f"  Stimmung:    {mindset.get('stimmung', '–')}")
        print(f"  Energielevel: {mindset.get('energielevel', '–')}/5")
        if mindset.get("freitext"):
            print(f"  Notiz:       {mindset['freitext']}")


def verlauf_ansehen() -> None:
    """Zeigt den Trainingsverlauf an und ermöglicht Detailansicht."""
    trainings = daten_laden(TRAININGS_DATEI)

    trennlinie_ausgeben()
    print("📚 TRAININGSVERLAUF")
    trennlinie_ausgeben()

    if not trainings:
        print("Noch keine Trainings vorhanden.")
        return

    # Liste aller Trainings anzeigen
    for i, t in enumerate(reversed(trainings), 1):
        mindset = t.get("mindset", {})
        stimmung = mindset.get("stimmung", "–")
        energie = mindset.get("energielevel", "–")
        anzahl = len(t.get("uebungen", []))
        print(f"  {i}. {t['datum']}  | {anzahl} Übungen | {stimmung} | Energie: {energie}/5")

    print("\n0 – Zurück")
    print("Nummer eingeben für Details:")
    auswahl = eingabe_zahl("Auswahl: ", min_wert=0)

    if auswahl == 0:
        return

    index = len(trainings) - int(auswahl)
    if 0 <= index < len(trainings):
        training_details_anzeigen(trainings[index])
    else:
        print("⚠️  Ungültige Auswahl.")


# ──────────────────────────────────────────────────────────────
# MINDSET ÜBERSICHT
# ──────────────────────────────────────────────────────────────

def mindset_uebersicht() -> None:
    """Zeigt den Stimmungsverlauf und Trends an."""
    trainings = daten_laden(TRAININGS_DATEI)

    trennlinie_ausgeben()
    print("🧠 MINDSET ÜBERSICHT")
    trennlinie_ausgeben()

    if not trainings:
        print("Noch keine Daten vorhanden.")
        return

    # Filter nach Datum (optional)
    print("Filter nach Datum? (leer = alle anzeigen)")
    filter_datum = input("Datum (YYYY-MM, z.B. 2025-01): ").strip()

    eintraege_mit_mindset = []
    for t in trainings:
        if filter_datum and not t["datum"].startswith(filter_datum):
            continue
        if t.get("mindset"):
            eintraege_mit_mindset.append(t)

    if not eintraege_mit_mindset:
        print("Keine Einträge für diesen Zeitraum.")
        return

    # Stimmungsverlauf anzeigen
    print(f"\nStimmungsverlauf ({len(eintraege_mit_mindset)} Einträge):\n")
    for t in eintraege_mit_mindset:
        m = t["mindset"]
        print(f"  {t['datum']}  {m.get('stimmung', '–')}  Energie: {m.get('energielevel', '–')}/5")
        if m.get("freitext"):
            print(f"            → {m['freitext']}")

    # Trends erkennen
    energie_werte = [
        t["mindset"]["energielevel"]
        for t in eintraege_mit_mindset
        if isinstance(t["mindset"].get("energielevel"), (int, float))
    ]

    if energie_werte:
        durchschnitt = sum(energie_werte) / len(energie_werte)
        trennlinie_ausgeben()
        print("📈 TRENDS")
        print(f"  Durchschnittliches Energielevel: {durchschnitt:.1f}/5")
        print(f"  Höchstes Energielevel:           {max(energie_werte)}/5")
        print(f"  Niedrigstes Energielevel:        {min(energie_werte)}/5")

    input("\nWeiter mit Enter...")


# ──────────────────────────────────────────────────────────────
# HAUPTMENÜ
# ──────────────────────────────────────────────────────────────

def hauptmenue_anzeigen(benutzer: dict) -> None:
    """Zeigt das Hauptmenü an."""
    trennlinie_ausgeben()
    name = benutzer.get("name", "Gast")
    print(f"🏋️  TRAININGSAPP  |  {name}")
    trennlinie_ausgeben()
    print("1 – Training eintragen")
    print("2 – Verlauf ansehen")
    print("3 – Mindset Übersicht")
    print("4 – Übungen verwalten")
    print("5 – Abmelden")
    print("0 – Beenden")
    trennlinie_ausgeben()


def hauptprogramm() -> None:
    """Hauptschleife der Applikation (PAP: Start → Login → Hauptmenü → Funktionen → Ende)."""

    # Nutzerstatus prüfen (Selektion: eingeloggt?)
    benutzer = nutzerstatus_pruefen()

    if not benutzer:
        # Nein → Login / Gastmodus
        benutzer = login_oder_gastmodus()
    else:
        # Ja → direkt zum Hauptmenü
        print(f"✅ Willkommen zurück, {benutzer.get('name', 'Gast')}!")

    # Hauptmenü-Schleife (Iteration)
    laeuft = True
    while laeuft:
        hauptmenue_anzeigen(benutzer)
        wahl = eingabe_text("Wahl: ")

        if wahl == "1":
            training_eintragen()
        elif wahl == "2":
            verlauf_ansehen()
        elif wahl == "3":
            mindset_uebersicht()
        elif wahl == "4":
            uebungen_verwalten()
        elif wahl == "5":
            abmelden()
            benutzer = login_oder_gastmodus()
        elif wahl == "0":
            print("\n👋 Auf Wiedersehen! Bleib stark! 💪")
            laeuft = False
        else:
            print("⚠️  Ungültige Wahl. Bitte 0–5 eingeben.")

    # Ende


# ──────────────────────────────────────────────────────────────
# EINSTIEGSPUNKT
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    hauptprogramm()
