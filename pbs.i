// PBS python interface
// Author: Bas van der Vlies <basv@sara.nl>
// Date  : 04 Sep 2001
// Vers. : 1.0
// Desc. : This is a simple python wrapper for PBS.
//
// CVS info
// $Id: pbs.i,v 1.1 2002/02/27 13:55:44 sscpbas Exp $
// $Date: 2002/02/27 13:55:44 $
// $Revision: 1.1 $
//
%module pbs
%include pointer.i

// header declarations
//
%{

#include "pbs_ifl.h"
#include "pbs_error.h"
#include "rm.h"

%}


// *****************************************************************
// Some IN typemaps from Python ---> C
//
/*
 * Convert Python attrl list to a valid C-linked list
*/
%typemap(python,in) struct attrl *IN {
  PyObject	*py_obj;
  struct attrl	*ptr, *prev;
  char 		s[255];
  int		i=0, size=0;

  // printf("Python --> C\n");

  size = Get_List_Size($input);
  if ( size == -1 ) {
      PyErr_SetString(PyExc_TypeError, "not a list");
      return NULL; 
  }

  $1 = prev = NULL;
  for ( i=0; i < size; i++ ) {
    py_obj = PyList_GetItem($input, i);
    if (SWIG_ConvertPtr(py_obj, (void **) &ptr, SWIGTYPE_p_attrl, 1)) {

      sprintf(s,"list item %d has wrong type", i);
      PyErr_SetString(PyExc_TypeError, s);
      return NULL;

      // This will skipp the wrong entry
      // continue;
    }

    /* 
     * Make first entry head of C linked list
    */ 
    if ( i == 0) { 
      $1 = ptr;
      ptr->next = prev;
    }
    else {
      prev->next = ptr;
      ptr->next = NULL;
    }
    prev = ptr;

  } // end for
} // end struct attrl *IN typemap

/*
 * Convert Python attropl list to a valid C-linked list
*/
%typemap(python,in) struct attropl *IN {
  PyObject		*py_obj;
  struct attropl	*ptr, *prev;
  char 			s[255];
  int			i=0, size=0;

  // printf("Python --> C\n");

  size = Get_List_Size($input);
  if ( size == -1 ) {
    PyErr_SetString(PyExc_TypeError, "not a list");
    return NULL; 
  }
  //printf("Size = %d\n", size);

  $1 = prev = NULL;
  for ( i=0; i < size; i++ ) {
    py_obj = PyList_GetItem($input, i);
    if (SWIG_ConvertPtr(py_obj, (void **) &ptr, SWIGTYPE_p_attropl, 1)) {

       sprintf(s,"list item %d has wrong type", i);
       PyErr_SetString(PyExc_TypeError, s);
       return NULL;

       // This will skipp the wrong entry
       // continue;
    }

    /* 
     * Make first entry head of C linked list
    */ 
    if ( i == 0) { 
      $1 = ptr;
      ptr->next = prev;
    }
    else {
      prev->next = ptr;
      ptr->next = NULL;
    }
    prev = ptr;

  } // end for
} // end struct attrl *IN typemap

%typemap(python,in) char **IN {
  int		i=0, size=0;
  PyObject	*py_obj;

  size = Get_List_Size($input);

  if ( size == -1 ) {
    PyErr_SetString(PyExc_TypeError, "not a list");
    return NULL; 
  }
  // printf("Size = %d\n", size);

  $1 = (char **) malloc( (size+1) * sizeof(char *));
  for (i=0; i < size; i++) {
    py_obj = PyList_GetItem($input, i);
    if (PyString_Check(py_obj)) {
      $1[i] = PyString_AsString(py_obj);
    }
    else {
      PyErr_SetString(PyExc_TypeError, "not a list of strings");
      free($1);
      return NULL; 
    }
  } // end for
  $1[i] = 0;
} // end typemap char **IN

// *****************************************************************
// Some OUT typemaps from C ---> Python
//
%typemap(python,out) struct batch_status * {

  PyObject *obj_batch;
  struct batch_status *ptr;
  int i=0, len=0;

  // printf("Ja we are in bussniss\n");

  // Deterime length of list
  //
  ptr = $1;
  while (ptr != NULL) {
    len++;
    ptr = ptr->next;
  }
  $result = PyList_New(len);

  // Make a list of batch_status pointers
  //
  ptr = $1;
  for (i=0; i < len; i++) {
    obj_batch = SWIG_NewPointerObj((void *)ptr, SWIGTYPE_p_batch_status,0); 
    PyList_SetItem($result, i, obj_batch);  	
    ptr = ptr->next;
  }
} // end typemap struct batch_status *

%typemap(python,out) struct attrl * {
  PyObject	*obj_batch;
  struct attrl	*ptr;
  int		i=0, len=0;

  ptr = $1;
  while (ptr != NULL) {
    len++;
    ptr = ptr->next;
  }
  $result = PyList_New(len);

  ptr = $1;
  for (i=0; i < len; i++) {
    obj_batch = SWIG_NewPointerObj((void *)ptr, SWIGTYPE_p_attrl,1); 
    PyList_SetItem($result, i, obj_batch);  	
    ptr = ptr->next;
  }
} // end typemap struct attrl *

