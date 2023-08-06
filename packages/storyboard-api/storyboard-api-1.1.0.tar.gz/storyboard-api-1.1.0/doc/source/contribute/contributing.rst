.. include:: ../../../CONTRIBUTING.rst

.. NOTE(dhellmann): The title underline style just below relies on the
   existing format of the file included just above.

Got an Issue with StoryBoard?
------------------------------

If you are hitting an error, there's some new feature that you think would
make StoryBoard even more amazing, or just something that could be a
little different, please make a story for it! We won't know if you don't tell
us.

After you've created the story (title, description, set the default task to be
associated with the opendev/storyboard project, etc), you are welcome to
add tags. We have a defined set of tags we use as a project listed
below:

* blocking-storyboard-migration: These stories have been called out as blocking
  the migration of an OpenStack project from migrating to StoryBoard from
  Launchpad.
* its-storyboard: These stories are related to the `gerrit plugin "its-storyboard"
  <https://gerrit.googlesource.com/plugins/its-storyboard/>`_ that pulls
  information from gerrit for StoryBoard to use, i.e. updating task status, linking
  gerrit patches to stories, etc.
* storyboard-email: These stories relate to the email notification functionality and
  account settings.
* storyboard-feature-request: Stories with this tag involve implementing some new
  feature, probably involving both api and webclient updates.
* storyboard-notifications: Stories with this tag relate to work that needs to be
  done with the notification mechanism StoryBoard has.
* storyboard-releases: This tag denotes that the story relates to the release of
  storyboard on pypi since we have started doing releases.
* storyboard-searching-enhancements: Stories with this tag relate to work that
  needs to be done with the searching capabilities in StoryBoard. It could mean
  work on the jump-to search or to the advanced search that StoryBoard has.
* storyboard-testing: This tag is applied to stories that are focused on StoryBoard's
  testing suite- functional, integration, etc.
* storyboard-worklists: Stories with this tag relate to work that needs to be done
  on StoryBoard's worklist feature.

You'll notice we have no storyboard-bug, this is because anything that doesn't
generally fit into one of these other categories is likely a bug and we didn't
see a need to tag EVERYTHING.

We also use a few other tags that are more widely applicable to projects other
than StoryBoard that may be using StoryBoard. Below they are listed and defined
with regards to how we use them:

* low-hanging-fruit: Stories with this tag on them are good places to get started
  for newcomers, they are smaller bugs or new features that don't require a lot of
  design or discussion.
* dependency-upgrades: Stories with this tag discuss dependencies that are being
  utilized by StoryBoard (like libraries) that need to be upgraded.
* outreachy: Stories with this tag are being worked or will be worked by interns of
  the `outreachy program <https://www.outreachy.org/>`_.

Its also important to note, that more than one tag can be applied to
a story if more than one is relevant. 

Running the Tests
-----------------

Storyboard uses tox_ to manage its unit and functional tests. After
installing tox and downloading the storyboard source the next step is
to install system dependencies. Run::

  $ tox -e bindep

Then take the listed packages and install them with your system package
manager. For example::

  $ sudo apt-get install package list here

To run the tests quickly on your local development machine you can run
the tests with the sqlite backend::

  $ tox -e sqlite

And to run the style-checker and static analysis tool::

  $ tox -e pep8

If you would like to run the test suite with proper database backends or
with python2 instead of python3 there is one more step to follow. Note
that the testsuite takes quite a bit longer to run when using the MySQL
and PostgreSQL database backends.

First ensure MySQL and PostgreSQL are running (you may need to start
these services). Then run the test-setup.sh helper script::

  $ tools/test-setup.sh

This script needs to be run with a user that has sudo access. It will
configure the databases as needed to run the unittests. You can then
runt the unittests with::

  $ tox -e py27

or for Python 3::

  $ tox -e py35

On slower systems, the database migrations may take longer than the
default timeout of 120 seconds. To override the timeout, set the
``OS_TEST_TIMEOUT`` environment variable. For example, to set the
timeout to 3 minutes, run::

  $ OS_TEST_TIMEOUT=180 tox -e py27

For More Extensive Testing...
-------------------------------

To set up your own local storyboard to see how your changes look in the webclient, see
the :ref:`development`.


.. _tox: https://tox.readthedocs.io/en/latest/


