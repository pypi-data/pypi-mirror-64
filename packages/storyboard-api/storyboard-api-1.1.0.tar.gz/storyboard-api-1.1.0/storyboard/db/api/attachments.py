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

from storyboard.db.api import base as api_base
from storyboard.db import models


def get_by_id(attachment_id, current_user=None, session=None):
    query = api_base.model_query(models.Attachment, session=session)
    query = query.filter(models.Attachment.id == attachment_id)

    # Filter out attachments related to stories that the current user lacks
    # permissions to see
    query = query.join(models.Story)
    query = api_base.filter_private_stories(query, current_user)

    return query.first()


def _build_query(current_user=None, session=None, **kwargs):
    query = api_base.model_query(models.Attachment, session=session)
    query = api_base.apply_query_filters(query=query,
                                         model=models.Attachment,
                                         **kwargs)

    # Filter out attachments related to stories that the current user lacks
    # permissions to see
    query = query.join(models.Story)
    query = api_base.filter_private_stories(query, current_user)

    return query


def get_all(current_user=None, session=None, **kwargs):
    query = _build_query(current_user=current_user, session=session, **kwargs)
    return query.all()


def get_count(current_user=None, session=None, **kwargs):
    query = _build_query(current_user=current_user, session=session, **kwargs)
    return query.count()


def create(attachment_dict):
    return api_base.entity_create(models.Attachment, attachment_dict)
