# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_config import cfg
from pecan import abort
from pecan.decorators import expose
from pecan import response
from pecan import rest
from pecan.secure import secure
from six.moves.urllib.parse import unquote

import wsme.types as wtypes
import wsmeext.pecan as wsme_pecan

from storyboard._i18n import _
import storyboard.api.auth.authorization_checks as checks
from storyboard.api.v1 import validations
from storyboard.api.v1 import wmodels
from storyboard.common import decorators
import storyboard.common.exception as exc
from storyboard.db.api import project_groups
from storyboard.db.api import projects


CONF = cfg.CONF


def _is_int(s):
    # 20 is the number of digits in a 64-bit integer, which is realistically
    # way more than the number of Project Groups likely to be created.
    return len(s) < 20 and s.isdigit()


class ProjectsSubcontroller(rest.RestController):
    """This controller should be used to list, add or remove projects from a
    Project Group.
    """

    @decorators.db_exceptions
    @secure(checks.guest)
    @wsme_pecan.wsexpose([wmodels.Project], wtypes.text)
    def get(self, project_group_id):
        """Get projects inside a project group.

        Example::

          curl https://my.example.org/api/v1/project_groups/55/projects

        :param project_group_id: An ID or name of the project group.
        """

        if _is_int(project_group_id):
            group = project_groups.project_group_get(int(project_group_id))
        else:
            group = project_groups.project_group_get_by_name(project_group_id)

        if not group:
            raise exc.NotFound(_("Project Group %s not found")
                               % project_group_id)

        return [wmodels.Project.from_db_model(project)
                for project in group.projects]

    @decorators.db_exceptions
    @secure(checks.superuser)
    @wsme_pecan.wsexpose(wmodels.Project, int, int)
    def put(self, project_group_id, project_id):
        """Add a project to a project_group.
           This command is only available to Admin users.

        Example::

          curl https://my.example.org/api/v1/project_groups/17/projects/17 \\
          -X PUT -H 'Authorization: Bearer MY_ACCESS_TOKEN' \\
          -H 'Content-Type: application/json;charset=UTF-8' \\
          --data-binary '{}'

        :param project_group_id: An ID of the project group.
        :param project_id: An ID of project in this project group.
        """

        project_groups.project_group_add_project(project_group_id, project_id)

        return wmodels.Project.from_db_model(projects.project_get(project_id))

    @decorators.db_exceptions
    @secure(checks.superuser)
    @wsme_pecan.wsexpose(None, int, int, status_code=204)
    def delete(self, project_group_id, project_id):
        """Delete a project from a project_group.
           This command is only available to Admin users.

        Example::

          curl https://my.example.org/api/v1/project_groups/17/projects/1 \\
          -X DELETE -H 'Authorization: Bearer MY_ACCESS_TOKEN'

        :param project_group_id: An ID of the project group.
        :param project_id: An ID of project in this project group.
        """

        project_groups.project_group_delete_project(project_group_id,
                                                    project_id)


