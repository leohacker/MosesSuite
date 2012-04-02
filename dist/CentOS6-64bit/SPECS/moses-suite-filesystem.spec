%define dist    MosesSuite
%define release 1
%define version v1.0

Name: 		moses-suite-filesystem
Summary: 	File system of MosesSuite.
Version: 	%{version}
Release: 	%{release}.%{dist}
Vendor: 	MosesSuite
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	GNU GPL v2
Group: 		NLP Tools
Source:		moses-suite-filesystem.tar.gz
Buildroot: 	%{_tmppath}/%{name}-root
Requires:	moses-core
URL:		http://github.com/leohacker/MosesSuite/

%description
Setup the file system, or directory hierarchy for corpus management in moses
suite.

%prep
%setup -q -n moses-suite-filesystem

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/data/
mkdir -p %{buildroot}/data/corpus
mkdir -p %{buildroot}/data/engines
mkdir -p %{buildroot}/tools/bin
install -m 755 create-corpus-dir.sh %{buildroot}/tools/bin

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
/data/
/data/corpus
/data/engines
/tools/bin/create-corpus-dir.sh

%changelog
* Mon Apr 02 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- rename the name for package and source tarball.

* Fri Mar 30 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
