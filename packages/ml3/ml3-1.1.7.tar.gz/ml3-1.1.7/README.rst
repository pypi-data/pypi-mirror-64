# ML7
-----

Introduction
------------

ML7是TechYoung课程辅助工具包.

+-------------------------------+
| ## Distribution               |
+-------------------------------+
| Run the following commands to |
| register, build and upload    |
| the package to PYPI.          |
+-------------------------------+
| python3 setup.py sdist upload |
+-------------------------------+
| The home page on PYPI is:     |
| https://pypi.org/project/wcc/ |
+-------------------------------+

Install
-------

::

    sudo pip3 install wcc

--------------

Usage
-----

After installation, run the following command:

::

    from wcc import Wcc

Note
----

版本里的1.2.4是旧的版本。1.2.5和以后的版本是用于函数计算的版本。
1.2.5以及以后版本将去掉wcc自动框架.
目录下的子目录：libwebp-0.4.1-linux-x86-64
需要从网上下载，然后把里面的bin下的gif2webp放到/usr/bin里。这样就可以在wcc里调用了.
