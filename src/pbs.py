# This file was created automatically by SWIG.
import pbsc
class attrl:
    __setmethods__ = {}
    for _s in []: __setmethods__.update(_s.__setmethods__)
    def __setattr__(self,name,value):
        if (name == "this"):
            if isinstance(value,attrl):
                self.__dict__[name] = value.this
                if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
                del value.thisown
                return
        method = attrl.__setmethods__.get(name,None)
        if method: return method(self,value)
        self.__dict__[name] = value

    __getmethods__ = {}
    for _s in []: __getmethods__.update(_s.__getmethods__)
    def __getattr__(self,name):
        method = attrl.__getmethods__.get(name,None)
        if method: return method(self)
        raise AttributeError,name

    __setmethods__["name"] = pbsc.attrl_name_set
    __getmethods__["name"] = pbsc.attrl_name_get
    __setmethods__["resource"] = pbsc.attrl_resource_set
    __getmethods__["resource"] = pbsc.attrl_resource_get
    __setmethods__["value"] = pbsc.attrl_value_set
    __getmethods__["value"] = pbsc.attrl_value_get
    __setmethods__["op"] = pbsc.attrl_op_set
    __getmethods__["op"] = pbsc.attrl_op_get
    def __str__(*args): return apply(pbsc.attrl___str__,args)
    def __init__(self): raise RuntimeError, "No constructor defined"
    def __repr__(self):
        return "<C attrl instance at %s>" % (self.this,)

class attrlPtr(attrl):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = attrl
pbsc.attrl_swigregister(attrlPtr)
class attropl:
    __setmethods__ = {}
    for _s in []: __setmethods__.update(_s.__setmethods__)
    def __setattr__(self,name,value):
        if (name == "this"):
            if isinstance(value,attropl):
                self.__dict__[name] = value.this
                if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
                del value.thisown
                return
        method = attropl.__setmethods__.get(name,None)
        if method: return method(self,value)
        self.__dict__[name] = value

    __getmethods__ = {}
    for _s in []: __getmethods__.update(_s.__getmethods__)
    def __getattr__(self,name):
        method = attropl.__getmethods__.get(name,None)
        if method: return method(self)
        raise AttributeError,name

    __setmethods__["name"] = pbsc.attropl_name_set
    __getmethods__["name"] = pbsc.attropl_name_get
    __setmethods__["resource"] = pbsc.attropl_resource_set
    __getmethods__["resource"] = pbsc.attropl_resource_get
    __setmethods__["value"] = pbsc.attropl_value_set
    __getmethods__["value"] = pbsc.attropl_value_get
    __setmethods__["op"] = pbsc.attropl_op_set
    __getmethods__["op"] = pbsc.attropl_op_get
    def __str__(*args): return apply(pbsc.attropl___str__,args)
    def __init__(self): raise RuntimeError, "No constructor defined"
    def __repr__(self):
        return "<C attropl instance at %s>" % (self.this,)

class attroplPtr(attropl):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = attropl
pbsc.attropl_swigregister(attroplPtr)
class batch_status:
    __setmethods__ = {}
    for _s in []: __setmethods__.update(_s.__setmethods__)
    def __setattr__(self,name,value):
        if (name == "this"):
            if isinstance(value,batch_status):
                self.__dict__[name] = value.this
                if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
                del value.thisown
                return
        method = batch_status.__setmethods__.get(name,None)
        if method: return method(self,value)
        self.__dict__[name] = value

    __getmethods__ = {}
    for _s in []: __getmethods__.update(_s.__getmethods__)
    def __getattr__(self,name):
        method = batch_status.__getmethods__.get(name,None)
        if method: return method(self)
        raise AttributeError,name

    __setmethods__["name"] = pbsc.batch_status_name_set
    __getmethods__["name"] = pbsc.batch_status_name_get
    __setmethods__["attribs"] = pbsc.batch_status_attribs_set
    __getmethods__["attribs"] = pbsc.batch_status_attribs_get
    __setmethods__["text"] = pbsc.batch_status_text_set
    __getmethods__["text"] = pbsc.batch_status_text_get
    def __init__(self): raise RuntimeError, "No constructor defined"
    def __repr__(self):
        return "<C batch_status instance at %s>" % (self.this,)

