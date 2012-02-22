%define dist    MosesSuite
%define release 1
%define version v1.0.6

Name: 		gizapp
Summary: 	GIZA++ and mkcls
Version: 	%{version}
Release: 	%{release}.%{dist}
Vendor: 	MosesSuite
License: 	GNU GPL v2
Group: 		NLP Tools
Source: 	giza-pp.tgz
Patch0:		giza-pp.patch
BuildRequires: 	gcc gcc-c++
Buildroot: 	%{_tmppath}/%{name}-root
URL:		https://github.com/leohacker/MosesSuite

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
%setup -q -n giza-pp
%patch0 -p1

%build
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/tools/gizapp/bin
install -m 755 GIZA++-v2/GIZA++ %{buildroot}/tools/gizapp/bin
install -m 755 mkcls-v2/mkcls %{buildroot}/tools/gizapp/bin
install -m 755 GIZA++-v2/snt2cooc.out %{buildroot}/tools/gizapp/bin

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
/tools/gizapp
/tools/gizapp/bin/
/tools/gizapp/bin/GIZA++
/tools/gizapp/bin/mkcls
/tools/gizapp/bin/snt2cooc.out

%changelog
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
