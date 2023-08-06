# Copyright (c) 2019 Adam Coldrick
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

from oslo_config import cfg
from pecan import abort
from pecan import request
from pecan import response
from pecan import rest
from pecan.secure import secure
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from storyboard._i18n import _
from storyboard.api.auth import authorization_checks as checks
from storyboard.api.v1.storage import storage
from storyboard.api.v1 import wmodels
from storyboard.common import decorators
from storyboard.common import exception as exc
from storyboard.db.api import attachments as attachments_api
from storyboard.db.api import stories as stories_api


CONF = cfg.CONF

STORAGE_BACKEND = storage.get_storage_backend()


class AttachmentsController(rest.RestController):
    """Endpoint for managing attachments."""

    _custom_actions = {"upload_url": ["GET"]}

    @secure(checks.authenticated)
    @wsme_pecan.wsexpose(wtypes.text, int)
    def upload_url(self, story_id):
        """Return a URL which can be used to upload attachments.

        The storage type and authentication token are provided in the
        X-Storage-Type and X-Auth-Token response headers respectively.

        :param story_id: ID of the story the attachment is for.
            Currently unused, and just needed for routing.

        """
        response.headers['X-Storage-Type'] = CONF.attachments.storage_backend

        expiry, auth, name = STORAGE_BACKEND.get_auth()
        response.headers['X-Auth-Token'] = auth
        response.headers['X-Token-Expiry'] = str(expiry)
        response.headers['X-Object-Name'] = name

        return STORAGE_BACKEND.get_upload_url()

    @decorators.db_exceptions
    @secure(checks.guest)
    @wsme_pecan.wsexpose(wmodels.Attachment, int, int)
    def get_one(self, story_id, attachment_id):
        """Retrieve details about a single attachment.

        Example::

          curl https://my.example.org/api/v1/stories/1/attachments/1

        :param story_id: ID of the story which has the attachment.
        :param attachment_id: ID of the attachment to retrieve details
            about.

        """
        attachment = attachments_api.get_by_id(
            attachment_id, current_user=request.current_user_id)

        if attachment:
            return wmodels.Attachment.from_db_model(attachment)
        raise exc.NotFound(_("Attachment %s not found") % attachment_id)

    @decorators.db_exceptions
    @secure(checks.guest)
    @wsme_pecan.wsexpose([wmodels.Attachment], int)
    def get_all(self, story_id):
        """Retrieve details about all attachments for a given story.

        Example::

          curl https://my.example.org/api/v1/stories/1/attachments

        :param story_id: ID of the story to view attachments of.

        """
        attachments = attachments_api.get_all(
            story_id=story_id,
            current_user=request.current_user_id
        )
        attachment_count = attachments_api.get_count(
            story_id=story_id,
            current_user=request.current_user_id
        )

        response.headers['X-Total'] = str(attachment_count)
        return [wmodels.Attachment.from_db_model(a) for a in attachments]

    @decorators.db_exceptions
    @secure(checks.authenticated)
    @wsme_pecan.wsexpose(wmodels.Attachment, int, body=wmodels.Attachment)
    def post(self, story_id, attachment):
        """Create a record of a new attachment.

        Example::

          curl https://my.example.org/api/v1/stories/1/attachments \\
            -H 'Authorization: Bearer MY_ACCESS_TOKEN' \\
            -H 'Content-Type: application/json;charset=UTF-8' \\
            --data-binary '{"name":"logs.tar.gz",\\
            "link":"https://example.org/logs.tar.gz"}'

        :param story_id: The ID of the story the attachment is for.
        :param attachment: Attachment details within the request body.

        """
        attachment_dict = attachment.as_dict()
        user_id = request.current_user_id

        story = stories_api.story_get_simple(story_id, current_user=user_id)
        if not story:
            raise exc.NotFound(_("Story %s not found.") % story_id)
        if attachment.creator_id and attachment.creator_id != user_id:
            abort(400, _("You cannot select the creator of an attachment."))
        if attachment.story_id and attachment.story_id != story_id:
            abort(400, _("You cannot attach to a different story."))
        if not attachment.link:
            abort(400, _("An attachment must have a 'link' field."))
        if not attachment.name:
            abort(400, _("An attachment must have a 'name' field."))

        attachment_dict.update({
            "creator_id": user_id,
            "story_id": story_id
        })

        created_attachment = attachments_api.create(attachment_dict)
        return wmodels.Attachment.from_db_model(created_attachment)
