%define version 1.0
%define release 2

Summary:        Moses Suite test cases of moses core, srilm training and irstlm trainning.
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
Requires:       moses-core, moses-suite-tools

%description
Pre-built sample models and several scripts for moses suite installation 
verification.

%prep
%setup -q -n %{name} -a 1

%build

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{moses_data_root}/translation_models

test_root=%{buildroot}/%{moses_data_root}/translation_models/test
install -m 755 -d ${test_root}
cp -a sample-models ${test_root}

install -m 755 -d ${test_root}/training-srilm/
install -m 755 -d ${test_root}/training-irstlm/
install -m 644 news-commentary08.fr-en.en ${test_root}/training-srilm/news-commentary08.fr-en.en
install -m 644 news-commentary08.fr-en.fr ${test_root}/training-srilm/news-commentary08.fr-en.fr
install -m 644 nc-dev2007.fr ${test_root}/training-srilm/nc-dev2007.fr
install -m 644 nc-dev2007.en ${test_root}/training-srilm/nc-dev2007.en
install -m 644 nc-test2007.fr ${test_root}/training-srilm/nc-test2007.fr
install -m 644 nc-test2007-src.fr.sgm ${test_root}/training-srilm/nc-test2007-src.fr.sgm
install -m 644 nc-test2007-ref.en.sgm ${test_root}/training-srilm/nc-test2007-ref.en.sgm

install -m 644 news-commentary-v7.fr-en.en ${test_root}/training-irstlm/news-commentary-v7.fr-en.en
install -m 644 news-commentary-v7.fr-en.fr ${test_root}/training-irstlm/news-commentary-v7.fr-en.fr

install -m 755 -d %{buildroot}/%{moses_suite_root}/bin
install -m 755 moses-suite-test-inst.sh %{buildroot}/%{moses_suite_root}/bin/moses-suite-test-inst.sh
install -m 755 moses-server-xmlrpc-test.py %{buildroot}/%{moses_suite_root}/bin/moses-server-xmlrpc-test.py

install -m 755 moses-suite-test-srilm.sh %{buildroot}/%{moses_suite_root}/bin/moses-suite-test-srilm.sh
install -m 755 moses-suite-test-irstlm.sh %{buildroot}/%{moses_suite_root}/bin/moses-suite-test-irstlm.sh


%clean
rm -rf %{buildroot}

%preun
rm -rf %{moses_data_root}/translation_models/test/sample-models/*

%files
%defattr(-,root,root)
%{moses_suite_root}/bin/moses-suite-test-inst.sh
%{moses_suite_root}/bin/moses-server-xmlrpc-test.py
%{moses_suite_root}/bin/moses-suite-test-srilm.sh
%{moses_suite_root}/bin/moses-suite-test-irstlm.sh

%defattr(-,moses,moses)
%{moses_data_root}/translation_models/test/

%changelog
* Wed May 09 2012 Leo Jiang - 1.0-2
- add srilm test.

* Tue May 01 2012 Leo Jiang - 1.0-2
- init spec.
