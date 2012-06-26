%define release 1
%define version 12.05.22

Name: 		stanford-segmenter
Summary: 	Stanford Word Segmenter
Version: 	%{version}
Release: 	%{release}%{dist}
Vendor: 	MosesSuite Project
Packager:	Leo Jiang <leo.jiang.dev@gmail.com>
License: 	GPL v2
Group: 		Moses Suite
Source: 	%{name}-2012-05-22.tar.gz
Buildroot: 	%{_tmppath}/%{name}-root
URL:		http://nlp.stanford.edu/software/segmenter.shtml

%description
Tokenization of raw text is a standard pre-processing step for many NLP tasks. 
For English, tokenization usually involves punctuation splitting and separation 
of some affixes like possessives. Other languages require more extensive token 
pre-processing, which is usually called segmentation.

The Stanford Word Segmenter currently supports Arabic and Chinese. The provided 
segmentation schemes have been found to work well for a variety of applications. 

%prep
%setup -q -n %{name}-2012-05-22

%build

%install
rm -rf %{buildroot}
%define destdir %{buildroot}/%{moses_suite_root}
sed -i -e 's/mx2g/mx1g/' segment.sh
install -m 755 -d %{destdir}/stanford-segmenter
cp -a * %{destdir}/stanford-segmenter/

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
%defattr(-,root,root)
%{moses_suite_root}/stanford-segmenter/

%changelog
* Tue Jun 26 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
