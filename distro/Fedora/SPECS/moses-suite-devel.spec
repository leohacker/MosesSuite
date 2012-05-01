%define release 1
%define version 1.0

Name: 		moses-suite-devel
Summary: 	Devel package of Moses Suite.
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
Setup rpm macros for building packages in group Moses Suite. Those packges in 
group Moses Suite share same root directory which is defined as rpm macros in 
file macros.moses.

%prep
%setup -q -n %{name}

%build

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/etc/rpm/
install -m 644 macros.moses %{buildroot}/etc/rpm/

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
/etc/rpm/macros.moses

%changelog
* Tue May 01 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- init package.