class batch_statusPtr(batch_status):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = batch_status
pbsc.batch_status_swigregister(batch_statusPtr)
#  PBS python interface
#  Author: Bas van der Vlies <basv@sara.nl>
#  Date  : 27 Feb 2002
#  Desc. : This is python wrapper class for getting the resource
#          mom values.
#
# CVS info
# $Id: pbs.py,v 1.7 2003/03/03 09:37:37 sscpbas Exp $
# $Date: 2003/03/03 09:37:37 $
# $Revision: 1.7 $
#
import string
import types
# Default linux resources to get from the mom
#
default_linux_res = [   
	"availmem",	# available memory size in KB
	"ideal_load",	# static ideal_load value
	"loadave",      # the current load average
	"max_load",	# static max_load value
	"ncpus",        # number of cpus
	"physmem",      # physical memory size in KB
	"resi",		# resident memory size for a pid or session in KB
	"totmem",	# total memory size in KB
	"walltime",	# wall clock time for a pid
]
# Default irix6 resources to get from the mom
#
default_irix6_res = [   
	"availmem",	# available memory size in KB
	"loadave",      # the current load average
	"ncpus",        # number of cpus
	"physmem",      # physical memory size in KB
	"resi",		# resident memory size for a pid or session in KB
	"walltime",	# wall clock time for a pid
	"quota",	# quota information (sizes in KB)
]
default_mom_res = [   
	"arch",		# the architecture of the machine
	"uname",	# the architecture of the machine
        "cput",		# cpu time for a pid or session
	"idletime",	# seconds of idle time
	"mem",		# memory size for a pid or session in KB
	"sessions",	# list of sessions in the system
	"pids",         # list of pids in a session
	"nsessions",	# number of sessions in the system
	"nusers",	# number of users in the system
	"size",		# size of a file or filesystem
]
def check_resp(dict, str):
  """
  Check the daemon response. If we have no permission to
  query the values then we got a 'None' response. Else
  if we supplied a keyword that does not exits we get a
  '?' response
  """
  if not str:
    return
      
  key, val = string.split(str, '=')
  key = string.strip(key)
  val = string.strip(val)
  # Did we got a valid response
  #
  if not val[0] == '?':
    dict[key] = val
def use_default_keywords(id, d):
  """
  Get the default values from the mom daemon
  """
  for res in default_mom_res:
    addreq(id, res)
    resp = getreq(id)
    check_resp(d, resp)
  # Do not proceed if we have an empty dictionary
  #
  if not d:
    return
  if d['arch' ] == 'linux':
    for res in default_linux_res:
      addreq(id, res)
      resp = getreq(id)
      check_resp(d, resp)
def use_user_keywords(id, d, l):
  for res in l:
    if type(res) is types.StringType:
      addreq(id, res)
      resp = getreq(id)
      check_resp(d, resp)
    else:
      raise TypeError, 'Expected a string got %s :%s' %(type(res), res) 
def get_mom_values(id, list = None):
  """
  This function will query the mom with a default resmon keywords
  and 'arch' depended keywords. Supported archs are:
    linux
    irix6
  User can also supply their own list of keywords as second parameter.
  arguments:
    id   : connection number with mom daemon on a node
    list : optional parameter. If supplied then use this. A list
           of mom keywords.
  """
  d = {}
  if not list:
    use_default_keywords(id, d)
  else:
    use_user_keywords(id, d , list)
     
  return d


def version():
  """
  Returns the pbs python interface version as a string. 
  """
  return '2.6'


new_attrl = pbsc.new_attrl

new_attropl = pbsc.new_attropl

new_batch_status = pbsc.new_batch_status

