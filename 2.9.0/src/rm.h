/*
 * $Id: rm.h,v 1.1 2002/02/27 14:34:51 sscpbas Exp $
 *
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
 * @(#) $Id: rm.h,v 1.1 2002/02/27 14:34:51 sscpbas Exp $
 */

/*
**	Header file defineing the library calls for connecting
**	to the resource monitor.
*/

int	openrm(char *, unsigned int);
int	closerm(int);
int	downrm(int);
int	configrm(int, char *);
int	addreq(int, char *);
int	allreq(char *);
int	flushreq(void);
int	activereq(void);
void	fullresp(int);

char*  getreq(int);
