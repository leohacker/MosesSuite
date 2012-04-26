%define dist    fc16
%define release 2
%define version 5.70.04
%define tag     moses

Summary: 	IRST Language Modeling Toolkit
Name: 		irstlm
Version: 	%{version}
Release: 	%{release}.%{tag}.%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	LGPL
Group: 		Moses Suite
Source: 	irstlm-%{version}.tgz
Patch0:		irstlm-script-makefile.am.patch
Buildroot: 	%{_tmppath}/%{name}-root
BuildRequires:  autoconf, automake, libtool, m4
BuildRequires:  ccache, zlib-devel, libstdc++-devel
BuildRequires:  glibc-common, glibc-devel, glibc-headers
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
* Wed Apr 25 2012 Leo Jiang - 5.70.04-2.MosesSuite
- build for Fedora16.

* Thu Feb 23 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- update upstream source code.

* Tue Aug 09 2011 Moses - 5.60.02-3.adobe
- remove the relocatable.

* Tue Aug 09 2011 Moses - 5.60.02-2.adobe
- add the prefix.

* Wed Aug 03 2011 Leo Jiang <ljiang@adobe.com>
- create the rpm spec for irstlm.
