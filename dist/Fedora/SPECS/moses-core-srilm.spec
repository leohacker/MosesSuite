%define dist    fc16
%define version 1.0
%define release 5
%define release_date 20120224
%define tag     moses

Summary: 	Statistical Machine Translation System with SRILM support
Name: 		moses-core-srilm
Version: 	%{version}
Release: 	%{release}.%{tag}.%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	LGPL
Group: 		Moses Suite
Source0: 	mosesdecoder-%{release_date}.tar.bz2
#Source2:	mteval-v11b.pl.tar.gz
Buildroot: 	%{_tmppath}/%{name}-root
BuildRequires: 	ccache, glibc-devel, glibc-headers, libstdc++-devel 
BuildRequires: 	boost-devel, xmlrpc-c-devel, zlib-devel 
BuildRequires: 	gizapp, srilm 
Requires: 	boost, xmlrpc-c, gizapp, srilm, zlib, perl-CGI, perl-GD, perl-XML-Twig, perl-Switch
URL:		https://github.com/leohacker/MosesSuite

%description 
Moses is a statistical machine translation system that allows you to 
automatically train translation models for any language pair. All you need is 
a collection of translated texts (parallel corpus). An efficient search 
algorithm finds quickly the highest probability translation among the 
exponential number of choices. 

Moses and moses scripts included.

This version of Mosos Core package is compiled with SRILM support.

%prep
#%setup -q -T -b 2 -n bin

%setup -q -T -b 0 -n mosesdecoder

%build

%install
rm -rf %{buildroot}
cd %{_builddir}
mkdir -p $RPM_BUILD_ROOT/tools/
cd mosesdecoder
./bjam -a --notrace -j4 --with-srilm=/tools/srilm --with-xmlrpc-c --with-giza=/tools/gizapp/bin --prefix=$RPM_BUILD_ROOT/tools/moses --includedir=$RPM_BUILD_ROOT/tools/moses/include --install-scripts=$RPM_BUILD_ROOT/tools/moses/scripts

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
/tools/moses/

%changelog
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
