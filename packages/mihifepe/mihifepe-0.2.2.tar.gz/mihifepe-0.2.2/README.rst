========
mihifepe
========

.. image:: https://img.shields.io/pypi/v/mihifepe.svg
        :target: https://pypi.python.org/pypi/mihifepe
        :alt: Release status

.. image:: https://img.shields.io/travis/Craven-Biostat-Lab/mihifepe.svg
        :target: https://travis-ci.org/Craven-Biostat-Lab/mihifepe
        :alt: Build status

.. image:: https://readthedocs.org/projects/mihifepe/badge/?version=latest
        :target: https://mihifepe.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Craven-Biostat-Lab/mihifepe/shield.svg
        :target: https://pyup.io/repos/github/Craven-Biostat-Lab/mihifepe/
        :alt: Updates


--------
Overview
--------

``mihifepe``, or **M**\ odel **I**\ nterpretability via **Hi**\ erarchical **Fe**\ ature **Pe**\ rturbation, is a library implementing a model-agnostic method that, given a learned model and a hierarchy over features, (i) tests feature groups, in addition to base features, and tries to determine the level of resolution at which important features can be determined, (ii) uses hypothesis testing to rigorously assess the effect of each feature on the model's loss, (iii) employs a hierarchical approach to control the false discovery rate when testing feature groups and individual base features for importance, and (iv) uses hypothesis testing to identify important interactions among features and feature groups. ``mihifepe`` is based on the following paper:

Lee, Kyubin, Akshay Sood, and Mark Craven. 2019. “Understanding Learned Models by Identifying Important Features at the Right Resolution.” In Proceedings of the AAAI Conference on Artificial Intelligence, 33:4155–63. https://doi.org/10.1609/aaai.v33i01.33014155.

-------------
Documentation
-------------

https://mihifepe.readthedocs.io

------------
Installation
------------

Recommended installation method is via `virtual environments`_ and pip_.
In addition, you also need graphviz_ installed on your system.

When making the virtual environment, specify python3 as the python executable (python3 version must be 3.5+)::

    mkvirtualenv -p python3 mihifepe_env

To install the latest stable release::

    pip install mihifepe

Or to install the latest development version from GitHub::

    pip install git+https://github.com/Craven-Biostat-Lab/mihifepe.git@master#egg=mihifepe

On Ubuntu, graphviz may be installed by::

    sudo apt-get install graphviz

.. _pip: https://pip.pypa.io/
.. _virtual environments: https://python-guide-cn.readthedocs.io/en/latest/dev/virtualenvs.html
.. _graphviz: https://www.graphviz.org/

-----------
Development
-----------

https://mihifepe.readthedocs.io/en/latest/contributing.html

-----
Usage
-----

https://mihifepe.readthedocs.io/en/latest/usage.html

-------
License
-------

``mihifepe`` is free, open source software, released under the MIT license. See LICENSE_ for details.

.. _LICENSE: https://github.com/Craven-Biostat-Lab/mihifepe/blob/master/LICENSE

-------
Contact
-------

`Akshay Sood`_

.. _Akshay Sood: https://github.com/cloudbopper
