CC:=latexmk
OPTIONS:=-pdf
TARGET:=main

all: coverletter
	$(CC) $(OPTIONS) $(TARGET)

coverletter:
	$(CC) $(OPTIONS) coverletter.tex

clean_partial:
	rm -f *.aux
	rm -f *.bbl
	rm -f *.blg
	rm -f *.dvi
	rm -f *.fdb_latexmk
	rm -f *.fls
	rm -f *.glo
	rm -f *.hd
	rm -f *.idx
	rm -f *.ins
	rm -f *.log
	rm -f *.out
	rm -f *.toc
	rm -f archive.zip

clean: clean_partial
	rm -f *.pdf

fresh: clean all

combined:
	python helper.py combine
	$(CC) $(OPTIONS) $(TARGET)-combined

zip:
	$(MAKE) clean
	$(MAKE) combined
	$(MAKE) clean_partial
	zip archive.zip $(TARGET)-combined.tex
	zip archive.zip plos2025.bst
	zip archive.zip $(TARGET)-combined.pdf
	zip archive.zip references.bib
	python helper.py zip_graphics