%typemap(python,out) struct attropl * {
  PyObject		*obj_batch;
  struct attropl	*ptr;
  int			i=0, len=0;

  ptr = $1;
  while (ptr != NULL) {
    len++;
    ptr = ptr->next;
  }
  $result = PyList_New(len);

  ptr = $1;
  for (i=0; i < len; i++) {
    obj_batch = SWIG_NewPointerObj((void *)ptr, SWIGTYPE_p_attropl,1); 
    PyList_SetItem($result, i, obj_batch);  	
    ptr = ptr->next;
  }
} // end typemap struct attropl *

// Convert C (char **) to Python List
//
%typemap(python,out) char **pbs_selectjob {
   int len=0, i;

   if ($1 == NULL) 
     $result = PyList_New(0);
   else {
     while ($1[len]) 
       len++;

     $result = PyList_New(len);
     for (i=0; i < len; i++ )
       PyList_SetItem($result, i , PyString_FromString($1[i])); 
   }
} // end typemap char **pbs_selectjob

// *****************************************************************
// Some freearg typemaps 
//
%typemap(python, freearg) char ** {
  free( (char *) $1);
}

// *****************************************************************
// Some Functions used by all C-structs typemaps
//

%{
int Get_List_Size(PyObject *src)
{
  if (PyList_Check(src))
    return(PyList_Size(src));
  else {

    /* check if valid NULL pointer */
    if ( PyString_Check(src) ) {
      if ( ! strcmp(PyString_AsString(src), "NULL") )
        return(0);
    }
    else
      return(-1);

  } // end else
} // end Get_List_Size()

%}


// *****************************************************************
// These C-functions are the constructurs for the different C-structs 
//
/*
 * Make some default constructors for the various structs
*/
%inline %{

// The default constructor for struct attrl
//
struct attrl *new_attrl(int number)
{
  struct attrl *ptr;
  struct attrl *prev, *current;
  int i;

  /* 
    allocate memory as a one block is handy for Python scripts 
    and fill in the next fields so it also works for the C-library
  */
  ptr = (struct attrl *) malloc(number * sizeof(struct attrl));

  prev = NULL;
  current = ptr + (number - 1);
  for (i=0; i < number; i++)
  { 
    // printf("constructor called\n");
    current->name     = (char *) malloc(MAXNAMLEN * sizeof(char));
    current->resource = (char *) malloc(MAXNAMLEN * sizeof(char));
    current->value    = (char *) malloc(MAXNAMLEN * sizeof(char));

    bzero( (void*) current->name, sizeof(current->name));
    bzero( (void*) current->resource, sizeof(current->resource));
    bzero( (void*) current->value, sizeof(current->value));

    current->next     = prev;
    prev = current;
    current--;
  }
  return (struct attrl *)ptr;

} // end new_attrl()


// The default constructor for struct attropl
//
struct attropl *new_attropl(int number)
{
  struct attropl *ptr;
  struct attropl *prev, *current;
  int i;

  /* 
    allocate memory as a one block is handy for Python scripts 
    and fill in the next fields so it also works for the C-library
  */
  ptr = (struct attropl *) malloc(number * sizeof(struct attropl));

  prev = NULL;
  current = ptr + (number - 1);
  for (i=0; i < number; i++)
  { 
    // printf("constructor called\n");
    current->name     = (char *) malloc(MAXNAMLEN * sizeof(char));
    current->resource = (char *) malloc(MAXNAMLEN * sizeof(char));
    current->value    = (char *) malloc(MAXNAMLEN * sizeof(char));

    bzero( (void*) current->name, sizeof(current->name));
    bzero( (void*) current->resource, sizeof(current->resource));
    bzero( (void*) current->value, sizeof(current->value));
    current->op = 0;

    current->next     = prev;
    prev = current;
    current--;
  }
  return (struct attropl *)ptr;

} // end new_attropl()

/* Not used only returned */
struct batch_status *new_batch_status()
{
   struct batch_status *ptr;

   ptr = (struct batch_status *) malloc(sizeof(struct batch_status));
   return (struct batch_status *)ptr;
} // end new struct batch_status

%}  // end %inline functions


// *****************************************************************
// Here the Python shadow class is generated. We have added some
// stuff here to extend the python classes.
//
%nodefault
%include "pbs_python.h"
%include "rm.h"

/*
%feature("shadow") attrl::__str__ {
  def __str__(self): print self.name + self.value;
}
%addmethods attrl {
  void __str__();
}
*/

%addmethods attrl {
  char *__str__() {
    static char temp[4 * MAXNAMLEN] ;
    snprintf(temp, sizeof(temp), "(%s,%s,%s)", 
      self->name, self->resource, self->value);
    
    return &temp[0];
  }
}

%addmethods attropl {
  char *__str__() {
    static char temp[4 * MAXNAMLEN] ;
    snprintf(temp, sizeof(temp), "(%s,%s,%s)", 
      self->name, self->resource, self->value);
    
    return &temp[0];
  }
}


%shadow "resmom.py"
