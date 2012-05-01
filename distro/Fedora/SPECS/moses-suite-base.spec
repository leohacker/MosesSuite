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
Source:		%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  moses-suite-devel
Buildroot: 	%{_tmppath}/%{name}-root
URL:		http://github.com/leohacker/MosesSuite/

%description
Setup system configuration file and data directory hierarchy for Moses Suite. 

%prep
%setup -q -n %{name}

%build
# setup the root directory as rpm macros defined.
sed -i -e "s|MOSES_DATA_ROOT=|MOSES_DATA_ROOT=%{moses_data_root}|" moses-suite.conf

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/etc
install -m 644 moses-suite.conf %{buildroot}/etc/moses-suite.conf
install -m 755 -d %{buildroot}/%{moses_data_root}
install -m 755 -d %{buildroot}/%{moses_data_root}/corpus
install -m 755 -d %{buildroot}/%{moses_data_root}/engines

%clean
rm -rf %{buildroot}

%pre
# create user moses:moses for moses suite.
if ! grep "moses" /etc/passwd > /dev/null; then
    useradd moses > /dev/null
fi

%post

%preun

%postun

%files
%defattr(-,root,root)
/etc/moses-suite.conf
%defattr(-,moses,moses)
%{moses_data_root}/

%changelog
* Tue May 02 2012 Leo Jiang - 1.0-2
- add user moses if not exists, set the permission of data folder for user moses.

* Tue May 02 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
