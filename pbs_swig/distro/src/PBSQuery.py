#
# Authors: Roy Dragseth (roy.dragseth@cc.uit.no) 
#          Bas van der Vlies (basv@sara.nl)
#
# SVN INFO:
#	$Id$
#
"""
Usage: from PBSQuery import PBSQuery

This class gets the info from the pbs_server via the pbs.py module
for the several batch objects. All get..() functions return an dictionary
with id as key and batch object as value

There are four batch objects:
 - server 
 - queue
 - job
 - node

Each object can be handled as an dictionary and has several member
functions. The second parameter is an python list and can be used if you 
are only interested in certain resources, see example

There are the following functions for PBSQuery:
  job - 
	getjob(job_id, attributes=<default is all>)
	getjobs(attributes=<default is all>)
 
  node -
	getnode(node_id, attributes=<default is all>)
	getnodes(attributes=<default is all>)

  queue -
	getqueue(queue_id, attributes=<default is all>)
	getqueues(attributes=<default is all>)

  server -
	get_serverinfo(attributes=<default is all>)

Here is an example how to use the module:
	from PBSQuery import PBSQuery
	p = PBSQuery()
	nodes = p.getnodes()
	for name,node in nodes.items():
	    print name
	    if node.is_free():
	       print node, node['state']

	l = [ 'state', 'np' ]
	nodes = p.getnodes(l)
	for name,node in nodes.items():
	       print node, node['state']

The parameter 'attributes' is an python list of resources that 
you are interested in, eg: only show state of nodes
        l = list()
	l.append('state')
	nodes = p.getnodes(l)
"""
import pbs


class PBSQuery:
    def __init__(self, server=None):
        if not server:
            self.server = pbs.pbs_default()
	else:
	    self.server = server


    def _connect(self):
       """Connect to the PBS/Torque server"""
       self.con = pbs.pbs_connect(self.server)

    def _disconnect(self):
       """Close the PBS/Torque connection"""
       pbs.pbs_disconnect(self.con)
       self.attribs = 'NULL'

    def _list_2_attrib(self, list):
        """Convert an python list to an attrib list suitable for pbs"""
        self.attribs = pbs.new_attrl( len(list) )
        i = 0 
        for attrib in list:
	    self.attribs[i].name = attrib
	    i = i + 1

    def _list_2_dict(self, l, class_func):
        """Convert an pbsstat function list to an class dictionary"""
        self.d = dict()
        for item in l:
	    new = class_func()
	    for a in item.attribs:
	        new.name = item.name 
	        if a.resource:
                   new.attribs[a.name + '.' + a.resource] = a.value
		else:
	           new.attribs[a.name] = a.value
                self.d[item.name] = new
        self._free(l)
	        
    def _free(self, memory):
        pbs.pbs_statfree(memory)

    def _statserver(self, attrib_list=None):
        """Get the server config from the pbs server"""
        if attrib_list:
	   self._list_2_attrib(attrib_list)
        else:
	   self.attribs = 'NULL'

        self._connect()
        serverinfo = pbs.pbs_statserver(self.con, self.attribs, 'NULL')
        self._disconnect()

	self.serverinfo = dict()
	self._list_2_dict(serverinfo, server)

    def get_serverinfo(self, attrib_list=None):
        self._statserver(attrib_list)
	return self.d

    def _statqueue(self, queue_name='', attrib_list=None):
        """Get the queue config from the pbs server"""
        if attrib_list:
	   self._list_2_attrib(attrib_list)
        else:
	   self.attribs = 'NULL'

        self._connect()
        queues = pbs.pbs_statque(self.con, queue_name, self.attribs, 'NULL')
        self._disconnect()

	self.queues = dict()
	self._list_2_dict(queues, queue)

    def getqueue(self, name, attrib_list=None):
        self._statqueue(name, attrib_list)
	return self.d
        
    def getqueues(self, attrib_list=None):
        self._statqueue('', attrib_list)
	return self.d

    def _statnode(self, node_name='', attrib_list=None):
        """Get the node config from the pbs server"""
        if attrib_list:
	   self._list_2_attrib(attrib_list)
        else:
	   self.attribs = 'NULL'

        self._connect()
        nodes = pbs.pbs_statnode(self.con, node_name, self.attribs, 'NULL')
        self._disconnect()

        self.nodes = dict()
	self._list_2_dict(nodes, node)

    def getnode(self, name, attrib_list=None):
        self._statnode(name, attrib_list)
	return self.d
        
    def getnodes(self, attrib_list=None):
        self._statnode('', attrib_list)
	return self.d

    def _statjob(self, job_name='', attrib_list=None):
        """Get the job config from the pbs server"""
        if attrib_list:
	   self._list_2_attrib(attrib_list)
        else:
	   self.attribs = 'NULL'
	   
        self._connect()
        jobs = pbs.pbs_statjob(self.con, job_name, self.attribs, 'NULL')
        self._disconnect()

        self.jobs = dict()
	self._list_2_dict(jobs, job)

    def getjob(self, name, attrib_list=None):
        self._statjob(name, attrib_list)
	return self.d
        
    def getjobs(self, attrib_list=None):
        self._statjob('', attrib_list)
	return self.d

class _PBSobject:
    TRUE  = 1
    FALSE = 0

    def __init__(self):
        self.attribs = dict()
	self.name = None

    def __len__(self):
    	return(len(self.attribs.keys()))

    def __str__(self):
        data = self.name + '\n'
	for name,value in self.attribs.items():
                data = data + '\t%s = %s\n' %(name, value)
	return(data)

    __repr__ = __str__

    def __getitem__(self,key):
        if key == 'name':
            return self.name
        
    	return(self.attribs[key])

    def get_value(self, key):
        if self.attribs.has_key(key):
	   return self.attribs[key]
        else:
	   return None

    def has_key(self, key):
        if self.attribs.has_key(key):
	   return self.TRUE
        else:
	   return None

    def keys(self):
        return self.attribs.keys()

    def values(self):
        return self.attribs.values()

    def items(self):
        return self.attribs.items()
    
class job(_PBSobject):
    """PBS job class"""

    def is_running(self):
    	if self.get_value('job_state') == 'Q':
	   return self.FALSE
	else:
	   return self.TRUE 

class node(_PBSobject):
    """PBS node class"""

    def is_free(self):
        """Check if node is free"""
        if self.get_value('state') == 'free':
	      return self.TRUE
	else:
	      return self.FALSE 

    def has_job(self):
        """Does the node run a job"""
        if self.get_value('jobs'):
	      return self.TRUE
	else:
	      return self.FALSE

class queue(_PBSobject):
    """PBS queue class"""

    def is_enabled(self):
    	if self.get_value('enabled') == 'True':
	   return self.TRUE 
	else:
	   return self.FALSE

    def is_execution(self):
    	if self.get_value('queue_type') == 'Execution':
	   return self.TRUE 
	else:
	   return self.FALSE


class server(_PBSobject):
    """PBS server class"""

def main():
    p = PBSQuery()

    serverinfo = p.get_serverinfo()
    for name, server in serverinfo.items():
	print server
	for key in server.keys():
		print key, ' = ', server[key]

    queues = p.getqueues()
    for queue in queues.values():
	if queue.is_execution():
	   print queue

    jobs = p.getjobs()
    for name,job in jobs.items():
	if job.is_running():
	   print job

    l = ['state']
    nodes = p.getnodes(l)
    for name,node in nodes.items():
        if node.is_free(): 
           print node

if __name__ == "__main__":
    main()
