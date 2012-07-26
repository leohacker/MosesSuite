# Moses Suite
Author: [Leo Jiang](leo.jiang.dev@gmail.com) Blog: http://leohacker.wordpress.com/.

* Introduction

Moses Suite is developed for supporting OpenSource Machine Translation framework 
Moses SMT. Currently Moses Suite has several parts: 
* Moses suite base system
* SMT Corpus Tools
* Moses suite training tools

Moses suite base system integrate upstream software (Moses and Language models)
to build a base system of moses for training and decoding. Other tools aim to 
provide better solution for corpus processing, training and other works in
more user friendly, flexible and customiziable way. If possible, improving user
experience is on the list of objectives.

Since the storage limitation of github, I put the source code from upstream at 
http://code.google.com/p/moses-suite/.

If you find this project very interesting, don't hesitate to join me :D

* Licence
Moses Suite is distributed under BSD 2-Clause License (a.k.a. FreeBSD License).

BSD 2-Clause License

Copyright (c) 2012, Leo Jiang
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

Generally, most of source code is written from scratch for Moses Suite, apparently 
is under BSD 2-Clause License. Some upstream sources code will be included in this
repository also just after we need to modify something. Please notify me via email
(leo.jiang.dev@gmail.com) if the source code can't be modified and redistributed 
since I misunderstand your license. I will remove them from repository as soon as 
I can. Otherwise, I will put them under your original license or the project's 
license (BSD 2-Clause License) if original one is a permissive open source license. 
You can find their own license files in root directory of subproject.
