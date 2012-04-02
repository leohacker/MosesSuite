%define dist MosesSuite
%define version 1.0
%define release 1
%define release_date 20120224

Summary: 	Statistical Machine Translation System
Name: 		moses-core
Version: 	%{version}
Release: 	%{release}.%{dist}
Vendor: 	MosesSuite
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	LGPL
Group: 		NLP Tools
Source0: 	mosesdecoder-%{release_date}.tar.bz2
Source1:	scripts.tgz
Source2:	mteval-v11b.pl.tar.gz
#Patch0:		moses-scripts-makefile.patch
#Patch1:		mert-moses.pl.patch
Buildroot: 	%{_tmppath}/%{name}-root
BuildRequires: 	boost, boost-devel, xmlrpc-c, xmlrpc-c-devel, zlib, zlib-devel, gizapp, srilm
Requires: 	boost, xmlrpc-c, gizapp, srilm, zlib, perl-GD, perl-XML-Twig
URL:		https://github.com/leohacker/MosesSuite

%description 
Moses is a statistical machine translation system that allows you to 
automatically train translation models for any language pair. All you need is 
a collection of translated texts (parallel corpus). An efficient search 
algorithm finds quickly the highest probability translation among the 
exponential number of choices. 

Moses and moses scripts included.

%prep
%setup -q -T -b 1 -n scripts
%setup -q -T -b 2 -n bin

%setup -q -T -b 0 -n mosesdecoder
#%patch0 -p1
#%patch1 -p1

%build
#./regenerate-makefiles.sh --force
#./configure --with-boost --enable-threads --with-srilm=/tools/srilm --with-xmlrpc-c --prefix=/tools/moses
#make -j 2

%install
rm -rf %{buildroot}
cd %{_builddir}
mkdir -p $RPM_BUILD_ROOT/tools/
cp -a scripts $RPM_BUILD_ROOT/tools/
cp -a bin $RPM_BUILD_ROOT/tools/
cd mosesdecoder
./bjam -a -j4 --with-srilm=/tools/srilm --with-xmlrpc-c --with-giza=/tools/gizapp/bin --prefix=$RPM_BUILD_ROOT/tools/moses
# compile and install the moses-scripts
cd scripts 
mkdir -p $RPM_BUILD_ROOT/tools/moses/scripts
../bjam --with-giza=/tools/gizapp/bin --install-scripts=$RPM_BUILD_ROOT/tools/moses/scripts

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
/tools/bin/
/tools/scripts/
/tools/moses/bin/
#/tools/moses/include/
/tools/moses/lib/
/tools/moses/scripts/

%changelog
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
