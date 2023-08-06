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

plot.histplot(data, column\_name, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_name:*** column name of dataframe, 例如 "hr\_mean"

-  ***kwargs:*** "xmin", "xmax"

plot.gmmplot(data, column\_names, k\_range, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of dataframe, 例如
   ["hr\_mean", "hr\_std"]

-  ***k\_range:*** the range of components (k), 例如 [2, 11] or (2, 11)

-  ***kwargs:*** "xmin", "xmax"

plot.kmeansplot(data, column\_names, k\_range, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of dataframe, 例如
   ["hr\_mean", "hr\_std"]

-  ***k\_range:*** the range of clusters (k), 例如 [2, 11] or (2, 11)

-  ***kwargs:*** "xmin", "xmax"

plot.metricplot(n\_clusters\_range, scores, scores2=[], \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***n\_clusters\_range：*** tuple or list of range，例如 (2, 10)

-  ***scores:*** list of score

-  ***scores:*** list of score2 (option)

-  ***kwargs:*** "x\_label", "y\_label"

plot.errorbarplot(data, x, y=[], y2=[], \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***x:*** x-axis column name，例如 "ctime"

-  ***y:*** y column name，例如 ["hr\_mean", "hr\_std"]

-  ***y2:*** y2 column name，例如 ["br\_mean", "br\_std"] (option)

-  ***kwargs:*** "X\_LABEL", "Y\_LABEL", "TITLE", "LIMIT"

plot.pcaplot(data, column\_names, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of dataframe, 例如
   ["hr\_mean", "hr\_std"]

-  ***kwargs:*** "n\_components"

plot.tsenplot(data, column\_names, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of dataframe, 例如
   ["hr\_mean", "hr\_std"]

-  ***kwargs:*** "n\_components"

seaborn.boxplot(x, y, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

此函数需要ml4进行对原始数据进行窗口化分类

-  ***x:*** the UNIX timestamp list from ml4

-  ***y:*** the data list from ml4

-  ***kwargs:*** "X\_LABEL", "Y\_LABEL", "TITLE"

seaborn.violinplot(x, y, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

此函数需要ml4进行对原始数据进行窗口化分类

-  ***x:*** the UNIX timestamp list from ml4

-  ***y:*** the data list from ml4

-  ***kwargs:*** "X\_LABEL", "Y\_LABEL", "TITLE"

Note
----

版本里的1.2.4是旧的版本。1.2.5和以后的版本是用于函数计算的版本。
1.2.5以及以后版本将去掉wcc自动框架.
目录下的子目录：libwebp-0.4.1-linux-x86-64
需要从网上下载，然后把里面的bin下的gif2webp放到/usr/bin里。这样就可以在wcc里调用了.
