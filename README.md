# Szablon dokumentacji projektu (LaTeX)

Szablon służy do przygotowania raportu z projektu realizowanego w ramach zajęć. Obsługuje projekty indywidualne i zespołowe.

## Spis treści

- [Powiązany szablon pracy dyplomowej](#powiązany-szablon-pracy-dyplomowej)
- [Szybki start](#szybki-start)
- [Autorzy projektu](#autorzy-projektu)
- [Tryb roboczy i końcowy](#tryb-roboczy-i-końcowy)
- [Struktura raportu](#struktura-raportu)
- [Rysunki, jednostki i kod](#rysunki-jednostki-i-kod)
- [Polskie znaki w listingach](#polskie-znaki-w-listingach)
- [Kompilacja](#kompilacja)
  - [Wymagania lokalne w systemie Windows](#wymagania-lokalne-w-systemie-windows)
  - [Budowanie dokumentu](#budowanie-dokumentu)
  - [TeXstudio](#texstudio)
- [Gotowe paczki ZIP](#gotowe-paczki-zip)

## Powiązany szablon pracy dyplomowej

Szablon dokumentacji projektu wykorzystuje konwencje opracowane dla
[szablonu pracy dyplomowej](https://github.com/EduKowol/SZABLON-Pracy-Dyplomowej),
ale ma uproszczoną strukturę dostosowaną do projektów realizowanych w ramach
zajęć. Przy przygotowywaniu pracy inżynierskiej, magisterskiej lub doktorskiej
należy skorzystać z repozytorium
[EduKowol/SZABLON-Pracy-Dyplomowej](https://github.com/EduKowol/SZABLON-Pracy-Dyplomowej).

## Szybki start

Do zalecanej kompilacji lokalnej w systemie Windows potrzebne są **MiKTeX oraz
Perl**, ponieważ używany przez szablon program `latexmk` jest skryptem napisanym
w Perlu. Można zainstalować np. [Strawberry Perl](https://strawberryperl.com/),
a następnie zamknąć i ponownie uruchomić terminal oraz edytor LaTeX. Prism,
Overleaf i podobne edytory internetowe nie wymagają instalowania Perla na
komputerze użytkownika.

1. Uzupełnij `config/metadata.tex`, zwłaszcza tytuł, przedmiot, prowadzącego i autorów.
2. Zastąp teksty instruktażowe w `chapters/` własną treścią.
3. Dodaj źródła do `bibliografia.bib` i cytuj je przez `\cite{klucz}`.
4. Uruchom `latexmk main.tex`.

Gotowy dokument powstanie jako `build/main.pdf`.

## Autorzy projektu

Autorów wpisuje się w `\projectauthors`. Każdy wiersz zawiera imię i nazwisko oraz numer albumu:

```tex
\newcommand{\projectauthors}{%
  Anna Nowak & 123456 \\
  Jan Kowalski & 234567 \\
}
\newcommand{\projectpdfauthors}{Anna Nowak, Jan Kowalski}
```

## Tryb roboczy i końcowy

Podczas pracy pozostaw `\projectstatus` ustawiony na `draft`. Przed oddaniem zmień wartość na `final`; brak podstawowych metadanych spowoduje wtedy błąd kompilacji.

## Struktura raportu

- wprowadzenie;
- cel, zakres i wymagania;
- koncepcja i projekt rozwiązania;
- realizacja;
- weryfikacja i wyniki;
- organizacja i przebieg projektu;
- podsumowanie i wnioski;
- oświadczenie o wykorzystaniu narzędzi AI;
- podział zadań i procentowy udział autorów;
- bibliografia i opcjonalne załączniki.

Układ jest propozycją. Rozdziały można łączyć, skracać lub usuwać zgodnie z wymaganiami prowadzącego i charakterem projektu.

Informacja o wykorzystaniu AI oraz tabela wkładu autorów są domyślnie
włączone. Ich treść znajduje się w `backmatter/`, a widoczność kontrolują
ustawienia `\showaideclaration` i `\showcontributions` w
`config/metadata.tex`.

Plik `backmatter/ai-declaration.tex` jest przygotowany zgodnie z załącznikiem
nr 2A do Zasad korzystania z narzędzi AI przez studentów i doktorantów
Politechniki Opolskiej. Polityka korzystania z narzędzi sztucznej inteligencji
(AI) została opracowana na podstawie Zarządzenia nr 65/2026 Rektora
Politechniki Opolskiej. Należy pozostawić dokładnie jeden z dwóch wariantów:

- gdy AI wpłynęła na materiał — podać nazwę narzędzia, cel i zakres użycia oraz
  elementy przygotowane lub zmienione z AI, a następnie potwierdzić sprawdzenie
  wyników i odpowiedzialność za materiał;
- gdy AI nie używano w zakresie wymagającym ujawnienia — zamieścić przygotowane
  oświadczenie z wariantu 2.

Zwykła autokorekta i sprawdzanie pisowni, które nie wpływają na treść
merytoryczną, co do zasady nie wymagają ujawnienia, chyba że prowadzący określi
inaczej. Prowadzący może również zażądać bardziej szczegółowych informacji,
np. przykładowych poleceń, wyników narzędzia lub materiałów roboczych. Użycie AI
musi mieścić się w zakresie dopuszczonym przez prowadzącego oraz respektować
ochronę danych, poufność, prawa autorskie i warunki korzystania z narzędzi.

## Rysunki, jednostki i kod

Rysunki wstawiaj przez `\projectgraphic`, jednostki zapisuj pakietem `siunitx`, np. `\qty{12}{\volt}`, a kod przechowuj poza plikiem rozdziału i wczytuj przez `\lstinputlisting`.

Zalecane style kodu to `project-python`, `project-matlab`, `project-c`,
`project-cpp` i `project-shell`. Dla zgodności z przykładami ze „SZABLONU
Prezentacji” działa także zapis `[style=weail,language=Python]`.

## Polskie znaki w listingach

Styl projektu rozszerza wewnętrzną tabelę `\lst@DefEC` pakietu `listings` o
polskie litery. Dzięki temu LuaLaTeX zachowuje ich kolejność, odstępy i
kolorowanie w komentarzach, napisach oraz identyfikatorach — zarówno w
środowisku `lstlisting`, jak i w plikach wczytywanych przez
`\lstinputlisting`. Nie należy dodawać mapowania `literate`.

Znacznik kończący tabelę znaków jest generowany programowo. W pliku stylu nie
ma surowego znaku sterującego, który jest odrzucany przez nowsze wersje TeX
Live używane m.in. w Prism.

Jeżeli komunikaty błędów zaczynają się od tekstu „Ten szablon wymaga
LuaLaTeX”, wybrano niewłaściwy silnik. Komunikaty `OT1` albo `Invalid UTF-8`
w pliku `main.vrb` również są skutkiem kompilacji przez pdfLaTeX, a nie
niepoprawnego zapisu polskich znaków w kodzie. W Prism, Overleaf lub podobnym
edytorze ustaw plik główny na `main.tex`, kompilator na LuaLaTeX i po zmianie
silnika wykonaj pełną kompilację od początku (`Recompile from scratch`).
Lokalnie korzystaj z polecenia `latexmk main.tex`.

## Kompilacja

### Wymagania lokalne w systemie Windows

Przed pierwszą kompilacją sprawdź dostępność wymaganych programów:

```text
perl --version
latexmk -v
lualatex --version
biber --version
```

MiKTeX dostarcza LuaLaTeX, Biber, pakiety LaTeX-a oraz program `latexmk`, ale
`latexmk` jest skryptem napisanym w Perlu. Dlatego instalacja samego MiKTeX-a
może nie wystarczyć w systemie Windows. Jeżeli polecenie `perl` nie jest
rozpoznawane albo `latexmk` zgłasza brak interpretera, zainstaluj Perl — np.
[Strawberry Perl](https://strawberryperl.com/) — a następnie zamknij i ponownie
otwórz terminal oraz TeXstudio, aby programy odczytały zaktualizowaną zmienną
`PATH`.

Sam LuaLaTeX nie wymaga Perla. Perl jest jednak potrzebny do zalecanego
budowania przez `latexmk`, które automatycznie wykonuje właściwą liczbę
przebiegów LuaLaTeX i Bibera. Przy pracy w Prism, Overleaf lub podobnym edytorze
internetowym lokalna instalacja Perla nie jest potrzebna.

### Budowanie dokumentu

```text
latexmk main.tex
latexmk -g main.tex   # pełne przeliczenie po usunięciu błędu
latexmk -C main.tex   # usunięcie artefaktów kompilacji
```

Gotowy dokument powstanie jako `build/main.pdf`.

### TeXstudio

Poniższa konfiguracja powoduje, że TeXstudio uruchamia program `latexmk` w
katalogu projektu. Program automatycznie odczytuje znajdujący się tam plik
`latexmkrc`, który wybiera LuaLaTeX, uruchamia Biber w razie potrzeby i zapisuje
PDF oraz pliki pomocnicze w katalogu `build/`.

Przed konfiguracją należy zainstalować MiKTeX i Perl, ponownie uruchomić
TeXstudio, a następnie otworzyć w nim plik `main.tex`. Aby skonfigurować
budowanie projektu:

1. Otwórz **Opcje → Konfiguruj TeXstudio** i po lewej stronie wybierz
   **Zbuduj**.
2. Zaznacz znajdującą się na dole okna opcję **Pokaż opcje zaawansowane**.
3. W polu **Kompilator domyślny** wybierz `txs:///latexmk`.
4. W sekcji **Polecenia użytkownika** kliknij **+ Dodaj**.
5. W polu nazwy polecenia wpisz `user0:Latexmk LuaLaTeX`.
6. W polu polecenia wpisz dokładnie:

   ```text
   latexmk.exe -synctex=1 -interaction=nonstopmode -file-line-error %.tex
   ```

7. W sekcji **Opcje budowania → Dodatkowe ścieżki wyszukiwania**, w polu
   **Plik PDF**, wpisz:

   ```text
   build;
   ```

8. Zatwierdź konfigurację przyciskiem **OK**.

![Konfiguracja TeXstudio do kompilacji projektu przez LatexMk](docs/images/Ustawienia_TeXstudio.png)

Wartość `%.tex` oznacza aktualnie kompilowany dokument. Nie należy dopisywać do
polecenia opcji `-pdf` ani `-lualatex`: właściwy silnik i katalog wyjściowy są
ustawione centralnie w projektowym pliku `latexmkrc`. Wpis `build;` wskazuje
TeXstudio dodatkowe miejsce, w którym ma szukać utworzonego PDF-u. Średnik jest
separatorem ścieżek używanym w tym polu w systemie Windows.

Po zapisaniu ustawień otwórz `main.tex` i uruchom kompilację. Gotowy dokument
powinien pojawić się jako `build/main.pdf`. Jeśli TeXstudio przy pierwszym
otwarciu dokumentu poprosi o zgodę na zastosowanie projektowej dyrektywy
kompilacji, wybierz zgodę tylko dla tego dokumentu. Dyrektywa usuwa z
wbudowanego polecenia wyłącznie opcję `-pdf`, aby nie wymuszać pdfLaTeX;
pozostałe ustawienia przejmuje `latexmkrc`.

## Gotowe paczki ZIP

Katalog `dist/` zawiera dwie przenośne wersje szablonu:

- `szablon-projektu-local.zip` — do pracy na komputerze; zawiera `latexmkrc`,
  a w systemie Windows wymaga MiKTeX-a i Perla;
- `szablon-projektu-online.zip` — do Prism, Overleaf lub podobnego edytora;
  nie zawiera lokalnej konfiguracji LatexMk, a na początku pliku `main.tex`
  ma dyrektywę `% !TeX program = lualatex` wskazującą wymagany kompilator.

Oba archiwa zawierają źródła, instrukcje, rozdziały, oświadczenia końcowe,
przykładową bibliografię i generator paczek. Nie zawierają plików z `build/`,
`tmp/`, wcześniejszych archiwów ani innych artefaktów kompilacji.

Paczki tworzy program `tools/create_release.py`:

```text
python tools/create_release.py --target local
python tools/create_release.py --target online
```

Bez opcji `--target` program interaktywnie zapyta o wariant. Własną nazwę pliku
można podać przez `--output ścieżka/do/pliku.zip`.

Po każdej zmianie plików wchodzących w skład szablonu należy ponownie
wygenerować oba archiwa i zapisać je w repozytorium. Katalog `dist/` nie jest
wykluczony przez `.gitignore`.
