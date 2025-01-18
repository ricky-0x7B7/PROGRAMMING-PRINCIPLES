"""
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Riccardo ZOLA - matricola S00005824
Facoltà di Computer Science & Artifical Intelligence
EPICODE Institute of Technology - Malta
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
A.A. 2024/25 // Primo Semestre
Progetto di PROGRAMMING PRINCIPLES 
appello del 31/01/2025
compito assegnato: creare una classe e relativi metodi (18 esercizi)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""


# Importa il modulo necessario a manipolare i file di tipo JSON
import json


# Definisce il metodo costruttore
class MovieLibrary:
    class MovieNotFoundError(Exception):
        pass


    # Inizializza la libreria con il file specificato (gestendo le eccezioni)
    def __init__(self, json_file):
        self.json_file = json_file
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                self.movies = json.load(file)
        except FileNotFoundError: # gestisce nel caso il file non esista
            raise FileNotFoundError(
                f"\n⛔ Oops... file non trovato! --> {self.json_file}\n")
        except json.JSONDecodeError: # gestisce nel caso il file presenti errori di codifica
            raise ValueError(
                f"\n⛔ Oops... errore nel decodificare il file JSON! --> {self.json_file}.\n")
        except UnicodeDecodeError: # gestisce nel caso il file sia di un formato sbagliato
            raise ValueError(
                f"\n⛔ Il file '{self.json_file}' non è un file JSON valido o non è codificato in UTF-8.\n")

    
    # Aggiorna il file JSON con l'attributo movies corrente
    def __update_json_file(self): 

        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file, indent=4, ensure_ascii=False)


    # DRY / Normalizza gli input case insensitive e rimuove gli spazi ridondanti
    def __normalize_input(self, value): # definisce il metodo con il relativo attributo
        if isinstance(value, str):
            # Rimuove spazi multipli, normalizza in minuscolo
            return ' '.join(value.split()).lower()
        return value

    # (Esercizio 1) Restituisce l'intera collezione di film
    def get_movies(self):
        return self.movies


    # (Esercizio 2) Aggiunge un nuovo film alla collezione
    def add_movie(self, title, director, year, genres): # definisce il metodo con i relativi attributi

        new_movie = {
            "title": title,
            "director": director,
            "year": year,
            "genres": genres
        }
        self.movies.append(new_movie) # aggiunge il nuovo dizionario del film alla lista di dizionari
        self.__update_json_file() # richiama il metodo di aggiornamento del file JSON


    # (Esercizio 3) Rimuove un film dalla collezione in base al titolo
    def remove_movie(self, title): # definisce il metodo con il relativo attributo

        normalized_title = self.__normalize_input(
            title)  # Normalizza il titolo in input
        removed_movie = None

        # Cerca il film in base al titolo
        for movie in self.movies:
            # Confronto normalizzato
            if self.__normalize_input(movie['title']) == normalized_title:
                removed_movie = movie
                break
        if removed_movie:
            self.movies.remove(removed_movie)  # Rimuove il film dalla lista
            self.__update_json_file()  # richiama il metodo di aggiornamento del file JSON
            return removed_movie
        else:
            # Lancia un'eccezione se il film non è stato trovato
            raise self.MovieNotFoundError("Movie was not found")


    # (Esercizio 4) Aggiorna un film nella collezione in base al titolo
    def update_movie(self, title, director=None, year=None, genres=None): # definisce il metodo con i relativi attributi

        normalized_title = self.__normalize_input(
            title)  # Normalizza il titolo in input
        for movie in self.movies:
            # Confronto normalizzato (se vuoto, lascia invariato)
            if self.__normalize_input(movie['title']) == normalized_title:
                if director is not None:
                    movie['director'] = director
                if year is not None:
                    movie['year'] = year
                if genres is not None:
                    movie['genres'] = genres
                self.__update_json_file() # richiama il metodo di aggiornamento del file JSON
                return movie
        return None


    # (Esercizio 5) Restituisce una lista contenente tutti i titloi dei film
    def get_movie_titles(self): # definisce il metodo
        return [movie['title'] for movie in self.movies]

    # (Esercizio 6) Restituisce il numero totale dei film nella collezione
    def count_movies(self): # definisce il metodo
        return len(self.movies) 


    # (Esercizio 7) Restituisce il film con il titolo corrispondente
    def get_movie_by_title(self, title): # definisce il metodo con il relativo attributo
        normalized_title = self.__normalize_input(title) # input normalizzato non case sensitive
        for movie in self.movies:
            # Confronto normalizzato
            if self.__normalize_input(movie['title']) == normalized_title:
                return movie
        return None


    # (Esercizio 8) Restituisce tutti i film che contengono la sottostringa nel titolo (case sensitive)
    def get_movies_by_title_substring(self, substring): # definisce il metodo con il relativo attributo
        return [movie for movie in self.movies if substring in movie['title']]


    # (Esercizio 9) Filtra i film per anno
    def get_movies_by_year(self, year):
        try: # verifica l'input e gestisce l'eccezione
            year = int(year)  # Converte l'input in un intero
        except ValueError:
            raise ValueError(
                f"⛔ L'anno fornito ('{year}') non è valido. Deve essere un numero.")
        
        return [movie['title'] for movie in self.movies if movie['year'] == year]


    # (Esercizio 10) Restituisce il numero totale di film del regista specificato (ncs)
    def count_movies_by_director(self, director): # definisce il metodo con il relativo attributo
        normalized_director = self.__normalize_input(director)  # Normalizza il regista in input
        return sum(1 for movie in self.movies if self.__normalize_input(movie['director']) == normalized_director)


    # (Esercizio 11) Restituisce una lista dei film corrispondenti al genere specificato (ncs)
    def get_movies_by_genre(self, genre): # definisce il metodo con il relativo attributo
        normalized_genre = self.__normalize_input(genre)  # Normalizza il genere in input
        return [
            movie['title'] for movie in self.movies
            if normalized_genre in (self.__normalize_input(g) for g in movie['genres'])
        ]


    # (Esercizio 12) Restituisce il titolo del film più antico della collezione
    def get_oldest_movie_title(self): # definisce il metodo
        if not self.movies: # gestisce la lista vuota 
            return None
        oldest_movie = min(self.movies, key=lambda movie: movie['year']) # ricerca il solo anno più remoto
        return oldest_movie['title'] # ritorna il relativo titolo


    # (Esercizio 13) Restituisce la media aritmetica degli anni di pubblicazione dei film
    def get_average_release_year(self): # definisce il metodo
        if not self.movies: # gestisce la lista vuota 
            return 0.0
        total_years = sum(movie['year'] for movie in self.movies) # calcola la somma degli anni di tutti i titoli
        return total_years / len(self.movies) # ritorna la media aritmetica in floating point


    # (Esercizio 14) Restituisce il titolo più lungo della collezione di film
    def get_longest_title(self): # definisce il metodo
        if not self.movies: # gestisce la lista vuota 
            return None
        longest_title_movie = max(
            self.movies, key=lambda movie: len(movie['title'])) # ricerca il titolo più lungo
        return longest_title_movie['title'] 

    # (Esercizio 15) Restituisce i titoli dei film pubblicati tra start_year ed end_year (inclusi)
    def get_titles_between_years(self, start_year, end_year): # definisce il metodo con i relativi attributi
        return [movie['title'] for movie in self.movies if start_year <= movie['year'] <= end_year] # popola la lista con i soli film inclusi nellíntervallo

    # (Esercizuo 16) Restituisce l'anno che si ripete più spesso fra i film della collezione
    def get_most_common_year(self): # definisce il metodo
        if not self.movies: # gestisce la lista vuota
            return None
        year_counts = {}
        for movie in self.movies: # itera la lista ed aggiorna il contatore delle occorrenze
            year = movie['year']
            year_counts[year] = year_counts.get(year, 0) + 1
        most_common_year = max(year_counts, key=year_counts.get) # determina l'anno più frequente
        return most_common_year


if __name__ == "__main__":
    # Questo codice viene eseguito solo se il file viene eseguito direttamente,
    # ma non viene eseguito quando il file viene importato.
    # (per l'integrazione col modulo di controllo menu.py)
    pass
