compile: ## compile sources
	gcc -Wall -o hash.exe src/*.c

run:  ## run program
	./hash.exe testfile
