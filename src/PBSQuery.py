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
import UserDict
import string
import sys
import re

class PBSError(Exception):
	def __init__(self, msg=''):
		self.msg = msg
		Exception.__init__(self, msg)
		
	def __repr__(self):
		return self.msg

	__str__ = __repr__


class PBSQuery:
	def __init__(self, server=None):
		if not server:
			self.server = pbs.pbs_default()
		else:
			self.server = server


	def _connect(self):
		"""Connect to the PBS/Torque server"""
		self.con = pbs.pbs_connect(self.server)
		if self.con < 0:
			str = "Could not make a connection with %s\n" %(self.server)
			raise PBSError(str)

	def _disconnect(self):
		"""Close the PBS/Torque connection"""
		pbs.pbs_disconnect(self.con)
		self.attribs = 'NULL'

	def _list_2_attrib(self, list):
		"""Convert a python list to an attrib list suitable for pbs"""
		self.attribs = pbs.new_attrl( len(list) )
		i = 0 
		for attrib in list:
			self.attribs[i].name = attrib
			i = i + 1

	def _pbsstr_2_list(self, str, delimiter):
		"""Convert a string to a python list and use delimiter as spit char"""
		l = sting.splitfields(str, delimiter)
		if len(l) > 1:
			return l

	def _list_2_dict(self, l, class_func):
		"""Convert a pbsstat function list to a class dictionary"""
		self.d = {}
		for item in l:
			new = class_func()
			self.d[item.name] = new 
			
			for a in item.attribs:
				new.name = item.name 
				if a.resource:
					new[a.name + '.' + a.resource] = a.value
				else:
					new[a.name] = a.value
		self._free(l)
	        
	def _free(self, memory):
		"""
		freeing up used memmory
		"""
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
		
		self._list_2_dict(queues, queue)

	def getqueue(self, name, attrib_list=None):
		self._statqueue(name, attrib_list)
		return self.d[name]
        
	def getqueues(self, attrib_list=None):
		self._statqueue('', attrib_list)
		return self.d

	def _statnode(self, select='', attrib_list=None, property=None):
		"""Get the node config from the pbs server"""
		if attrib_list:
			self._list_2_attrib(attrib_list)
		else:
			self.attribs = 'NULL' 
			
		if property:
			select = ':%s' %(property)

		self._connect()
		nodes = pbs.pbs_statnode(self.con, select, self.attribs, 'NULL')
		self._disconnect() 
		
		self._list_2_dict(nodes, node)

	def getnode(self, name, attrib_list=None):
		self._statnode(name, attrib_list)
		return self.d[name]
        
	def getnodes(self, attrib_list=None):
		self._statnode('', attrib_list)
		return self.d

	def getnodes_with_property(self, property, attrib_list=None):
		self._statnode('', attrib_list, property)
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
		
		self._list_2_dict(jobs, job)

	def getjob(self, name, attrib_list=None):
		# To make sure we use the full name of a job; Changes a name
		# like 1234567 into 1234567.server.name 
		name = name.split('.')[0] + "." + self.get_server_name()

		self._statjob(name, attrib_list)
		return self.d[name]
        
	def getjobs(self, attrib_list=None):
		self._statjob('', attrib_list)
		return self.d

	def get_server_name(self):
		return self.server

class _PBSobject(UserDict.UserDict):
	TRUE  = 1
	FALSE = 0

	def __init__(self):
		UserDict.UserDict.__init__(self)
		self.name = None

	def get_value(self, key):
		if self.has_key(key):
			return self[key]
		else:
			return None

	def uniq(self, list):
		"""Filter out unique items of a list"""
		uniq_items = {}
		for item in list:
			uniq_items[item] = 1
		return uniq_items.keys()

class job(_PBSobject):
	"""PBS job class""" 
	def is_running(self):
		if self.get_value('job_state') == 'Q':
			return self.FALSE
		else:
			return self.TRUE 

	def get_nodes(self, unique=None):
		"""Returns a list of the nodes which run this job"""
		nodes = self.get_value('exec_host')
		if nodes:
			nodelist = string.split(nodes,'+')
			if not unique:
				return nodelist
			else:
				return self.uniq(nodelist)
		return list()


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
	
	def get_jobs(self, unique=None):
		"""Returns a list of the currently running job-id('s) on the node"""
		jobstring = self.get_value('jobs')
		if jobstring:
			joblist = re.compile('[^\\ /]\\d+[^/.]').findall( jobstring )
			if not unique:
				return joblist
			else:
				return self.uniq(joblist)
		return list()





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

	def get_version(self):
		return self.get_value('pbs_version')

def main():
	p = PBSQuery() 
	serverinfo = p.get_serverinfo()
	for server in serverinfo.keys():
		print server, ' version: ', serverinfo[server].get_version()
	for resource in serverinfo[server].keys():
		print '\t ', resource, ' = ', serverinfo[server][resource]

	queues = p.getqueues()
	for queue in queues.keys():
		print queue
		if queues[queue].is_execution():
			print '\t ', queues[queue]
		if queues[queue].has_key('acl_groups'):
			print '\t acl_groups: yes'
		else:
			print '\t acl_groups: no'

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
