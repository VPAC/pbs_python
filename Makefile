# 
# $Id: Makefile,v 1.4 2002/02/27 13:55:43 sscpbas Exp $
#
LIBS    =  -L/usr/local/lib -lnet -lpbs
#INCLUDE =  -I/usr/include/python1.5
INCLUDE =  -I/usr/local/include/python2.1

pbs::
	/usr/bin/swig -python -shadow pbs.i
	gcc -c pbs_wrap.c ${INCLUDE}
	ld -G pbs_wrap.o ${LIBS} -o pbscmodule.so

clean::
	rm *.o pbs.pyc *.so