ATTR_a = pbsc.ATTR_a
ATTR_c = pbsc.ATTR_c
ATTR_e = pbsc.ATTR_e
ATTR_g = pbsc.ATTR_g
ATTR_h = pbsc.ATTR_h
ATTR_j = pbsc.ATTR_j
ATTR_k = pbsc.ATTR_k
ATTR_l = pbsc.ATTR_l
ATTR_m = pbsc.ATTR_m
ATTR_o = pbsc.ATTR_o
ATTR_p = pbsc.ATTR_p
ATTR_q = pbsc.ATTR_q
ATTR_r = pbsc.ATTR_r
ATTR_u = pbsc.ATTR_u
ATTR_v = pbsc.ATTR_v
ATTR_A = pbsc.ATTR_A
ATTR_M = pbsc.ATTR_M
ATTR_N = pbsc.ATTR_N
ATTR_S = pbsc.ATTR_S
ATTR_depend = pbsc.ATTR_depend
ATTR_inter = pbsc.ATTR_inter
ATTR_stagein = pbsc.ATTR_stagein
ATTR_stageout = pbsc.ATTR_stageout
ATTR_ctime = pbsc.ATTR_ctime
ATTR_exechost = pbsc.ATTR_exechost
ATTR_mtime = pbsc.ATTR_mtime
ATTR_qtime = pbsc.ATTR_qtime
ATTR_session = pbsc.ATTR_session
ATTR_euser = pbsc.ATTR_euser
ATTR_egroup = pbsc.ATTR_egroup
ATTR_hashname = pbsc.ATTR_hashname
ATTR_hopcount = pbsc.ATTR_hopcount
ATTR_security = pbsc.ATTR_security
ATTR_sched_hint = pbsc.ATTR_sched_hint
ATTR_substate = pbsc.ATTR_substate
ATTR_name = pbsc.ATTR_name
ATTR_owner = pbsc.ATTR_owner
ATTR_used = pbsc.ATTR_used
ATTR_state = pbsc.ATTR_state
ATTR_queue = pbsc.ATTR_queue
ATTR_server = pbsc.ATTR_server
ATTR_maxrun = pbsc.ATTR_maxrun
ATTR_total = pbsc.ATTR_total
ATTR_comment = pbsc.ATTR_comment
ATTR_cookie = pbsc.ATTR_cookie
ATTR_qrank = pbsc.ATTR_qrank
ATTR_altid = pbsc.ATTR_altid
ATTR_etime = pbsc.ATTR_etime
ATTR_aclgren = pbsc.ATTR_aclgren
ATTR_aclgroup = pbsc.ATTR_aclgroup
ATTR_aclhten = pbsc.ATTR_aclhten
ATTR_aclhost = pbsc.ATTR_aclhost
ATTR_acluren = pbsc.ATTR_acluren
ATTR_acluser = pbsc.ATTR_acluser
ATTR_altrouter = pbsc.ATTR_altrouter
ATTR_chkptmin = pbsc.ATTR_chkptmin
ATTR_enable = pbsc.ATTR_enable
ATTR_fromroute = pbsc.ATTR_fromroute
ATTR_killdelay = pbsc.ATTR_killdelay
ATTR_maxgrprun = pbsc.ATTR_maxgrprun
ATTR_maxque = pbsc.ATTR_maxque
ATTR_maxuserrun = pbsc.ATTR_maxuserrun
ATTR_qtype = pbsc.ATTR_qtype
ATTR_rescassn = pbsc.ATTR_rescassn
ATTR_rescdflt = pbsc.ATTR_rescdflt
ATTR_rescmax = pbsc.ATTR_rescmax
ATTR_rescmin = pbsc.ATTR_rescmin
ATTR_rndzretry = pbsc.ATTR_rndzretry
ATTR_routedest = pbsc.ATTR_routedest
ATTR_routeheld = pbsc.ATTR_routeheld
ATTR_routewait = pbsc.ATTR_routewait
ATTR_routeretry = pbsc.ATTR_routeretry
ATTR_routelife = pbsc.ATTR_routelife
ATTR_rsvexpdt = pbsc.ATTR_rsvexpdt
ATTR_rsvsync = pbsc.ATTR_rsvsync
ATTR_start = pbsc.ATTR_start
ATTR_count = pbsc.ATTR_count
ATTR_number = pbsc.ATTR_number
ATTR_aclroot = pbsc.ATTR_aclroot
ATTR_managers = pbsc.ATTR_managers
ATTR_dfltque = pbsc.ATTR_dfltque
ATTR_defnode = pbsc.ATTR_defnode
ATTR_locsvrs = pbsc.ATTR_locsvrs
ATTR_logevents = pbsc.ATTR_logevents
ATTR_logfile = pbsc.ATTR_logfile
ATTR_mailfrom = pbsc.ATTR_mailfrom
ATTR_nodepack = pbsc.ATTR_nodepack
ATTR_operators = pbsc.ATTR_operators
ATTR_queryother = pbsc.ATTR_queryother
ATTR_resccost = pbsc.ATTR_resccost
ATTR_rescavail = pbsc.ATTR_rescavail
ATTR_schedit = pbsc.ATTR_schedit
ATTR_scheduling = pbsc.ATTR_scheduling
ATTR_status = pbsc.ATTR_status
ATTR_syscost = pbsc.ATTR_syscost
ATTR_NODE_state = pbsc.ATTR_NODE_state
ATTR_NODE_np = pbsc.ATTR_NODE_np
ATTR_NODE_properties = pbsc.ATTR_NODE_properties
ATTR_NODE_ntype = pbsc.ATTR_NODE_ntype
ATTR_NODE_jobs = pbsc.ATTR_NODE_jobs
CHECKPOINT_UNSPECIFIED = pbsc.CHECKPOINT_UNSPECIFIED
NO_HOLD = pbsc.NO_HOLD
NO_JOIN = pbsc.NO_JOIN
NO_KEEP = pbsc.NO_KEEP
MAIL_AT_ABORT = pbsc.MAIL_AT_ABORT
DELDELAY = pbsc.DELDELAY
USER_HOLD = pbsc.USER_HOLD
OTHER_HOLD = pbsc.OTHER_HOLD
SYSTEM_HOLD = pbsc.SYSTEM_HOLD
ND_free = pbsc.ND_free
ND_offline = pbsc.ND_offline
ND_down = pbsc.ND_down
ND_reserve = pbsc.ND_reserve
ND_job_exclusive = pbsc.ND_job_exclusive
ND_job_sharing = pbsc.ND_job_sharing
ND_busy = pbsc.ND_busy
ND_state_unknown = pbsc.ND_state_unknown
ND_timeshared = pbsc.ND_timeshared
ND_cluster = pbsc.ND_cluster
MAX_ENCODE_BFR = pbsc.MAX_ENCODE_BFR
MGR_CMD_CREATE = pbsc.MGR_CMD_CREATE
MGR_CMD_DELETE = pbsc.MGR_CMD_DELETE
MGR_CMD_SET = pbsc.MGR_CMD_SET
MGR_CMD_UNSET = pbsc.MGR_CMD_UNSET
MGR_CMD_LIST = pbsc.MGR_CMD_LIST
MGR_CMD_PRINT = pbsc.MGR_CMD_PRINT
MGR_CMD_ACTIVE = pbsc.MGR_CMD_ACTIVE
MGR_OBJ_NONE = pbsc.MGR_OBJ_NONE
MGR_OBJ_SERVER = pbsc.MGR_OBJ_SERVER
MGR_OBJ_QUEUE = pbsc.MGR_OBJ_QUEUE
MGR_OBJ_JOB = pbsc.MGR_OBJ_JOB
MGR_OBJ_NODE = pbsc.MGR_OBJ_NODE
MSG_OUT = pbsc.MSG_OUT
MSG_ERR = pbsc.MSG_ERR
SHUT_SIG = pbsc.SHUT_SIG
SHUT_IMMEDIATE = pbsc.SHUT_IMMEDIATE
SHUT_DELAY = pbsc.SHUT_DELAY
SHUT_QUICK = pbsc.SHUT_QUICK
SIG_RESUME = pbsc.SIG_RESUME
SIG_SUSPEND = pbsc.SIG_SUSPEND
PBS_MAXHOSTNAME = pbsc.PBS_MAXHOSTNAME
MAXPATHLEN = pbsc.MAXPATHLEN
MAXNAMLEN = pbsc.MAXNAMLEN
PBS_MAXUSER = pbsc.PBS_MAXUSER
PBS_MAXGRPN = pbsc.PBS_MAXGRPN
PBS_MAXQUEUENAME = pbsc.PBS_MAXQUEUENAME
PBS_MAXSERVERNAME = pbsc.PBS_MAXSERVERNAME
PBS_MAXSEQNUM = pbsc.PBS_MAXSEQNUM
PBS_MAXPORTNUM = pbsc.PBS_MAXPORTNUM
PBS_MAXSVRJOBID = pbsc.PBS_MAXSVRJOBID
PBS_MAXCLTJOBID = pbsc.PBS_MAXCLTJOBID
PBS_MAXDEST = pbsc.PBS_MAXDEST
PBS_MAXROUTEDEST = pbsc.PBS_MAXROUTEDEST
PBS_USE_IFF = pbsc.PBS_USE_IFF
PBS_INTERACTIVE = pbsc.PBS_INTERACTIVE
PBS_TERM_BUF_SZ = pbsc.PBS_TERM_BUF_SZ
PBS_TERM_CCA = pbsc.PBS_TERM_CCA
PBS_BATCH_SERVICE_NAME = pbsc.PBS_BATCH_SERVICE_NAME
PBS_BATCH_SERVICE_PORT = pbsc.PBS_BATCH_SERVICE_PORT
PBS_BATCH_SERVICE_NAME_DIS = pbsc.PBS_BATCH_SERVICE_NAME_DIS
PBS_BATCH_SERVICE_PORT_DIS = pbsc.PBS_BATCH_SERVICE_PORT_DIS
PBS_MOM_SERVICE_NAME = pbsc.PBS_MOM_SERVICE_NAME
PBS_MOM_SERVICE_PORT = pbsc.PBS_MOM_SERVICE_PORT
PBS_MANAGER_SERVICE_NAME = pbsc.PBS_MANAGER_SERVICE_NAME
PBS_MANAGER_SERVICE_PORT = pbsc.PBS_MANAGER_SERVICE_PORT
PBS_SCHEDULER_SERVICE_NAME = pbsc.PBS_SCHEDULER_SERVICE_NAME
PBS_SCHEDULER_SERVICE_PORT = pbsc.PBS_SCHEDULER_SERVICE_PORT
SET = pbsc.SET
UNSET = pbsc.UNSET
INCR = pbsc.INCR
DECR = pbsc.DECR
EQ = pbsc.EQ
NE = pbsc.NE
GE = pbsc.GE
GT = pbsc.GT
LE = pbsc.LE
LT = pbsc.LT
DFLT = pbsc.DFLT
cvar = pbsc.cvar
avail = pbsc.avail

