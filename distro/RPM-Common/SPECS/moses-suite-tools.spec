%define release 2
%define version 1.0

Name: 		moses-suite-tools
Summary: 	Moses Suite Tools
Version: 	%{version}
Release: 	%{release}%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	GNU GPL v2
Group: 		Moses Suite
Source:		%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  moses-suite-devel
Requires:       moses-suite-base
Buildroot: 	%{_tmppath}/%{name}-root
URL:		http://github.com/leohacker/MosesSuite/

%description
Some tools/scripts to support moses suite.

%prep
%setup -q -n %{name}

%build

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{moses_suite_root}
install -m 755 -d %{buildroot}/%{moses_suite_root}/bin/
install -m 755 moses-suite.functions %{buildroot}/%{moses_suite_root}/bin/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{moses_suite_root}/bin/

%changelog
* Fri May 11 2012 Leo Jiang - 1.0-2
- remove the tm-setuptree script and the function in function script.

* Thu May 10 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- init spec.
