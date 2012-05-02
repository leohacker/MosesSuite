%define version 1.0
%define release 1

Summary:        Test cases for Moses Suite
Name:           moses-suite-test
Version:        %{version}
Release:        %{release}%{dist}
Vendor:         MosesSuite Project
Packager:       Leo Jiang <leo.jiang.dev@gmail.com>
URL:            https://github.com/leohacker/MosesSuite/
License:        GPL
Group:          Moses Suite
Source0:        %{name}-%{version}.tar.gz
Source1:        sample-models.tgz
Buildroot:      %{_tmppath}/%{name}-root
Buildarch:      noarch
BuildRequires:  moses-suite-devel
Requires:       moses-core, moses-suite-base

%description
Pre-built sample models and several scripts for moses suite installation 
verification.

%prep
%setup -q -n %{name} -a 1

%build

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{moses_data_root}/engines
cp -a sample-models $RPM_BUILD_ROOT/%{moses_data_root}/engines/
install -m 755 -d %{buildroot}/%{moses_suite_root}/bin
install -m 755 moses-suite-test-inst.sh %{buildroot}/%{moses_suite_root}/bin/moses-suite-test-inst.sh
install -m 755 moses-server-xmlrpc-test.py %{buildroot}/%{moses_suite_root}/bin/moses-server-xmlrpc-test.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{moses_suite_root}/bin/moses-suite-test-inst.sh
%{moses_suite_root}/bin/moses-server-xmlrpc-test.py

%defattr(-,moses,moses)
%{moses_data_root}/engines/sample-models

%changelog
* Tue May 01 2012 Leo Jiang - 1.0-2
- init spec.