pbs_asyrunjob = pbsc.pbs_asyrunjob

pbs_alterjob = pbsc.pbs_alterjob

pbs_connect = pbsc.pbs_connect

pbs_query_max_connections = pbsc.pbs_query_max_connections

pbs_default = pbsc.pbs_default

pbs_deljob = pbsc.pbs_deljob

pbs_disconnect = pbsc.pbs_disconnect

pbs_geterrmsg = pbsc.pbs_geterrmsg

pbs_holdjob = pbsc.pbs_holdjob

pbs_locjob = pbsc.pbs_locjob

pbs_manager = pbsc.pbs_manager

pbs_movejob = pbsc.pbs_movejob

pbs_msgjob = pbsc.pbs_msgjob

pbs_orderjob = pbsc.pbs_orderjob

pbs_rescquery = pbsc.pbs_rescquery

pbs_rescreserve = pbsc.pbs_rescreserve

pbs_rescrelease = pbsc.pbs_rescrelease

pbs_rerunjob = pbsc.pbs_rerunjob

pbs_rlsjob = pbsc.pbs_rlsjob

pbs_runjob = pbsc.pbs_runjob

pbs_selectjob = pbsc.pbs_selectjob

pbs_sigjob = pbsc.pbs_sigjob

pbs_statfree = pbsc.pbs_statfree

