%define dist    fc16
%define version 1.0
%define release 1
%define tag     moses

Summary:        Sample models for Moses
Name:           moses-suite-sample-models
Version:        %{version}
Release:        %{release}.%{tag}.%{dist}
Vendor:         MosesSuite Project
Packager:       Leo Jiang <leo.jiang.dev@gmail.com>
URL:            https://github.com/leohacker/MosesSuite/
License:        GPL
Group:          Moses Suite
Source0:        sample-models.tgz
Buildroot:      %{_tmppath}/%{name}-root
Buildarch:      noarch


#BuildRequires:  
#Requires:       

%description
Pre-built sample models for moses and several scripts for moses installation
verification.

%prep
%setup -q -n sample-models

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/data/engines/
#make install DESTDIR=$RPM_BUILD_ROOT
cd %{_builddir}
cp -a sample-models $RPM_BUILD_ROOT/data/engines/

%files
#%doc
/data/engines/sample-models


%changelog
