#Generate lookup tables from source data
sourcedir := sources
targetdir := lookuptables
scriptdir := scripts
tmpdir    := tmp

peopleurl := http://www.govtrack.us/data/us/113/people.xml
targetxml := $(targetdir)/acts.xml $(targetdir)/committees.xml $(targetdir)/federal-bodies.xml $(targetdir)/people.xml $(targetdir)/billversions.xml
xmlschema := entity-table.xsd
movedest  := ../templates/vocabularies

.PHONY: all preview validate clean move


all: $(targetxml)

$(targetdir)/%.xml: $(tmpdir)/%.xml.tmp-unformatted
	xmllint --format --output $@ $<

$(tmpdir)/billversions.xml.tmp-unformatted: $(scriptdir)/doctypes2xml.py $(sourcedir)/doctypes.txt
	python $+ $@

$(tmpdir)/acts.xml.tmp-unformatted: $(scriptdir)/act-names.py $(sourcedir)/popular-names.csv
	python  $+ $@

$(targetdir)/committees.xml: $(scriptdir)/fix-committees.xsl $(sourcedir)/committees-subcommittees.xml
	xsltproc --output $@ $+

$(tmpdir)/federal-bodies.xml.tmp-unformatted: $(scriptdir)/nistcsv2xml.py $(sourcedir)/NIST-agencies-bureaus.csv
	python $+ $@

$(tmpdir)/people-govtrack.xml:
	curl --compressed --time-cond $@ -o $@ $(peopleurl)

$(targetdir)/people.xml: $(scriptdir)/govtrack2cato.xsl $(tmpdir)/people-govtrack.xml
	xsltproc --output $@ --stringparam source $(peopleurl) $+

preview: $(targetxml)
	less -S -M $^

validate: $(targetxml) $(xmlschema) 
	xmllint --noout --schema $(xmlschema) $(targetxml)

clean:
	rm $(tmpdir)/* $(targetxml)

move:
	cp $(targetxml) $(movedest)