pbs_statjob = pbsc.pbs_statjob

pbs_selstat = pbsc.pbs_selstat

pbs_statque = pbsc.pbs_statque

pbs_statserver = pbsc.pbs_statserver

pbs_statnode = pbsc.pbs_statnode

pbs_submit = pbsc.pbs_submit

pbs_terminate = pbsc.pbs_terminate

totpool = pbsc.totpool

usepool = pbsc.usepool

openrm = pbsc.openrm

closerm = pbsc.closerm

downrm = pbsc.downrm

configrm = pbsc.configrm

addreq = pbsc.addreq

allreq = pbsc.allreq

flushreq = pbsc.flushreq

activereq = pbsc.activereq

fullresp = pbsc.fullresp

getreq = pbsc.getreq

LOG_BUF_SIZE = pbsc.LOG_BUF_SIZE
log_close = pbsc.log_close

log_err = pbsc.log_err

log_event = pbsc.log_event

log_open = pbsc.log_open

log_record = pbsc.log_record

setup_env = pbsc.setup_env

chk_file_sec = pbsc.chk_file_sec

PBSEVENT_ERROR = pbsc.PBSEVENT_ERROR
PBSEVENT_SYSTEM = pbsc.PBSEVENT_SYSTEM
PBSEVENT_ADMIN = pbsc.PBSEVENT_ADMIN
PBSEVENT_JOB = pbsc.PBSEVENT_JOB
PBSEVENT_JOB_USAGE = pbsc.PBSEVENT_JOB_USAGE
PBSEVENT_SECURITY = pbsc.PBSEVENT_SECURITY
PBSEVENT_SCHED = pbsc.PBSEVENT_SCHED
PBSEVENT_DEBUG = pbsc.PBSEVENT_DEBUG
PBSEVENT_DEBUG2 = pbsc.PBSEVENT_DEBUG2
PBSEVENT_FORCE = pbsc.PBSEVENT_FORCE
PBS_EVENTCLASS_SERVER = pbsc.PBS_EVENTCLASS_SERVER
PBS_EVENTCLASS_QUEUE = pbsc.PBS_EVENTCLASS_QUEUE
PBS_EVENTCLASS_JOB = pbsc.PBS_EVENTCLASS_JOB
PBS_EVENTCLASS_REQUEST = pbsc.PBS_EVENTCLASS_REQUEST
PBS_EVENTCLASS_FILE = pbsc.PBS_EVENTCLASS_FILE
PBS_EVENTCLASS_ACCT = pbsc.PBS_EVENTCLASS_ACCT
PBS_EVENTCLASS_NODE = pbsc.PBS_EVENTCLASS_NODE
PBSEVENT_MASK = pbsc.PBSEVENT_MASK

