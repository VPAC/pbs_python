# 
# $Id$
#
LIBS    =  -L/opt/pbs/usr/lib -llog -lnet -lpbs
INCLUDE =  -I/usr/include/python2.1

pbs::
	gcc -c pbs_wrap.c ${INCLUDE}
	ld -G pbs_wrap.o ${LIBS} -o pbscmodule.so

clean::
	rm *.o pbs.pyc *.so
