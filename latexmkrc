# UWAGA DLA WINDOWS: latexmk jest skryptem napisanym w Perlu. Do lokalnej
# kompilacji potrzebne są MiKTeX oraz interpreter Perl, np. Strawberry Perl.
# Po instalacji sprawdź polecenia: perl --version oraz latexmk -v.

# Wszystkie artefakty kompilacji trafiają do jednego katalogu.
# Dzięki temu katalog główny projektu zawiera wyłącznie źródła.
$out_dir = 'build';
$aux_dir = 'build';

# Domyślnym silnikiem projektu jest LuaLaTeX.
$pdf_mode = 4;
$lualatex = 'lualatex %O %S';

# Pliki usuwane przez: latexmk -C
$clean_ext .= ' run.xml bbl bcf blg synctex.gz';
