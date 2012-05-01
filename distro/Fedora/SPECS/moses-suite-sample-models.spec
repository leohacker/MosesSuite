%define version 1.0
%define release 1

Summary:        Sample models for Moses
Name:           moses-suite-sample-models
Version:        %{version}
Release:        %{release}%{dist}
Vendor:         MosesSuite Project
Packager:       Leo Jiang <leo.jiang.dev@gmail.com>
URL:            https://github.com/leohacker/MosesSuite/
License:        GPL
Group:          Moses Suite
Source0:        sample-models.tgz
Buildroot:      %{_tmppath}/%{name}-root
Buildarch:      noarch
BuildRequires:  moses-suite-devel
Requires:       moses-core

%description
Pre-built sample models for moses and several scripts for moses installation
verification.

%prep
%setup -q -n sample-models

%build

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{moses_data_root}/engines/
cd %{_builddir}
cp -a sample-models $RPM_BUILD_ROOT/%{moses_data_root}/engines/

%files
%defattr(-,moses,moses)
%{moses_data_root}/engines/sample-models

%changelog
* Tue May 01 2012 Leo Jiang - 1.0-2
- rebuilt
