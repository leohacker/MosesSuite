%define release 6
%define version 1.6.0

Name: 		srilm
Summary: 	SRI Language Modeling Toolkit
Version: 	%{version}
Release: 	%{release}%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	SRILM Research Community License
Group: 		Moses Suite
Source: 	%{name}-%{version}.tar.gz
Patch0: 	srilm-NoTCL-RemoveUserLocal.patch
Buildroot: 	%{_tmppath}/%{name}-root
BuildRequires: 	tcsh, glibc-devel, glibc-headers, libstdc++-devel 
BuildRequires:  moses-suite-devel
Requires: 	tcsh
Requires:       moses-suite-base
URL:		http://www.speech.sri.com/projects/srilm/

%description 
SRILM is a toolkit for building and applying statistical language models (LMs), 
primarily for use in speech recognition, statistical tagging and segmentation, 
and machine translation.

%prep
%setup -q
%patch0 -p1

%build
make SRILM=$PWD World

%install
rm -rf %{buildroot}
%define destdir %{buildroot}/%{moses_suite_root}
install -m 755 -d %{destdir}/srilm 
install -m 755 -d %{destdir}/srilm/bin
install -m 755 -d %{destdir}/srilm/sbin
install -m 755 -d %{destdir}/srilm/lib/i686
install -m 755 -d %{destdir}/srilm/include
install -m 755 -d %{destdir}/srilm/doc
cp -a bin/ %{destdir}/srilm/
cp -a sbin/ %{destdir}/srilm/
cp -a lib/ %{destdir}/srilm/
cp -a include/ %{destdir}/srilm/
cp -a doc/ %{destdir}/srilm/
install -m 755 doc/* %{destdir}/srilm/doc/
install -m 444 Copyright %{destdir}/srilm/
install -m 444 CHANGES %{destdir}/srilm/
install -m 444 License %{destdir}/srilm/

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
%{moses_suite_root}/srilm

%changelog
* Tue May 08 2012 Leo Jiang - 1.6.0-6
- add moses-suite-base as requires.

* Tue May 01 2012 Leo Jiang - 1.6.0-5
- add moses-suite-devel as build requires.

* Sun Apr 29 2012 Leo Jiang - 1.6.0-4.fc16
- remove tag and replace the installation path with rpm macros.

* Wed Apr 25 2012 Leo Jiang - 1.6.0-3.MosesSuite
- modify this spec for building on Fedora16.

* Wed Feb 22 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- update the source code to version 1.6.0.

* Tue Aug 09 2011 Moses - 1.6.0.beta-4.adobe
- remove the relocatable.

* Mon Aug 08 2011 Moses <ljiang@adobe.com>
- make the package relocatable.

* Wed Aug 03 2011 Leo Jiang <ljiang@adobe.com>
- update the SRILM to 1.6.0, patch the source code for compiling for i686 only.

* Mon Apr 19 2011 Leo Jiang <ljiang@adobe.com>
- create the rpm spec for srilm, and make some change to original Makefile.
