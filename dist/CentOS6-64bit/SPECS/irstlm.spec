%define dist MosesSuite
%define release 1
%define version 5.70.04

Summary: 	IRST Language Modeling Toolkit
Name: 		irstlm
Version: 	%{version}
Release: 	%{release}.%{dist}
Vendor: 	MosesSuite
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	Open Source LGPL
Group: 		NLP Tools
Source: 	irstlm-%{version}.tgz
Patch0:		irstlm-script-makefile.am.patch
Buildroot: 	%{_tmppath}/%{name}-root
#BuildRequires: tcl-devel
BuildRequires: 	gcc-c++ >= 4.1
URL:		http://hlt.fbk.eu/en/irstlm

%description 
The IRST Language Modeling Toolkit features algorithms and data structures 
suitable to estimate, store, and access very large LMs. Our software has been 
integrated into a popular open source Statistical Machine Translation decoder 
called Moses, and is compatible with language models created with other tools, 
such as the SRILM Toolkit.

%prep
%setup -q -n irstlm-%{version}
%patch0 -p1

%build
./regenerate-makefiles.sh
./configure --prefix=/tools/irstlm --enable-caching
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/tools/irstlm
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
/tools/irstlm

%changelog
* Thu Feb 23 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- update upstream source code.

* Tue Aug 09 2011 Moses - 5.60.02-3.adobe
- remove the relocatable.

* Tue Aug 09 2011 Moses - 5.60.02-2.adobe
- add the prefix.

* Wed Aug 03 2011 Leo Jiang <ljiang@adobe.com>
- create the rpm spec for irstlm.
