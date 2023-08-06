=========================================
 Things that StoryBoard does differently
=========================================

StoryBoard has been custom-designed to support collaboration within an `open
community <https://governance.openstack.org/tc/reference/opens.html>`_
with the following characteristics:

- The community manages a large number of projects, and some
  initiatives will span multiple projects.

- There are a variety of sponsors; no single organisation or person is
  in control of the community's direction.

- Everyone is equally empowered to contribute.

- There are many stakeholders, who need to track diverse sets of
  requirements for each project.

- Even when requirements overlap, priorities can differ widely.

Consequently StoryBoard has several features built specifically around
these needs.

If you've been using Launchpad on your project, by now you're probably
aware of its norms and idiosyncracies. It can be hard to envisage
different ways of doing the same tasks when thinking in terms of
things that are possible in Launchpad, so this document aims to give
an overview of some of the interesting new features in StoryBoard that
don't have a Launchpad equivalent.


Moving beyond universal priorities
==================================

In StoryBoard, it's possible for different people to say 'this is a
priority for us', so that a task can have different priorities,
tailored to different audiences.

So, why is this useful?

Traditional bug / task trackers have often modelled the concept of
priority as a single, shared attribute field.  For example, anyone
could change a task's priority, and this would be seen by everyone
viewing the task.  Typically there has been no way to say 'you can
only change this priority if you have discussed this on IRC and it has
been agreed among the project team', etc.  This has meant that people
with no context could alter global priority of tasks.  Also, two
different groups might prioritize tasks differently, and this could
result in long prioritization sessions, where the real question was
'whose priorities matter most?' (and often the answer was 'it depends
on who the audience is', so these arguments would result in a
stalemate).

So, StoryBoard provides a way to say 'this task matters to *me*' or
'this task matters to *my team*', without trying to force that point
of view on everyone else.  We use worklists to express priority: if
you manually add tasks to a worklist, you can drag and drop them in
order of priority.  This has the side effect that you can see how
prioritizing one task affects the priority of other tasks; you can
only have one item at the top, and putting anything high on the list
will push other things down.  It is possible for others to subscribe
to the worklists of those individuals or teams whose priorities they
care about; then, whenever they browse to a prioritised story, they
will see if any of the tasks are on those lists, and what position the
tasks are on the list.

Worklists have permissions, so it is possible to set up a project team
list on which items can only be moved by contributors selected by core
reviewers, etc. This stops everyone changing the priority of tasks
without discussion.

This is still relatively new, and we're excited to see how people use
it. We've lost some ease in assigning priority in favour of finer
grained representation of priority. In the past, StoryBoard did show
lots of different people's priorities, it just didn't offer any way of
tracking whose priorities were whose. So this makes things more open
and explicit. We hope to tailor the implementation based on user
feedback, and these are the first steps! :)


Worklists and Boards
====================

StoryBoard introduces some new data models to meet the complex needs
of OpenStack.

Worklists are arbitrary groupings of stories and/or tasks with
whatever title the user wants. Each 'item' (story or task) is placed
on a 'card' on the worklist. Here is an example:

.. image:: _assets/example-worklist.png

A worklist can be handy as a personal todo list. Anyone can make a
worklist, and the creator can decide who (if anyone) else can view and
edit it. It is possible to either populate a worklist manually, or
automatically populate it with stories or tasks that fulfil some
criteria (eg: 'assigned to Alice'. Here are some example filter
criterai for an automatic worklist:

.. image:: _assets/example-automatic-worklist-filters.png

For more information about how to create and edit worklists, see
:doc:`this documentation<worklists>`.

We also have boards, which are akin to collections of
worklists. Here's an example:

.. image:: _assets/example-board.png

You can name 'lanes' (lists) in the board what you want, and either
populate them as a visualisation of some data by making them
'automatic' (like worklists, populate them with stories or tasks that
meet some criteria), or manually move cards to and from non-automatic
lanes. This means you can use boards to visualise data, or you can use
them for a workflow like kanban if that's your thing. So, for example,
you might group various stories in different lanes according to
criteria, and then the board would function as an 'epic', tracking the
status of multiple stories. You can give a board a markdown
description if you want to provide more detail on the background. You
can even take a hybrid approach where you write custom scripts to move
cards around based on certain conditions.

Permissions for boards work the same way as worklist permissions. A
public board or worklist is visible to all, and editable for users and
owners. A private board or worklist is only visible to its users and
owners. Users can move and delete cards, but only owners can delete
lanes or change the metadata of the board itself (eg: its title or
description).

For documentation on how to create boards, add users/owners, etc
:doc:`that can be located here<boards>`.


The REST API
============

StoryBoard has been developed with an API-first approach. What does
this mean? Well, at its core, StoryBoard has a python API. This then
plugs into a database, and can get information from it (or transmit
information to it). The StoryBoard API can then be accessed from
various clients, so that users can interact with some given database.

This means StoryBoard's features are first built on the API side, and
are then expressed in various clients. You can do more in the API than
in any given UI, since the UI just expresses the API.

Why does that matter?

Custom scripts! Custom UIs! If you can express it in a script, you can
fetch the data from StoryBoard. You don't have to rely on features in
any current UI if you have a niche request, and it's possible to build
your own new UI (or dashboard) if you want. You can also get info from
the commandline on the fly with a tool like curl.

There are some docs to illustrate usage here:

https://docs.openstack.org/infra/storyboard/webapi/v1.html

Moreover, as the API is generally RESTful, it's straightforward to
guess how to do things, and compatible with a lot of other tools with
minimal tinkering. Here are some sample, heavily commented scripts for
one simple example (commandline) interface, a python client:

https://review.openstack.org/#/c/371620/

There is also a much more fully-featured and interactive commandline
StoryBoard interface named `boartty
<https://opendev.org/ttygroup/boartty/>`_ written by Jim Blair:

.. image:: _assets/boartty-3.png

The long and short of it is, if you know how to display data from a
REST API, you can display data from a StoryBoard instance.

You can do some fun things with this. For example, you could use
pygame if you wanted to depict stories as moving platforms or
something.  On that note, if you feel like hacking something up, the
Storyboard team would love to hear from you!  Come and say hello on
the ``#storyboard`` channel on Freenode IRC.
