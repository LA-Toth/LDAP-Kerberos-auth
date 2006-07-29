.PHONY:  all build edit log viewpdf viewps silent make pdf emacs-x dvi emacs e ex html
NAME=$(notdir $(shell pwd))
all:	build
build:	$(NAME).tex
	pslatex ${NAME}.tex
#	dvips ${NAME}.dvi
	pdflatex ${NAME}.tex
edit:
	mcedit  ${NAME}.tex
emacs-x:
	emacs ${NAME}.tex &
emacs:
	@emacs -nw ${NAME}.tex
e: emacs
ex: emacs-x
log:
	@mcview ${NAME}.log
viewpdf:
	@acroread $(NAME).pdf
viewps:
	@gv $(NAME).ps
silent:	$(NAME).tex
	@pdflatex ${NAME}.tex >/dev/null 2>&1
dvi:
	@pslatex ${NAME}.tex >/dev/null 2>&1
make:
	mcedit Makefile
pdf: silent viewpdf
html:
	@html/reparse
