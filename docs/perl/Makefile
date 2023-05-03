VERSION=3.1
SRC=~/src/Fsdb-$(VERSION)

all: buildperl scripts perlindex

.PHONY: buildperl scripts # always rebuild

buildperl:
	cd $(SRC) ; \
	perl Makefile.PL ; \
	make

scripts:
	outdir=`pwd` ; \
	cd $(SRC)/blib/script ; \
	for i in * ; do \
		pod2man $$i | \
		pandoc -f man -i - -t rst -o - | \
		perl -n -e 'if (/^NAME$$/) { $$_ = <>; $$_ = <>; $$_ = <>; print("$$_" . "=" x 70 . "\n\n"); $$printit = 1; $$_ = <>; $$_ = <>; } if (/^SYNOPSIS$$/) { print("*NOTE: this page was directly converted from the perl FSDB manual pages from FSDB version $(VERSION)*\n\n")} ; if ("$$printit" eq "1") { s/^(==+)/"-" x length($$1)/e; print; }' > $$outdir/$$(basename $$i).rst ; \
	done

perlindex:
	outfile=../perltools.rst ; \
	echo -e "Perl FSDB Tools\n===============\n\n.. toctree::\n   :maxdepth: 1\n   :caption: FSDB Perl Scripts:\n" > $$outfile ; \
	for i in *.rst ; do \
		echo "   perl/$$i" >> $$outfile ; \
	done
