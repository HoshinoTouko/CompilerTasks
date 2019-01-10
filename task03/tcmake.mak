# You must set TCHOME to your proper TC Home Directory!
TCHOME=c:\TC

CFLAGS	= -v -O 
INCLUDE = -I$(TCHOME)\include;.
LIB = -L$(TCHOME)\lib;.
CC	= $(TCHOME)\tcc
MODEL  = -ms

.c.obj:
	 $(CC) $(INCLUDE) -c $(CFLAGS) $(MODEL) $*.c

OBJ = set.obj parser.obj ast.obj dfa.obj main.obj

all: reg2dfa.exe

reg2dfa.exe: $(OBJ) 
	$(CC) -ereg2dfa.exe $(LIB) $(MODEL) $(CLIB) $(OBJ)

ast.obj: ast.c ast.h set.h
dfa.obj: dfa.c ast.h set.h
parser.obj: parser.c ast.h set.h
set.obj: set.c set.h
main.obj: main.c ast.h set.h

clean:
	del  *.obj 
	del reg2dfa.exe
