uuid := $(shell uuidgen)

BOOK=Sample


.PHONY: all
all: clean create open

.PHONY: clean
clean:
	rm -f *.epub
	find . -name ".DS_Store" | xargs rm

.PHONY: create
create:
	zip -0X "${BOOK}-${uuid}.epub" mimetype
	zip -Xr9D "${BOOK}-${uuid}.epub" -r . -x mimetype -x "Makefile" -x "scratch.py" -x "${BOOK}-${uuid}.epub"

.PHONY: open
open:
	open "${BOOK}-${uuid}.epub"
