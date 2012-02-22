How to build 
------------
Before build the moses suite packages for CentOS6.0 64bit system, please install the necessary development tools, library and header files. 

$ yum groupinstall "Development tools" "Additional Development"

And install the prerequisite package prompted when building failed.

Gerenal Instruction
-------------------
0. download the official source tarball and put it into SOURCES folder under rpmbuild tree.
1. put the patch files into SOURCES folder under rpmbuild tree.
2. put the spec file into SPECS folder.
3. issue the command "rpmbuild -ba package-name.spec" for building binary packages.

Notes: Because of the storage limitaion for free account in github.com, I can't put the tarball for upstream software in this project. Please help to verify whether these patch files can be applied to newer source code and improve the spec files. THANKS!

GIZAPP
------
URL: http://code.google.com/p/giza-pp/
Version: stable (?)
SOURCE: gizapp.tgz
This version is released on Sep 24 2011, and no version number was specified. I guess this should be a stable version, give it verion 1.0.6 in spec file.

Patch0: giza-pp.patch 
Since there is no static library libm in CentOS6 64bit, we have to remove the link flag -static for successful compilation. For CentOS6 32bit, you can use the -static flag.

SRILM
-----
URL: http://www.speech.sri.com/projects/srilm/
Verison: 1.6.0
SOURCE: srilm-1.6.0.tar.gz

Patch0: srilm-m64-NoTCL-RemoveUserLocal.patch
Some trival patchs for 64bit system, and make it installed to /usr/ instead of /usr/local.

IRSTLM
------
URL: http://hlt.fbk.eu/en/irstlm
Version: 5.70.04
SOURCE: irstlm-5.70.04.tgz

Patch0: irstlm-script-makefile.am.patch
Make the scripts can be copied into DEST directory.