class ProjectGroupsController(rest.RestController):
    """REST controller for Project Groups.

    NOTE: PUT requests should be used to update only top-level fields.
    The nested fields (projects) should be updated using requests to a
    projects subcontroller.
    """

    validation_post_schema = validations.PROJECT_GROUPS_POST_SCHEMA
    validation_put_schema = validations.PROJECT_GROUPS_PUT_SCHEMA

    @decorators.db_exceptions
    @secure(checks.guest)
    @wsme_pecan.wsexpose(wmodels.ProjectGroup, int)
    def get_one_by_id(self, project_group_id):
        """Retrieve information about the given project group.

        Example::

          curl https://my.example.org/api/v1/project_groups/55

        :param project_group_id: Project group id.
        """

        group = project_groups.project_group_get(project_group_id)
        if not group:
            raise exc.NotFound(_("Project Group %s not found")
                               % project_group_id)

        return wmodels.ProjectGroup.from_db_model(group)

    @decorators.db_exceptions
    @secure(checks.guest)
    @wsme_pecan.wsexpose(wmodels.ProjectGroup, wtypes.text)
    def get_one_by_name(self, project_group_name):
        """Retrieve information about the given project group.

        :param project_group_name: Project group name.

        """
        group = project_groups.project_group_get_by_name(project_group_name)

        if group:
            return wmodels.ProjectGroup.from_db_model(group)
        else:
            raise exc.NotFound(_("Project Group %s not found") %
                               project_group_name)

    @decorators.db_exceptions
    @secure(checks.guest)
    @wsme_pecan.wsexpose([wmodels.ProjectGroup], int, int, int, wtypes.text,
                         wtypes.text, int, wtypes.text, wtypes.text)
    def get(self, marker=None, offset=None, limit=None, name=None, title=None,
            subscriber_id=None, sort_field='id', sort_dir='asc'):
        """Retrieve a list of projects groups.

        Example::

          curl https://my.example.org/api/v1/project_groups

        :param marker: The resource id where the page should begin.
        :param offset: The offset to start the page at.
        :param limit: The number of project groups to retrieve.
        :param name: A string to filter the name by.
        :param title: A string to filter the title by.
        :param subscriber_id: The ID of a subscriber to filter by.
        :param sort_field: The name of the field to sort on.
        :param sort_dir: Sort direction for results (asc, desc).
        """

        if limit is not None:
            limit = max(0, limit)

        # Resolve the marker record.
        marker_group = None
        if marker is not None:
            marker_group = project_groups.project_group_get(marker)

        groups = project_groups.project_group_get_all(
            marker=marker_group,
            offset=offset,
            limit=limit,
            name=name,
            title=title,
            subscriber_id=subscriber_id,
            sort_field=sort_field,
            sort_dir=sort_dir)

        group_count = project_groups.project_group_get_count(
            name=name, title=title, subscriber_id=subscriber_id)

        # Apply the query response headers.
        if limit:
            response.headers['X-Limit'] = str(limit)
        response.headers['X-Total'] = str(group_count)
        if marker_group:
            response.headers['X-Marker'] = str(marker_group.id)
        if offset is not None:
            response.headers['X-Offset'] = str(offset)

        return [wmodels.ProjectGroup.from_db_model(group) for group in groups]

    @decorators.db_exceptions
    @secure(checks.superuser)
    @wsme_pecan.wsexpose(wmodels.ProjectGroup, body=wmodels.ProjectGroup)
    def post(self, project_group):
        """Create a new project group.
           This command is only available to Admin users.

        Example::

          curl https://my.example.org/api/v1/project_groups \\
          -H 'Authorization: Bearer MY_ACCESS_TOKEN' \\
          -H 'Content-Type: application/json;charset=UTF-8' \\
          --data-binary '{"title":"test-group","name":"test-group"}'

        :param project_group: A project group within the request body.
        """

        created_group = project_groups.project_group_create(
            project_group.as_dict())

        return wmodels.ProjectGroup.from_db_model(created_group)

    @decorators.db_exceptions
    @secure(checks.superuser)
    @wsme_pecan.wsexpose(wmodels.ProjectGroup, int, body=wmodels.ProjectGroup)
    def put(self, project_group_id, project_group):
        """Modify this project group.
           This command is only available to Admin users.

        Example::

          curl https://my.example.org/api/v1/project_groups/17 -X PUT \\
          -H 'Authorization: Bearer MY_ACCESS_TOKEN' \\
          -H 'Content-Type: application/json;charset=UTF-8' \\
          --data-binary '{"id":17,"name":"test-group",\\
                          "title":"test-group-that-is-changed"}'

        :param project_group_id: An ID of the project group.
        :param project_group: A project group within the request body.
        """

        updated_group = project_groups.project_group_update(
            project_group_id,
            project_group.as_dict(omit_unset=True))

        return wmodels.ProjectGroup.from_db_model(updated_group)

    @decorators.db_exceptions
    @secure(checks.superuser)
    @wsme_pecan.wsexpose(None, int, status_code=204)
    def delete(self, project_group_id):
        """Delete this project group.
           This command is only available to Admin users.

        Example::

          curl https://my.example.org/api/v1/project_groups/17 -X DELETE \\
          -H 'Authorization: Bearer MY_ACCESS_TOKEN'

        :param project_group_id: An ID of the project group.
        """
        try:
            project_groups.project_group_delete(project_group_id)
        except exc.NotFound as not_found_exc:
            abort(404, not_found_exc.message)

    projects = ProjectsSubcontroller()

    @expose()
    def _route(self, args, request):
        if request.method == 'GET' and len(args) > 0:
            something = unquote(args[0])

            if _is_int(something):
                if len(args) == 1:
                    return self.get_one_by_id, args
            elif args[-1] != 'projects':
                return self.get_one_by_name, ["/".join(args)]
            else:
                # If a getting a groups' projects by name, handle the case
                # where the project group has slashes in the name by joining
                # all but the last arg with slashes.
                args = ["/".join(args[:-1]), args[-1]]

        return super(ProjectGroupsController, self)._route(args, request)
