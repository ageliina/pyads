TO=$(HOME)/.local/bin
BIN=pyads.py
BIN1=$(PWD)/pyads.py
BIN2=$(TO)/$(basename $(BIN))

install:
	ln -sf $(BIN1) $(BIN2)
