.PHONY:  all build edit log viewpdf viewps silent make pdf emacs-x dvi emacs e ex html simple
NAME=main
FILE ?= ${NAME}.tex

all:	build dvi
build:	$(NAME).tex setdate
	pslatex ${NAME}.tex
	pdflatex ${NAME}.tex
	pdflatex ${NAME}.tex
	pdflatex ${NAME}.tex
	bibtex ${NAME}
	pdflatex ${NAME}.tex
	pdflatex ${NAME}.tex
	pdflatex ${NAME}.tex
	pslatex ${NAME}.tex
edit:
	mcedit  ${FILE}
emacs-x:
	emacs ${FILE} &
emacs:
	@emacs -nw ${FILE}
e: emacs
ex: emacs-x
log:
	@mcview ${NAME}.log
viewpdf:
	@acroread $(NAME).pdf
viewps:
	@gv $(NAME).ps
silent:	$(NAME).tex setdate
	@pdflatex ${NAME}.tex >/dev/null 2>&1
	@pdflatex ${NAME}.tex >/dev/null 2>&1
	@pdflatex ${NAME}.tex >/dev/null 2>&1
	@bibtex ${NAME} 2>/dev/null >&2
	@pdflatex ${NAME}.tex >/dev/null 2>&1
	@pdflatex ${NAME}.tex >/dev/null 2>&1
	@pdflatex ${NAME}.tex >/dev/null 2>&1
dvi:
	@pslatex ${NAME}.tex >/dev/null 2>&1
make:
	mcedit Makefile
pdf: silent viewpdf

setdate:
	@bash mkdate.sh
simple:
	@pdflatex ${NAME}.tex >/dev/null 2>&1


html:
	@html/reparse
	@html/postparse.php | sed 's/main.html#/#/g'>  html/main/ldap-kerberos.html
