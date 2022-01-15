compile: ## compile sources
	gcc -Wall -o hash.exe main.c src/hasher.c src/sha.c

run:  ## run program
	./hash.exe testfile


clean: ## clean
	rm -r src/Release
	rm src/_hasher.py
