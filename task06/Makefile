
CC = gcc

all: lambda
COMOBJ = y.tab.o lex.yy.o emalloc.o tree.o type.o closure.o 

# ------------------------------------------------------------

.c.o:
	 $(CC)  -pg  -Wall $(INCLUDE) -c $(CFLAGS) $(MODEL) $*.c

#------------------------------------------------------------

lex.yy.c:  lexer.l
	flex  lexer.l

y.tab.c y.tab.h:  grammar.y
	byacc -tvd grammar.y
#------------------------------------------------------------

lambda:  $(COMOBJ) 
	$(CC) -pg -o lambda $(LIB) $(MODEL) $(COMOBJ) $(CLIB)

# ----------------------------------------------------------------------

clean: 
	rm *.o y.tab.c y.tab.h lex.yy.c
#

emalloc.o: emalloc.c
lex.yy.o: lex.yy.c tree.h y.tab.h
tree.o: tree.h tree.c
type.o: type.h tree.h type.c
closure.o: tree.h closure.c
y.tab.o: y.tab.c tree.h 


