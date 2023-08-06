# ML4
-----

Introduction
------------

ML4是TechYoung课程辅助工具包.

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

    sudo pip3 install ml4

--------------

Usage
-----

methods:
~~~~~~~~

ml4.getWindowData(data, x, y, windowSize=300, steps=300):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***x:*** x-axis column name , 例如 "ctime"

-  ***y:*** column name, 例如 "hr"

-  ***window:*** window size (s)

-  ***steps:*** window steps (s)

Note
----
