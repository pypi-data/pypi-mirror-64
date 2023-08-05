*****************
upgrade_ensurepip
*****************

.. image:: https://sourceforge.net/p/upgrade-ensurepip/code/ci/default/tree/_doc/_static/license.svg?format=raw
   :target: https://opensource.org/licenses/MIT

.. image:: https://sourceforge.net/p/upgrade-ensurepip/code/ci/default/tree/_doc/_static/pypi.svg?format=raw
   :target: https://pypi.org/project/upgrade_ensurepip/

.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw
   :target: https://bitbucket.org/ruamel/oitnb/

.. image:: https://bitbucket.org/ruamel/ryd/raw/default/_doc/_static/ryd.svg
   :target: https://pypi.org/project/ryd/

Once you find that ``/your/installed/version/bin/python3 -m venv
/some/venv`` followed by ``/some/venv/bin/pip install some_package``
gives a message that there is an update for ``pip``, this package can
update the wheel files used by ``ensurepip`` to the latest versions
available on pypi.

You can do this upgrade by running::

  /your/installed/version/bin/python3 -m upgrade_ensurepip

A heck against the sha256 is made before saving the newly downloaded
wheels to disc. After finding and downloading newer versiosn, the
``/your/installed/version/lib/pythonX.Y/ensurepip/__init__.py`` file
is updated as it hard-codes the versions of the wheels used. Before
changing, a backup of the original is made if such a backup does not
yet exists.

Old wheels are preserved, so only backup file ``__init__.py.org`` located under
``/your/installed/version/lib/pythonX.Y/ensurepip/``
needs to be copied back in case you encounter problems.
