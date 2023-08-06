*****************
upgrade_ensurepip
*****************

.. image:: https://sourceforge.net/p/upgrade-ensurepip/code/ci/default/tree/_doc/_static/license.svg?format=raw
   :target: https://opensource.org/licenses/MIT

.. image:: https://sourceforge.net/p/upgrade-ensurepip/code/ci/default/tree/_doc/_static/pypi.svg?format=raw
   :target: https://pypi.org/project/upgrade_ensurepip/

.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw
   :target: https://bitbucket.org/ruamel/oitnb/

.. image:: https://sourceforge.net/p/ryd/code/ci/default/tree/_doc/_static/ryd.svg?format=raw
   :target: https://pypi.org/project/ryd/

Once you find that::

  /your/installed/version/bin/python3 -m venv /some/venv

followed by::

   /some/venv/bin/pip install some_package

gives a message that there is an update for ``pip``, this package can
update the wheel files used by ``ensurepip`` (``pip``, ``setuptools``) to the latest versions
available on pypi, and get rid of this message (at least to the next upgrade).

You can do this upgrade by running::

  /your/installed/version/bin/python3 -m upgrade_ensurepip

In order to be able to use the above command, you either have to install the
package using something like::

  /your/installed/version/bin/pip install --disable-pip-version-check upgrade_ensurepip

or alternatively you can to make sure the file ``upgrade_ensurepip.py`` from that package is in
your current directory.

Without options ``upgrade_ensurepip`` checks the JSON information on the
pacakage, downloads the wheel (to memory) if there is a newer version and does a
check against the sha256 is made before saving the newly downloaded wheels to
disc.

If started With the option ``--pip``, the ``pip`` "living" in the same directory
as the Python executable is used to first search for the package to get the
latest version number, then ``pip`` is used to download the wheel for that
version. This is somewhat slower, but as ``pip`` should follow any instructions
in your ``~/.config/pip/pip.conf``, including upgrading from local repositories.

After finding and downloading newer versions, using one of the above methods, the
``/your/installed/version/lib/pythonX.Y/ensurepip/__init__.py`` file is updated
as it hard-codes the versions of the wheels used. Before changing, a backup of
the original is made if such a backup does not yet exist.

As old wheels are preserved, only backup file ``__init__.py.org`` located under
``/your/installed/version/lib/pythonX.Y/ensurepip/``
needs to be copied back in case you encounter any problems.
