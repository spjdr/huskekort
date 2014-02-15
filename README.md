huskekort
=========

Genererer huskekort udfra data på `spjdrpedia.dk/wiki/Huskekort`.


## HOW TO

### Opsætning

* Hent web-fonten Bitter og læg den i `fonts` mappen.
* Installer `python` sammen med bibliotekterne `requests` og `pyPDF2`.
* Installer `pdflatex` og `xelatex`
* Installer `convert` og `inkscape`

### Kør

1. Hent alle kortene fra spjdrpedia med `parse.py` med kommandoen:
        
        python parse.py

2. Byg alle huskekortene med 
        
        python parselatex.py

3. Byg hjemmeside med 
        
        python parsehomepage.py

Voila.


