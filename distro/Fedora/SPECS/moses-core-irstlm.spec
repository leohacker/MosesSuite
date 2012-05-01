%define dist    fc16
%define version 1.0
%define release 7
%define release_date 20120224

Summary: 	Statistical Machine Translation System with IRSTLM support
Name: 		moses-core-irstlm
Version: 	%{version}
Release: 	%{release}.%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	LGPL
Group: 		Moses Suite
Source0: 	mosesdecoder-%{release_date}.tar.bz2
Buildroot: 	%{_tmppath}/%{name}-root
BuildRequires: 	glibc-devel, glibc-headers, libstdc++-devel 
BuildRequires: 	boost-devel, xmlrpc-c-devel, zlib-devel 
BuildRequires: 	gizapp, irstlm
Requires: 	boost, xmlrpc-c, gizapp, irstlm, zlib, perl-CGI, perl-GD, perl-XML-Twig, perl-Switch
Conflicts:      moses-core, moses-core-srilm
URL:		https://github.com/leohacker/MosesSuite

%description 
Moses is a statistical machine translation system that allows you to 
automatically train translation models for any language pair. All you need is 
a collection of translated texts (parallel corpus). An efficient search 
algorithm finds quickly the highest probability translation among the 
exponential number of choices. 

This version of Mosos Core package is compiled with IRSTLM support.

%prep
%setup -q -T -b 0 -n mosesdecoder

%build

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{moses_suite_root}/moses
./bjam -a --notrace -j4 --with-irstlm=%{moses_suite_root}/irstlm --with-xmlrpc-c --with-giza=%{moses_suite_root}/gizapp/bin --prefix=$RPM_BUILD_ROOT/%{moses_suite_root}/moses --includedir=$RPM_BUILD_ROOT/%{moses_suite_root}/moses/include --install-scripts=$RPM_BUILD_ROOT/%{moses_suite_root}/moses/scripts

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
%{moses_suite_root}/moses/

%changelog
* Sun Apr 29 2012 Leo Jiang - 1.0-7.fc16
- build with irstlm support.

* Sun Apr 29 2012 Leo Jiang - 1.0-6.fc16
- remove tag and replace installation path with rpmmacros.

* Sat Apr 28 2012 Leo Jiang - 1.0-5.moses.fc16
- append "srilm" to the name.

* Thu Apr 26 2012 Leo Jiang - 1.0-4.MosesSuite
- correct the parameter list for bjam.

* Wed Apr 25 2012 Leo Jiang - 1.0-3.MosesSuite
- build for Fedora16.

* Thu Apr 12 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- remove the .git directory from source tarball.

* Mon Apr 02 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- include the scripts in.

* Fri Mar 30 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- Change the package name from 'moses' to 'mosescore'.

* Sun Feb 26 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- Using the bjam to compile in spec file.

* Fri Feb 24 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- update the upstream source code to 20120224.

* Wed Aug 10 2011 Leo Jiang - 1.0-5.adobe <ljiang@adobe.com>
- set the executable bit for mteval-v11b.pl. 

* Tue Aug 09 2011 Leo Jiang - 1.0-4 <ljiang@adobe.com>
- add the additional scripts into this package.

* Thu Aug 04 2011 Leo Jiang <ljiang@adobe.com>
- update the moses to rivision 4081.

* Mon Apr 25 2011 Leo Jiang <ljiang@adobe.com>
- Add the lines to compile and install the moses-scripts.

* Mon Apr 25 2011 Leo Jiang <ljiang@adobe.com>
- create the rpm spec for moses.
