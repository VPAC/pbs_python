/*
*         Portable Batch System (PBS) Software License
* 
* Copyright (c) 1999, MRJ Technology Solutions.
* All rights reserved.
* 
* Acknowledgment: The Portable Batch System Software was originally developed
* as a joint project between the Numerical Aerospace Simulation (NAS) Systems
* Division of NASA Ames Research Center and the National Energy Research
* Supercomputer Center (NERSC) of Lawrence Livermore National Laboratory.
* 
* Redistribution of the Portable Batch System Software and use in source
* and binary forms, with or without modification, are permitted provided
* that the following conditions are met:
* 
* - Redistributions of source code must retain the above copyright and
*   acknowledgment notices, this list of conditions and the following
*   disclaimer.
* 
* - Redistributions in binary form must reproduce the above copyright and 
*   acknowledgment notices, this list of conditions and the following
*   disclaimer in the documentation and/or other materials provided with the
*   distribution.
* 
* - All advertising materials mentioning features or use of this software must
*   display the following acknowledgment:
* 
*   This product includes software developed by NASA Ames Research Center,
*   Lawrence Livermore National Laboratory, and MRJ Technology Solutions.
* 
*         DISCLAIMER OF WARRANTY
* 
* THIS SOFTWARE IS PROVIDED BY MRJ TECHNOLOGY SOLUTIONS ("MRJ") "AS IS" WITHOUT 
* WARRANTY OF ANY KIND, AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
* BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
* FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT ARE EXPRESSLY DISCLAIMED.
* 
* IN NO EVENT, UNLESS REQUIRED BY APPLICABLE LAW, SHALL MRJ, NASA, NOR
* THE U.S. GOVERNMENT BE LIABLE FOR ANY DIRECT DAMAGES WHATSOEVER,
* NOR ANY INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
* DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
* OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
* USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
* 
* This license will be governed by the laws of the Commonwealth of Virginia,
* without reference to its choice of law rules.
*/

/*
 * @(#) $Id: pbs_error.h,v 1.1 2001/12/07 19:01:18 sscpbas Exp $
 */

/*
 * The error returns possible to a Batch Request
 *
 * Each error is prefixed with the string PBSE_ for Portable (Posix)
 * Batch System Error.  The numeric values start with 15000 since the
 * POSIX Batch Extensions Working group is 1003.15
 */
#ifndef PBSE_

#define PBSE_	15000

