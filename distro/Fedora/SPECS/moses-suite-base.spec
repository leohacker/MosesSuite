%define release 2
%define version 1.0

Name: 		moses-suite-base
Summary: 	Base package of Moses Suite.
Version: 	%{version}
Release: 	%{release}%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	GNU GPL v2
Group: 		Moses Suite
Source:		%{name}.tar.gz
BuildArch:      noarch
Buildroot: 	%{_tmppath}/%{name}-root
URL:		http://github.com/leohacker/MosesSuite/

%description
Moses suite configuration and generated rpm macros file for moses according to
this configuration file.

%prep
%setup -q -n %{name}

%build
./generate-rpmmacros.sh

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{moses_suite_root}
install -m 755 -d %{buildroot}/etc/rpm/
install -m 644 macros.moses %{buildroot}/etc/rpm/
install -m 644 moses-suite.conf %{buildroot}/etc/

%clean
#rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
#%{moses_suite_root}/
#%{moses_data_root}/
/etc/rpm/macros.moses
/etc/moses-suite.conf

%changelog
* Tue May 01 2012 Leo Jiang - 1.0-2
- rename the package to moses-suite-base.

* Mon Apr 02 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- rename the name for package and source tarball.

* Fri Mar 30 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
