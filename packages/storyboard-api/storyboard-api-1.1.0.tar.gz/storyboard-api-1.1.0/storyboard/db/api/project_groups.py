# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy.orm import subqueryload
from wsme.exc import ClientSideError

from storyboard._i18n import _
from storyboard.common import exception as exc
from storyboard.db.api import base as api_base
from storyboard.db.api import projects
from storyboard.db import models


def _entity_get_query(session=None):
    if not session:
        session = api_base.get_session()
    query = session.query(models.ProjectGroup)\
        .options(subqueryload(models.ProjectGroup.projects))

    return query


def _entity_get(id, session=None):
    query = _entity_get_query(session).filter_by(id=id)
    return query.first()


def project_group_get(project_group_id):
    return _entity_get(project_group_id)


def project_group_get_by_name(name):
    query = _entity_get_query().filter_by(name=name)
    return query.first()


def project_group_get_all(marker=None, limit=None, offset=None,
                          subscriber_id=None, sort_field=None, sort_dir=None,
                          **kwargs):
    # Sanity checks, in case someone accidentally explicitly passes in 'None'
    if not sort_field:
        sort_field = 'id'
    if not sort_dir:
        sort_dir = 'asc'

    query = api_base.model_query(models.ProjectGroup)
    query = api_base.apply_query_filters(query=query,
                                         model=models.ProjectGroup,
                                         **kwargs)

    # Filter by subscriber ID
    if subscriber_id is not None:
        subs = api_base.model_query(models.Subscription)
        subs = api_base.apply_query_filters(query=subs,
                                            model=models.Subscription,
                                            target_type='project_group',
                                            user_id=subscriber_id)
        subs = subs.subquery()
        query = query.join(subs, subs.c.target_id == models.ProjectGroup.id)

    query = api_base.paginate_query(query=query,
                                    model=models.ProjectGroup,
                                    limit=limit,
                                    sort_key=sort_field,
                                    marker=marker,
                                    offset=offset,
                                    sort_dir=sort_dir)

    # Execute the query
    return query.all()


def project_group_get_count(subscriber_id=None, **kwargs):
    # Construct the query
    query = api_base.model_query(models.ProjectGroup)
    query = api_base.apply_query_filters(query=query,
                                         model=models.ProjectGroup,
                                         **kwargs)

    # Filter by subscriber ID
    if subscriber_id is not None:
        subs = api_base.model_query(models.Subscription)
        subs = api_base.apply_query_filters(query=subs,
                                            model=models.Subscription,
                                            target_type='project_group',
                                            user_id=subscriber_id)
        subs = subs.subquery()
        query = query.join(subs, subs.c.target_id == models.ProjectGroup.id)

    return query.count()


def project_group_create(values):
    return api_base.entity_create(models.ProjectGroup, values)


def project_group_update(project_group_id, values):
    return api_base.entity_update(models.ProjectGroup, project_group_id,
                                  values)


def project_group_add_project(project_group_id, project_id):
    session = api_base.get_session()

    with session.begin(subtransactions=True):
        project_group = _entity_get(project_group_id, session)
        if project_group is None:
            raise exc.NotFound(_("%(name)s %(id)s not found")
                               % {'name': "Project Group",
                                  'id': project_group_id})

        project = projects.project_get(project_id)
        if project is None:
            raise exc.NotFound(_("%(name)s %(id)s not found")
                               % {'name': "Project", 'id': project_id})

        if project_id in [p.id for p in project_group.projects]:
            raise ClientSideError(_("The Project %(id)d is already in "
                                  "Project Group %(group_id)d") %
                                  {'id': project_id,
                                   'group_id': project_group_id})

        project_group.projects.append(project)
        session.add(project_group)

    return project_group


def project_group_delete_project(project_group_id, project_id):
    session = api_base.get_session()

    with session.begin(subtransactions=True):
        project_group = _entity_get(project_group_id, session)
        if project_group is None:
            raise exc.NotFound(_("%(name)s %(id)s not found")
                               % {'name': "Project Group",
                                  'id': project_group_id})

        project = projects.project_get(project_id)
        if project is None:
            raise exc.NotFound(_("%(name)s %(id)s not found")
                               % {'name': "Project",
                                  'id': project_id})

        if project_id not in [p.id for p in project_group.projects]:
            raise ClientSideError(_("The Project %(id)d is not in "
                                  "Project Group %(group_id)d") %
                                  {'id': project_id,
                                   'group_id': project_group_id})

        project_entry = [p for p in project_group.projects
                         if p.id == project_id][0]
        project_group.projects.remove(project_entry)
        session.add(project_group)

    return project_group


def project_group_delete(project_group_id):
    project_group = project_group_get(project_group_id)

    if not project_group:
        raise exc.NotFound(_('Project group not found.'))

    api_base.entity_hard_delete(models.ProjectGroup, project_group_id)
