%define dist    fc16
%define release 3
%define version 1.6.0
%define tag     moses

Name: 		srilm
Summary: 	SRI Language Modeling Toolkit
Version: 	%{version}
Release: 	%{release}.%{tag}.%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	SRILM Research Community License
Group: 		Moses Suite
Source: 	srilm-%{version}.tar.gz
Patch0: 	srilm-NoTCL-RemoveUserLocal.patch
Buildroot: 	%{_tmppath}/%{name}-root
BuildRequires: 	tcsh, glibc-devel, glibc-headers, libstdc++-devel 
Requires: 	tcsh
URL:		http://www.speech.sri.com/projects/srilm/

%description 
RILM is a toolkit for building and applying statistical language models (LMs), 
primarily for use in speech recognition, statistical tagging and segmentation, 
and machine translation.

%prep
%setup -q
%patch0 -p1

%build
make SRILM=$PWD World

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/tools/srilm 
install -m 755 -d %{buildroot}/tools/srilm/bin
install -m 755 -d %{buildroot}/tools/srilm/sbin
install -m 755 -d %{buildroot}/tools/srilm/lib/i686
install -m 755 -d %{buildroot}/tools/srilm/include
install -m 755 -d %{buildroot}/tools/srilm/doc
cp -a bin/ %{buildroot}/tools/srilm/
cp -a sbin/ %{buildroot}/tools/srilm/
cp -a lib/ %{buildroot}/tools/srilm/
cp -a include/ %{buildroot}/tools/srilm/
cp -a doc/ %{buildroot}/tools/srilm/
install -m 755 doc/* %{buildroot}/tools/srilm/doc/
install -m 444 Copyright %{buildroot}/tools/srilm/
install -m 444 CHANGES %{buildroot}/tools/srilm/
install -m 444 License %{buildroot}/tools/srilm/

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
/tools/srilm

%changelog
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
