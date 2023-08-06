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

from hashlib import sha1
import hmac
from time import time
import uuid

import openstack
from openstack import connection
from oslo_config import cfg
from six.moves.urllib import parse

from storyboard.api.v1.storage.storage import StorageBackend


CONF = cfg.CONF

SWIFT_OPTS = [
    cfg.StrOpt("cloud",
               default="",
               help="Name of the cloud which provides Swift as "
                    "used in `clouds.yaml`. Other auth-related "
                    "options are ignored if this is set."),
    cfg.StrOpt("auth_url",
               default="http://127.0.0.1:8888/auth/v1.0",
               help="URL to use to obtain an auth token from swift."),
    cfg.StrOpt("auth_type",
               default="v1password",
               help="Swift auth type, defaults to 'v1password' "
                    "(which is legacy auth)."),
    cfg.StrOpt("user",
               default="test:tester",
               help="User to use when authenticating with Swift to obtain an "
                    "auth token."),
    cfg.StrOpt("password",
               default="testing",
               help="Password to use when authenticating with Swift."),
    cfg.StrOpt("container",
               default="storyboard",
               help="Swift container to store attachments in. Will be "
                    "created if it doesn't already exist."),
    cfg.StrOpt("temp_url_key",
               default="secret_key",
               help="Temp URL secret key to set for the container if it "
                    "is created by StoryBoard."),
    cfg.IntOpt("temp_url_timeout",
               default=120,
               help="Number of seconds that Swift tempurl signatures "
                    "are valid for after generation.")
]

CONF.register_opts(SWIFT_OPTS, "swift")


class SwiftStorageImpl(StorageBackend):
    """Implementation of an attachment storage backend using swift."""

    def _get_connection(self):
        if CONF.swift.cloud:
            return connection.Connection(
                cloud=CONF.swift.cloud,
                service_types={'object-store'})

        return openstack.connect(
            auth_type=CONF.swift.auth_type,
            auth_url=CONF.swift.auth_url,
            username=CONF.swift.user,
            password=CONF.swift.password,
        )

    def _ensure_container_exists(self, conn):
        names = [container.name
                 for container in conn.object_store.containers()]
        if CONF.swift.container not in names:
            conn.object_store.create_container(CONF.swift.container)
            conn.object_store.set_container_temp_url_key(
                CONF.swift.container, CONF.swift.temp_url_key)
            container = conn.object_store.set_container_metadata(
                CONF.swift.container, read_ACL=".r:*")

    def get_upload_url(self):
        conn = self._get_connection()
        self._ensure_container_exists(conn)

        url = conn.object_store.get_endpoint()
        return "%s/%s" % (url, CONF.swift.container)

    def get_auth(self):
        conn = self._get_connection()
        self._ensure_container_exists(conn)

        name = str(uuid.uuid4())
        endpoint = parse.urlparse(conn.object_store.get_endpoint())
        path = '/'.join((endpoint.path, CONF.swift.container, name))

        method = 'PUT'
        expires = int(time() + CONF.swift.temp_url_timeout)
        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        hmac_body = hmac_body.encode('utf8')

        key = conn.object_store.get_temp_url_key(CONF.swift.container)
        signature = hmac.new(key, hmac_body, sha1).hexdigest()
        return expires, signature, name
