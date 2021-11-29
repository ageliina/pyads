BIN=pyads.py
TO=$(HOME)/.local/bin

install:
	cp -v $(BIN) $(TO)/$(basename $(BIN))
