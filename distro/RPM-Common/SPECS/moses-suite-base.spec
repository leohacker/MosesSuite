%define release 5
%define version 1.0

Name: 		moses-suite-base
Summary: 	Moses Suite base package
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
Setup a directory hierarchy for moses suite tools(giza++, language models,
moses core, and other scripts, etc), corpus and translation_models. Set these 
root directories as system wide environments to allow scripts to locate any 
data or programs.

%prep
%setup -q -n %{name}

%build
# setup the root directories as rpm macros defined.
sed -i -e "s|MOSES_DATA_ROOT=$|MOSES_DATA_ROOT=%{moses_data_root}|" moses-suite.conf
sed -i -e "s|MOSES_SUITE_ROOT=$|MOSES_SUITE_ROOT=%{moses_suite_root}|" moses-suite.conf


%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/etc
install -m 644 moses-suite.conf %{buildroot}/etc/moses-suite.conf
install -m 755 -d %{buildroot}/%{moses_data_root}
install -m 755 -d %{buildroot}/%{moses_data_root}/corpus
install -m 755 -d %{buildroot}/%{moses_data_root}/translation_models
install -m 755 -d %{buildroot}/%{moses_suite_root}
install -m 755 -d %{buildroot}/%{moses_suite_root}/bin

%clean
rm -rf %{buildroot}

%pre
# create user moses:moses for moses suite.
if ! grep "moses" /etc/passwd > /dev/null; then
    useradd moses > /dev/null
    echo "User moses added, DON'T forget to setup password."
fi

if ! grep "moses/bin" /home/moses/.bash_profile > /dev/null; then
    echo "" >> /home/moses/.bash_profile
    echo "# Setup env variable PATH for moses suite." >> /home/moses/.bash_profile
    echo 'export PATH=%{moses_suite_root}/bin:%{moses_suite_root}/moses/bin:$PATH' >> /home/moses/.bash_profile
    echo "Add moses suite path into user bash profile."
fi

%post

%preun

%postun

%files
%defattr(-,root,root)
/etc/moses-suite.conf
%{moses_suite_root}

%defattr(-,moses,moses)
%{moses_data_root}/

%changelog
* Tue May 08 2012 Leo Jiang - 1.0-5
- set the path of moses suite into moses-suite.conf .

* Mon May 07 2012 Leo Jiang - 1.0-4
- change the directory name.

* Fri May 04 2012 Leo Jiang - 1.0-3
- add the env IRSTLM into user moses's bash_profile.

* Tue May 02 2012 Leo Jiang - 1.0-2
- add user moses if not exists, set the permission of data folder for user moses.

* Tue May 02 2012 Leo Jiang <leo.jiang.dev@gmail.com>
- create the rpm spec.
