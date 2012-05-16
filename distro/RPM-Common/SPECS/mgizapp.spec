%define release 1
%define version 0.6.3

Name: 		mgizapp
Summary: 	Multi-threads version of GIZA++ and mkcls
Version: 	%{version}
Release: 	%{release}%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	GNU GPL v2
Group: 		Moses Suite
Source: 	%{name}-%{version}.tar.gz
BuildRequires: 	glibc-devel, glibc-headers
BuildRequires:  libstdc++-devel
BuildRequires:  moses-suite-devel
Requires:	tcsh, libstdc++
Requires:       moses-suite-base, giza-pp
Buildroot: 	%{_tmppath}/%{name}-root
URL:		http://www.kyloo.net/software/doku.php/mgiza:overview

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

This is the multi-thread version extends GIZA++ created by Qin Gao
(http://geek.kyloo.net).

%prep
%setup -q -n %{name}

%build
./configure --prefix=%{moses_suite_root}/mgizapp/
make

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{moses_suite_root}/mgizapp/
install -m 755 -d %{buildroot}/%{moses_suite_root}/giza-pp/bin/
make DESTDIR=$RPM_BUILD_ROOT install
cp %{buildroot}/%{moses_suite_root}/mgizapp/bin/mgiza %{buildroot}/%{moses_suite_root}/giza-pp/bin/mgiza
cp %{buildroot}/%{moses_suite_root}/mgizapp/scripts/merge_alignment.py %{buildroot}/%{moses_suite_root}/giza-pp/bin/

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
%{moses_suite_root}/giza-pp/bin/mgiza
%{moses_suite_root}/giza-pp/bin/merge_alignment.py
%{moses_suite_root}/mgizapp/

%changelog
* Wed May 16 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
