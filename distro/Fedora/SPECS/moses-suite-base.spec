%define dist    fc16
%define release 1
%define version 1.0

Name: 		moses-suite-filesystem
Summary: 	Definition of Moses Suite File system.
Version: 	%{version}
Release: 	%{release}.%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	GNU GPL v2
Group: 		Moses Suite
Source:		moses-suite-filesystem.tar.gz
BuildArch:      noarch
Buildroot: 	%{_tmppath}/%{name}-root
URL:		http://github.com/leohacker/MosesSuite/

%description
File system definition, configuration file and corpus management tools.

%prep
%setup -q -n moses-suite-filesystem

%build
echo "================================================"
pwd
sed -i -e "s|/tools|%{moses_suite_root}|" moses-suite.conf
sed -i -e "s|/data|%{moses_data_root}|" moses-suite.conf

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{moses_data_root}/
mkdir -p %{buildroot}/%{moses_data_root}/corpus
mkdir -p %{buildroot}/%{moses_data_root}/engines
mkdir -p %{buildroot}/%{moses_suite_root}/bin
install -m 755 moses-suite-corpus-setuptree.sh %{buildroot}/%{moses_suite_root}/bin

%clean
#rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
%{moses_data_root}/
%{moses_data_root}/corpus
%{moses_data_root}/engines
%{moses_suite_root}/bin/moses-suite-corpus-setuptree.sh

%changelog
* Mon Apr 02 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- rename the name for package and source tarball.

* Fri Mar 30 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
