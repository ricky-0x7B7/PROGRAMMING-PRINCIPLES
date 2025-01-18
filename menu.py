"""
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Riccardo ZOLA - matricola S00005824
Facoltà di Computer Science & Artifical Intelligence
EPICODE Institute of Technology - Malta
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
A.A. 2024/25 // Primo Semestre
Progetto di PROGRAMMING PRINCIPLES 
appello del 31/01/2025
Modulo di controllo e verifica della classe e dei metodi assegnati
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""

import os
import platform
from movie_library import MovieLibrary


# Pulisce la console per migliorare la leggibilità del menù (cross-platform)
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


# Attende che l'utente prema ENTER prima di tornare al menù principale (DRY)
def wait_for_input():
    input("\n⌛ --> Premi ENTER per tornare al menù principale <--")


"""
MENÙ INTERATTIVO
"""

# VOCE MENÙ n.1: mostra tutti i film presenti nella collezione.
def voce_menu_1(library):

    movies = library.get_movies() # importa l'intero dizionario col metodo della libreria
    if movies:
        print("\nEcco la tua collezione di film:\n")
        for movie in movies:
            print(movie)
    else:
        print("\nLa collezione è vuota.\n") # Se la collezione è vuota, avvisa l'utente
    wait_for_input()

# VOCE MENÙ n.2: aggiunge un nuovo film alla collezione
def voce_menu_2(library):
    try:
        # Riceve gli input ed avvisa in caso di errori
        title = input("Inserisci il titolo: ").strip()
        if not title:
            raise ValueError("Il titolo non può essere vuoto.") 
        director = input("Inserisci il regista: ").strip()
        if not director:
            raise ValueError("Il regista non può essere vuoto.") 
        year = input("Inserisci l'anno di uscita: ").strip()
        if not year.isdigit():
            raise ValueError("L'anno deve essere un numero intero.") 
        genres = input("Inserisci i generi del film (separati da una virgola): ").strip()
        if not genres:
            raise ValueError("I generi non possono essere vuoti.")

        # Applica regole di formattazione ai dati inseriti dall'utente
        title = ' '.join(title.split())  # Rimuove gli spazi in eccesso prima, dopo e dentro la stringa
        director = ' '.join(director.split()).title()  # Rimuove gli spazi e formatta in Title Case (iniziali maiuscole)
        year = int(year) # Converte in numero intero
        genres_list = [' '.join(genre.strip().split()).title() for genre in genres.split(',')]  # Gestisce come lista e formatta ogni genere in Title Case (iniziali maiuscole)

        # Aggiunge il film utilizzando il metodo della classe MovieLibrary e ne dà conferma all'utente
        library.add_movie(title, director, year, genres_list)
        print(f"\n✅ Film aggiunto con successo:\n '{title}' di {director} ({year}), Generi: {genres_list}\n")

    except ValueError as e: # Gestisce gli eventuali errori
        print(f"\n⛔ Errore: {e}\n")

    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.3: rimuove un film dalla collezione
def voce_menu_3(library):
    
    # Riceve gli input ed avvisa in caso di errori
    title = input("Inserisci il titolo (vuoto per tornare al menù): ").strip()
    normalized_title = library._MovieLibrary__normalize_input(title)  # Normalizza il titolo (solo per l'output)
    if not title: 
        print(f"\n⛔ Film non trovato: \"{normalized_title}\"\n Non è stato rimosso alcun titolo!")
        return
    try:
        removed_movie = library.remove_movie(title) # Informa l'utente del buon esito della rimozione
        print(f"✅ Film rimosso con successo: {removed_movie['title']}")
    except MovieLibrary.MovieNotFoundError as e: 
        print(f"⛔️ Errore: {e}")

    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.4: aggiorna un titolo esistente nella collezione
def voce_menu_4(library):
    try:
        # Riceve il titolo del film da aggiornare
        title = input("Inserisci il titolo che vuoi aggiornare: ").strip()
        normalized_title = library._MovieLibrary__normalize_input(title)  # Normalizza il titolo (solo per l'output)
        retrieved = library.get_movie_by_title(title)

        # Controlla se il film esiste
        if retrieved:
            print(f"\n🎥 Film trovato: \"{normalized_title}\"\n")

            # Riceve gli input per i campi da aggiornare
            director = input("Inserisci il regista (vuoto per lasciare invariato): ").strip()
            year = input("Inserisci l'anno di uscita (vuoto per lasciare invariato): ").strip()
            genres = input("Inserisci i generi del film (separati da una virgola // vuoto per lasciare invariato): ").strip()

            # Applica le regole di formattazione solo se il campo non è vuoto
            director = ' '.join(director.split()).title() if director else None
            year = int(year) if year else None
            genres_list = [' '.join(genre.strip().split()).title() for genre in genres.split(',')] if genres else None

            # Aggiorna il film utilizzando il metodo della classe
            updated_movie = library.update_movie(title, director, year, genres_list)

            # Avvisa l'utente sull'esito dell'aggiornamento
            if updated_movie:
                print(f"\n✅ Film aggiornato con successo:\n \"{normalized_title}\"\n") 
            else:
                print("\n⛔ Impossibile aggiornare il film.\n") 
        else: # Avvisa l'utente se il film non è presente nella collezione
            print(f"\n⛔ Film non trovato nella collezione: \"{normalized_title}\"n")

    except ValueError as e: # Gestisce altri errori
        print(f"\n⛔ Errore: {e}\n")

    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.5: elenca i titoli presenti in collezione
def voce_menu_5(library):

    titles = library.get_movie_titles() # Carica l'elenco dei film utilizzando il metodo della classe
    if titles: # se presenti, li elenca
        print("\nEcco l'elenco dei titoli presenti in collezione:\n")
        for title in sorted(titles):
            print(title)
    else: # se la collezione è vuota, avvisa l'utente
        print("\nLa collezione è vuota.\n")
    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.6: fornmisce dettagli su uno specifico titolo
def voce_menu_6(library):

    title = input("Inserisci il titolo di tuo interesse: ")
    normalized_title = library._MovieLibrary__normalize_input(title)  # Normalizza il titolo (solo per l'output)
    retrieved = library.get_movie_by_title(title) # Carica il dizionario del film utilizzando il metodo della classe
    if retrieved:
        print(f"\n✅ Ecco i dettagli del film \"{normalized_title}\":\n") 
        print(f"{retrieved}\n")
    else:
        print(f"\n🤷🏽‍♂️ Non ho trovato nessun film con titolo \"{normalized_title}\".\n")  # Avvisa l'utente se il film non è presente nella collezione

    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.7: cerca i titoli che includono una stringa di ricerca
def voce_menu_7(library):

    text = input("Inserisci il testo da ricercare dei titoli: ") # raccoglie l'input e lo tratta come case sensitive (nessuna normalizzazione)
    movies = library.get_movies_by_title_substring(text) # Carica la lista dei film utilizzando il metodo della classe
    if movies:
        print(f"\nEcco l'elenco dei titoli presenti in collezione \nche contengono nel titolo la stringa \"{text}\":\n") 
        # Ordina i film per titolo
        for movie in sorted(movies, key=lambda m: m['title']):
            print(movie['title'])
    else:
        print(f"\nLa collezione non comprende film che contengono la stringa \"{text}\" nel titolo.\n")  # Avvisa l'utente se la lista è vuota
    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.8: elenca i titoli prodotti in uno specifico anno
def voce_menu_8(library):

    year = input("Inserisci l'anno di tuo interesse: ")
    movies = library.get_movies_by_year(year) # importa l'elenco col metodo della libreria
    if movies:
        print(f"\nEcco l'elenco dei titoli presenti in collezione dell'anno {year}:\n") 
        # Ordina i film per titolo
        for movie in sorted(movies):
            print(movie)
    else:
        print(f"\nLa collezione non comprende film dell'anno {year}.\n") # Avvisa l'utente se la lista è vuota

    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.9: elenca i film di un dato regista
def voce_menu_9(library):

    director = input("Inserisci il regista di tuo interesse: ")
    normalized_director = library._MovieLibrary__normalize_input(director)  # Normalizza il regista (solo per l'output)
    retrieved = library.count_movies_by_director(director) # importa l'elenco col metodo della libreria
    if retrieved:
        print(f"\n✅ In collezione sono presenti {retrieved} film del regista {normalized_director}.\n")
    else:
        print(f"\n🤷🏽‍♂️ Non ho trovato nessun titolo associato al regista {normalized_director}.\n")

    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)


# VOCE MENÙ n.10: elenca i film di un dato genere
def voce_menu_10(library):

    genre = input("Inserisci il genere di tuo interesse: ")
    normalized_genre = library._MovieLibrary__normalize_input(genre)  # Normalizza il genere (solo per l'output)
    movies = library.get_movies_by_genre(genre) # importa l'elenco col metodo della libreria
    if movies:
        print(f"\nEcco l'elenco dei titoli presenti in collezione del genere {normalized_genre}:\n")
        # Ordina i film per titolo
        for movie in sorted(movies):
            print(movie)
    else:
        print(f"\nLa collezione non comprende film del genere {genre}.\n")
    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.11: filtra i film prodotti in un range di anni (estremi inclusi)
def voce_menu_11(library):

    try: # riceve gli input e gestisce le eccezioni
        
        year_from = input("Inserisci l'anno iniziale di ricerca: ").strip() # Riceve l'anno iniziale
        if not year_from:
            raise ValueError("Il valore non può essere vuoto.")
        year_from = int(year_from)  # Verifica se è convertibile in un intero
        
        year_to = input("Inserisci l'anno finale di ricerca: ").strip() # Riceve l'anno finale
        if not year_to:
            raise ValueError("Il valore non può essere vuoto.")
        year_to = int(year_to)  # Verifica se è convertibile in un intero

        movies = library.get_titles_between_years(year_from, year_to) # importa l'elenco col metodo della libreria
        if movies:
            print(f"\n🎥 Film pubblicati tra {year_from} e {year_to}:\n")
            for title in sorted(movies): # Ordina alfabneticamente
                print(f" - {title}")
        else:
            print(f"\n🤷‍♂️ Non sono stati trovati film pubblicati tra il {year_from} ed il {year_to}.\n") # Informa l'utente se la ricerca non ha prodotto rislutati

    except ValueError as e:
        print(f"\n⛔ Errore: {e}. Assicurati di inserire numeri validi.\n") # Gestisce errori di datatypoe

    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)

# VOCE MENÙ n.12: elenca varie statistiche per il controllo dei restanti metodi della classe
def voce_menu_12(library):

    print("\n")
    print(f"⭐ La collezione comprende {library.count_movies()} film.")
    print(f"⭐ Il film più vecchio è \"{library.get_oldest_movie_title()}\".")
    print(f"⭐ La media artimetica degli anni di pubblicazione è {library.get_average_release_year():.2f} ")
    print(f"⭐ Il film con il titolo più lungo è \"{library.get_longest_title()}\".")
    print(f"⭐ L'anno di pubblicazione più popolato della collezione è il {library.get_most_common_year()}.\n")

    # Conta e stampa il numero di film diretti da ciascun regista
    print("Film di ciascun regista della collezione:")
    directors = set(movie['director'] for movie in library.get_movies())  # Ottiene l'elenco unico dei registi
    for director in sorted(directors):  # Ordina i registi alfabeticamente
        count = library.count_movies_by_director(director)
        print(f" 🎥 {director}: {count} film")

    wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)


# Istanza del menù principale (chiede in avvio il file JSON sorgente)
def main_menu(): 
    clear_screen()  # Pulisce lo schermo prima di chiedere l'input
    print("--------------------------------------------------------------\n")
    print(" Benvenutə nella Movie Collection di s00005824@epicode.edu.mt\n")
    print("--------------------------------------------------------------\n")
    json_file = input(" Inserisci il nome del file JSON:  ") 

    # Prova a creare l'istanza della libreria e gestisce le eccezioni
    try:
        library = MovieLibrary(json_file)
    except FileNotFoundError as e:
        print(e)
        return
    except ValueError as e:
        print(e)
        return

    # Legge il banner ASCII-ART dal file esterno
    try:
        with open("testo-ASCII.txt", "r") as ascii_file:
            ascii_art = ascii_file.read()
    except FileNotFoundError:
        ascii_art = "--- Movie Collection Menu ---" # Alternativa di backup se decorazione ASCII non presente

    # Definisce il dizionario delle opzioni del menù
    opzioni = {
        1: (" 🎬 Esplora l'intera collezione di film", lambda: voce_menu_1(library)),
        2: (" ➕ Aggiungi un film alla collezione", lambda: voce_menu_2(library)),
        3: (" ➖ Rimuovi un film dalla collezione", lambda: voce_menu_3(library)),
        4: (" 🔄 Aggiorna un film della collezione", lambda: voce_menu_4(library)),
        5: (" 🗂️ Elenco dei titoli", lambda: voce_menu_5(library)),
        6: (" 🔎 Cerca per titolo", lambda: voce_menu_6(library)),
        7: (" 🔎 Cerca dentro al titolo", lambda: voce_menu_7(library)),
        8: (" 🔎 Cerca per anno", lambda: voce_menu_8(library)),
        9: (" 🔎 Cerca per regista", lambda: voce_menu_9(library)),
        10: ("🔎 Cerca per genere", lambda: voce_menu_10(library)),
        11: ("🔎 Cerca in un intervallo temporale", lambda: voce_menu_11(library)),
        12: ("📊 Statistiche", lambda: voce_menu_12(library)),
        99: ("👋🏼 Esci", None)
    }

    # MENÙ INTERATTIVO
    while True:
        clear_screen()  # Pulisce lo schermo prima di mostrare il menù
        retrieved = library.count_movies()  # Conta il numero totale di film
        print(ascii_art) # Stampa il banner in ASCII ART
        print(f"\nLa collezione al momento comprende --> {retrieved} titoli.") # informa sul totale record del database JSON
        print("\nSCEGLI UN'OPZIONE:\n")
        for numero, (descrizione, _) in opzioni.items(): # Crea il menù in base al dizioniario delle opzioni
            print(f"{numero}. {descrizione}")

        scelta = input("\nInserisci il numero della tua scelta: ").strip() # Raccoglie la scelta dell'utente

        # routing del menù, con gestione delle eccezini
        if scelta.isdigit():
            scelta = int(scelta)
            if scelta in opzioni:
                descrizione, voce_menu = opzioni[scelta]
                if voce_menu:
                    clear_screen()
                    print(f"Hai scelto: {descrizione}")
                    voce_menu()
                else:
                    print("\n✅ Sei uscito dal programma.\n🎬 Ci vediamo prossimamente su questi schermi!\n")
                    break
            else:
                print("Scelta non valida. Inserisci un numero tra 1 e 10.")
                wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)
        else:
            print("Inserisci un numero valido.")
            wait_for_input() # attende un ENTER prima di tornare al menù (cancellando la console)


if __name__ == "__main__":
    main_menu()
