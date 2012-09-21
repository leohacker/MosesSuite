docdir = $(pkgdatadir)/doc
TEX =  manual-j.tex  
PDF =  manual-j.pdf
EXTRA_DIST = $(TEX) $(PDF)
SUFFIXES= .tex .dvi .pdf

.tex.dvi:
	platex $<
	platex $<

.dvi.pdf:
	dvipdfmx $<
