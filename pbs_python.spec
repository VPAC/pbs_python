Summary: This package contains the pbs python module.
Name: pbs_python
Version: 2.7.10 
Release: 1
Copyright: See LICENSE
Group: Development/Libraries
Source: ftp://ftp.sara.nl/pub/outgoing/pbs_python.tar.gz 
BuildRoot: /var/tmp/%{name}-buildroot

%description
This package contains the pbs python module.

%prep
%setup -q

%build
python setup.py build

%install
python ./setup.py install --prefix $RPM_BUILD_ROOT/usr ;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO examples

/usr/lib/python2.2/site-packages/pbs/pbs.py
/usr/lib/python2.2/site-packages/pbs/PBSQuery.py
/usr/lib/python2.2/site-packages/pbs/_pbs.so
/usr/lib/python2.2/site-packages/pbs/pbs.pyc
/usr/lib/python2.2/site-packages/pbs/PBSQuery.pyc
/usr/lib/python2.2/site-packages/pbs.pth

%changelog
* Tue Nov 01 2005 Martin Pels <pels@sara.nl> 
- Initial version
