%define release 5
%define version 1.0.7

Name: 		giza-pp
Summary: 	GIZA++ and mkcls
Version: 	%{version}
Release: 	%{release}%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	GNU GPL v2
Group: 		Moses Suite
Source: 	%{name}-v%{version}.tar.gz
BuildRequires: 	glibc-devel, glibc-headers
BuildRequires:  libstdc++-devel
BuildRequires:  moses-suite-devel
Requires:	tcsh, libstdc++
Requires:       moses-suite-base
Buildroot: 	%{_tmppath}/%{name}-root
URL:		http://code.google.com/p/giza-pp/

%description
GIZA++ is a statical machine translation toolkit that is used to train IBM
Models 1-5 and an HMM word alignment model. This package also contains the
source for the mkcls tool which generates the word classes necessary for
training some of the alignment models.

For more information on the origins of these tools, refer to http://www.statmt
.org/moses/giza/GIZA++.html and http://www.statmt.org/moses/giza/mkcls.html.

If you make use of GIZA++ for research or commercial purpose, please cite:
- Franz Josef Och, Hermann Ney. "A Systematic Comparision of Various
Statistical Alignment Models", Computational Linguistics, volume 29, number 1,
pp. 19-51 March 2003.

%prep
%setup -q -n %{name}

%build
make

%install
rm -rf %{buildroot}
%define destdir %{buildroot}/%{moses_suite_root}
install -m 755 -d %{destdir}/giza-pp/bin
install -m 755 GIZA++-v2/GIZA++ %{destdir}/giza-pp/bin
install -m 755 GIZA++-v2/*.out %{destdir}/giza-pp/bin
install -m 755 GIZA++-v2/*.sh %{destdir}/giza-pp/bin
install -m 755 mkcls-v2/mkcls %{destdir}/giza-pp/bin

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
%{moses_suite_root}/giza-pp/

%changelog
* Tue May 08 2012 Leo Jiang - 1.0.7-5
- add moses-suite-base as dependence.

* Tue May 01 2012 Leo Jiang - 1.0.7-4
- rename the package and add the moses-suite-devel as build requires.

* Sun Apr 29 2012 Leo Jiang - 1.0.7-3.fc16
- remove the macro tag and replace the installation path with macro moses_suite_root.

* Wed Apr 25 2012 Leo Jiang - v1.0.7-2.MosesSuite
- build for Fedora16.

* Thu Apr 12 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- we don't need the patch file now since upstream had removed the static flag in makefile.

* Wed Feb 22 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- update the source code to giza-pp.tgz from upstream, and patch the makefile because there is no 64bit static library on CentOS6.

* Tue Aug 09 2011 Moses <leo.jiang.dev@gmail.com>
- remove the relocatable.

* Mon Aug 08 2011 Moses <leo.jiang.dev@gmail.com>
- make the package relocatable.

* Wed Aug 03 2011 Leo Jiang <leo.jiang.dev@gmail.com>
- add the patch0.

* Wed Apr 20 2011 Leo Jiang <leo.jiang.dev@gmail.com>
- update the rpm spec.

* Mon Apr 18 2011 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
