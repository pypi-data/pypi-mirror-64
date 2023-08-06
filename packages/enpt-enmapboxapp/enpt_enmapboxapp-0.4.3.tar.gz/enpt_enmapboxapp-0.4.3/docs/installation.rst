.. highlight:: shell

============
Installation
============

Since enpt_enmapboxapp extends the functionality of the EnMAP-Box_, the installation of enpt_enmapboxapp requires
QGIS_ including the EnMAP-Box plugin. If QGIS_ or the EnMAP-Box_ is not yet installed on your system,
follow the installation instructions
`here <https://enmap-box.readthedocs.io/en/latest/usr_section/usr_installation.html>`__.

The enpt_enmapboxapp package is then installed into the QGIS_ Python environment.

.. code-block:: console

    git clone https://gitext.gfz-potsdam.de/EnMAP/GFZ_Tools_EnMAP_BOX/enpt_enmapboxapp.git
    cd enpt_enmapboxapp
    pip install .

.. note::

    On a Windows system, you have to activate the the QGIS environment first. To do so, run the OSGeo4W Shell (listed
    under OSGeo4W in the Start Menu) as administrator and enter ``call py3_env.bat``.

To make the enpt_enmapboxapp GUI run together with EnPT_ (backend), EnPT_ has to be installed into a separate Anaconda
environment. Please refer to the EnPT_ installation instructions
`here <http://enmap.gitext.gfz-potsdam.de/GFZ_Tools_EnMAP_BOX/EnPT/doc/installation.html>`__.

.. _EnPT: https://gitext.gfz-potsdam.de/EnMAP/GFZ_Tools_EnMAP_BOX/EnPT
.. _EnMAP-Box: http://www.enmap.org/enmapbox.html
.. _QGIS: https://www.qgis.org
