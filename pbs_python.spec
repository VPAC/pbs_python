Summary: This package contains the pbs python module.
Name: pbs_python
Version: %{prodversion}
Release: %{prodrelease}
License: See LICENSE
Group: Development/Libraries
Source: ftp://ftp.sara.nl/pub/outgoing/pbs_python.tar.gz 
BuildRoot: /var/tmp/%{name}-buildroot


%description
This package contains the pbs python module.

%prep
%setup -q
./configure --with-pbsdir=%{libdir}

%build
python setup.py build

%install
echo %{pythonlib}
echo %{libdir}
python ./setup.py install --prefix $RPM_BUILD_ROOT/usr ;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README TODO examples
%{libdir}/%{pythonlib}/site-packages/pbs.pth
%{libdir}/%{pythonlib}/site-packages/pbs/*

%changelog
* Tue May  5 2009 Michel Jouvin <jouvin@lal.in2p3.fr>
- Rework spec file to make it generic with respect to platforms, python version... Intended to be used with Makefile.rpm
* Sun Mar  9 2008 Michael Sternberg <sternberg@anl.gov>
- libdir and python defines
* Wed Nov 23 2005 Ramon Bastiaans <bastiaans@sara.nl>
- Fixed missing prep setup and added configure
* Tue Nov 22 2005 Martin Pels <pels@sara.nl>
- Changed default directory permissions
* Tue Nov 01 2005 Martin Pels <pels@sara.nl> 
- Initial version