#define PBSE_NONE       0		/* no error */
#define PBSE_UNKJOBID	15001		/* Unknown Job Identifier */
#define PBSE_NOATTR	15002		/* Undefined Attribute */
#define PBSE_ATTRRO	15003		/* attempt to set READ ONLY attribute */
#define PBSE_IVALREQ	15004		/* Invalid request */
#define PBSE_UNKREQ	15005		/* Unknown batch request */
#define PBSE_TOOMANY	15006		/* Too many submit retries */
#define PBSE_PERM	15007		/* No permission */
#define PBSE_BADHOST	15008		/* access from host not allowed */
#define PBSE_JOBEXIST	15009		/* job already exists */
#define PBSE_SYSTEM	15010		/* system error occurred */
#define PBSE_INTERNAL	15011		/* internal server error occurred */
#define PBSE_REGROUTE	15012		/* parent job of dependent in rte que */
#define PBSE_UNKSIG	15013		/* unknown signal name */
#define PBSE_BADATVAL	15014		/* bad attribute value */
#define PBSE_MODATRRUN	15015		/* Cannot modify attrib in run state */
#define PBSE_BADSTATE	15016		/* request invalid for job state */
#define PBSE_UNKQUE	15018		/* Unknown queue name */
#define PBSE_BADCRED	15019		/* Invalid Credential in request */
#define PBSE_EXPIRED	15020		/* Expired Credential in request */
#define PBSE_QUNOENB	15021		/* Queue not enabled */
#define PBSE_QACESS	15022		/* No access permission for queue */
#define PBSE_BADUSER	15023		/* Bad user - no password entry */
#define PBSE_HOPCOUNT	15024		/* Max hop count exceeded */
#define PBSE_QUEEXIST	15025		/* Queue already exists */
#define PBSE_ATTRTYPE	15026		/* incompatable queue attribute type */
#define PBSE_QUEBUSY	15027		/* Queue Busy (not empty) */
#define PBSE_QUENBIG	15028		/* Queue name too long */
#define PBSE_NOSUP	15029		/* Feature/function not supported */
#define PBSE_QUENOEN	15030		/* Cannot enable queue,needs add def */
#define PBSE_PROTOCOL	15031		/* Protocol (ASN.1) error */
#define PBSE_BADATLST	15032		/* Bad attribute list structure */
#define PBSE_NOCONNECTS	15033		/* No free connections */
#define PBSE_NOSERVER	15034		/* No server to connect to */
#define PBSE_UNKRESC	15035		/* Unknown resource */
#define PBSE_EXCQRESC	15036		/* Job exceeds Queue resource limits */
#define PBSE_QUENODFLT	15037		/* No Default Queue Defined */
#define PBSE_NORERUN	15038		/* Job Not Rerunnable */
#define PBSE_ROUTEREJ	15039		/* Route rejected by all destinations */
#define PBSE_ROUTEEXPD	15040		/* Time in Route Queue Expired */
#define PBSE_MOMREJECT  15041		/* Request to MOM failed */
#define PBSE_BADSCRIPT	15042		/* (qsub) cannot access script file */
#define PBSE_STAGEIN	15043		/* Stage In of files failed */
#define PBSE_RESCUNAV	15044		/* Resources temporarily unavailable */
#define PBSE_BADGRP	15045		/* Bad Group specified */
#define PBSE_MAXQUED	15046		/* Max number of jobs in queue */
#define PBSE_CKPBSY	15047		/* Checkpoint Busy, may be retries */
#define PBSE_EXLIMIT	15048		/* Limit exceeds allowable */
#define PBSE_BADACCT	15049		/* Bad Account attribute value */
#define PBSE_ALRDYEXIT	15050		/* Job already in exit state */
#define PBSE_NOCOPYFILE	15051		/* Job files not copied */
#define PBSE_CLEANEDOUT	15052		/* unknown job id after clean init */
#define PBSE_NOSYNCMSTR	15053		/* No Master in Sync Set */
#define PBSE_BADDEPEND	15054		/* Invalid dependency */
#define PBSE_DUPLIST	15055		/* Duplicate entry in List */
#define PBSE_DISPROTO	15056		/* Bad DIS based Request Protocol */
#define PBSE_EXECTHERE	15057		/* cannot execute there */
#define PBSE_SISREJECT	15058		/* sister rejected */
#define PBSE_SISCOMM	15059		/* sister could not communicate */
#define PBSE_SVRDOWN	15060		/* req rejected -server shutting down */
#define PBSE_CKPSHORT	15061		/* not all tasks could checkpoint */
#define PBSE_UNKNODE	15062		/* Named node is not in the list */
#define PBSE_UNKNODEATR	15063		/* node-attribute not recognized */
#define PBSE_NONODES	15064		/* Server has no node list */
#define PBSE_NODENBIG	15065		/* Node name is too big */
#define PBSE_NODEEXIST	15066		/* Node name already exists */
#define PBSE_BADNDATVAL	15067		/* Bad node-attribute value */
#define PBSE_MUTUALEX	15068		/* State values are mutually exclusive */
#define PBSE_GMODERR	15069		/* Error(s) during global modification of nodes */
#define PBSE_NORELYMOM	15070		/* could not contact Mom */
#define PBSE_NOTSNODE	15071		/* no time-shared nodes */

/*
** 	Resource monitor specific
*/
#define PBSE_RMUNKNOWN	15201		/* resource unknown */
#define PBSE_RMBADPARAM	15202		/* parameter could not be used */
#define PBSE_RMNOPARAM	15203		/* a parameter needed did not exist */
#define PBSE_RMEXIST	15204		/* something specified didn't exist */
#define PBSE_RMSYSTEM	15205		/* a system error occured */
#define PBSE_RMPART	15206		/* only part of reservation made */
#define RM_ERR_UNKNOWN	PBSE_RMUNKNOWN
#define RM_ERR_BADPARAM	PBSE_RMBADPARAM
#define RM_ERR_NOPARAM	PBSE_RMNOPARAM
#define RM_ERR_EXIST	PBSE_RMEXIST
#define RM_ERR_SYSTEM	PBSE_RMSYSTEM


/* the following structure is used to tie error number      */
/* with text to be returned to a client, see svr_messages.c */

struct pbs_err_to_txt {
	int    err_no;
	char **err_txt;
};

extern char *pbse_to_txt();

#endif
