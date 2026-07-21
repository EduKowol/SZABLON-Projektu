# Pisanie rozdziałów i organizacja materiałów

Każdy rozdział ma osobny plik `.tex`. Dodatkowe materiały warto umieszczać w katalogu o tej samej nazwie co rozdział:

```text
chapters/04-realizacja/
├── figures/   # rysunki i schematy
├── code/      # kod wczytywany przez \lstinputlisting
├── data/      # dane źródłowe
└── scripts/   # skrypty odtwarzające wykresy i wyniki
```

Odwołania twórz przez `\label`, `\cref` i `\Cref`, a źródła cytuj przez `\cite`.

## Podstawowe zasady edycji

- treść wpisuj w plikach `.tex`, a nie w `main.tex`;
- pusty wiersz w źródle rozpoczyna nowy akapit;
- nie kończ zwykłych akapitów poleceniem `\\`;
- nowe podrozdziały twórz przez `\section{Tytuł}` i `\subsection{Tytuł}`;
- znak `%` rozpoczyna komentarz niewidoczny w PDF;
- znaki `%`, `&`, `_` i `#` w zwykłym tekście zapisuj jako `\%`, `\&`, `\_` i `\#`.

## Odwołania i cytowania

Element najpierw oznacz etykietą, a później przywołuj ją w tekście:

```tex
\section{Architektura}
\label{sec:architektura}

Szczegóły przedstawiono w \cref{sec:architektura}.
Źródło informacji wskazano w \cite{lamport1994}.
```

Nie wpisuj ręcznie numerów rozdziałów, rysunków, tabel ani cytowań.

## Rysunki

```tex
\begin{figure}[htbp]
  \centering
  \projectgraphic{chapters/03-koncepcja-i-projekt/figures/architektura.png}
  \caption{Architektura projektowanego rozwiązania}
  \label{fig:architektura}
\end{figure}
```

Każdy rysunek powinien mieć podpis, etykietę i odwołanie w tekście, np.
`\cref{fig:architektura}`.

## Kod źródłowy

```tex
\lstinputlisting[
  style=project-python,
  caption={Przetwarzanie danych wejściowych},
  label={lst:przetwarzanie}
]{chapters/04-realizacja/code/program.py}
```

Dostępne style: `project-python`, `project-matlab`, `project-c`, `project-cpp`
i `project-shell`. W treści przywołuj listing przez `\cref{lst:przetwarzanie}`.
Kod może zawierać polskie znaki zapisane bezpośrednio w UTF-8; są one
obsługiwane zarówno w środowisku `lstlisting`, jak i przez `\lstinputlisting`.

## Liczby i jednostki

Do zapisu wartości z jednostkami używaj `siunitx`:

```tex
Napięcie wynosiło \qty{12}{\volt}, a częstotliwość \qty{50}{\hertz}.
```
