%define release 1
%define version 2.4.4

Name: 		chasen-moses
Summary: 	chasen and dic files for moses suite.
Version: 	%{version}
Release: 	%{release}%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	Open Source
Group: 		Moses Suite
Source: 	%{name}-%{version}.tar.gz
Buildroot: 	%{_tmppath}/%{name}-root
URL:		http://chasen-legacy.sourceforge.jp/

%description
Morphological Analysis System for Japanese.

%prep
%setup -q

%build
sed -i -e "s|(GRAMMAR  ./dic)|(GRAMMAR  %{moses_suite_root}/chasen/dic)|" chasenrc
cd src
make && make install
cd ../dic
make 

%install
rm -rf %{buildroot}
%define destdir %{buildroot}/%{moses_suite_root}
install -m 755 -d %{destdir}/chasen
install -m 444 README %{destdir}/chasen
install -m 755 chasen %{destdir}/chasen
install -m 644 chasenrc %{destdir}/chasen
install -m 755 -d %{destdir}/chasen/dic
cp -a dic/* %{destdir}/chasen/dic

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
%{moses_suite_root}/chasen/

%changelog
* Tue Jun 26 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
