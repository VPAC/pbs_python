# 
# $Id: Makefile,v 1.4 2003/03/03 09:37:36 sscpbas Exp $
#
LIBS    =  -L/usr/local/lib -llog -lnet -lpbs
INCLUDE =  -I/usr/include/python1.5

pbs::
	gcc -c pbs_wrap.c ${INCLUDE}
	ld -G pbs_wrap.o ${LIBS} -o pbscmodule.so

clean::
	rm *.o pbs.pyc *.so
