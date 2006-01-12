# 
# $Id$
#
LIBS    =  -L/usr/lib/torque -llog -lnet -lpbs
INCLUDE =  -I/usr/include/python2.1

pbs::
	gcc -c pbs_wrap.c ${INCLUDE}
	gcc -shared pbs_wrap.o ${LIBS} -o _pbs.so

clean::
	rm -f *.o pbs.pyc *.so
