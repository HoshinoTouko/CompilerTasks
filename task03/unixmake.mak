CC=gcc
.c.o:
	echo rebuilding $*.o from $*.c
	$(CC) -g3 -c $<

all: re2dfa

re2dfa: set.o ast.o dfa.o  parser.o main.o 
	$(CC) -g3 -o ./reg2dfa $^

ast.o: ast.c ast.h set.h
dfa.o: dfa.c ast.h set.h
parser.o: parser.c ast.h set.h
set.o: set.c set.h
main.o: main.c ast.h set.h

clean: 
	rm -f *.o 


