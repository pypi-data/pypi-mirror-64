# ML3
-----

Introduction
------------

ML3是TechYoung课程辅助工具包.

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

    sudo pip3 install ml3

--------------

Usage
-----

After installation, run the following command:

::

    import ml3

Methods:
~~~~~~~~

histplot(data, column\_name, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_name:*** column name of dataframe, 例如 "hr\_mean"

-  ***kwargs:*** "xmin", "xmax"

gmmplot(data, feature\_name, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***feature\_name:*** column name of dataframe, 例如 "hr\_mean"

-  ***kwargs:*** "xmin", "xmax", "n\_components"

kmeansplot(data, feature\_name, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***feature\_name:*** column name of dataframe, 例如 "hr\_mean"

-  ***kwargs:*** "xmin", "xmax", "n\_clusters"

metrics(scores, n\_clusters\_range, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***scores:*** list of score

-  ***n\_clusters\_range：*** tuple or list of range，例如 (2, 10)

-  ***kwargs:*** "x\_label", "y\_label", "n\_clusters"

errorbarplot(data, x, feature\_name, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***x:*** x-axis value

-  ***feature\_name:*** column name of dataframe, 例如 ["hr\_mean",
   "hr\_std"] or [["hr\_mean", "hr\_std"], ["br\_mean", "br\_std"]]

-  ***kwargs:*** "x\_label", "y\_label", "title"

Note
----

版本里的1.2.4是旧的版本。1.2.5和以后的版本是用于函数计算的版本。
1.2.5以及以后版本将去掉wcc自动框架.
目录下的子目录：libwebp-0.4.1-linux-x86-64
需要从网上下载，然后把里面的bin下的gif2webp放到/usr/bin里。这样就可以在wcc里调用了.
