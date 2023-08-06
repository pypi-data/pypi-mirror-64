# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

"""Add an attachments table

Revision ID: 067
Revises: 066
Create Date: 2019-01-27 16:07:04.427155

"""

# revision identifiers, used by Alembic.
revision = '067'
down_revision = '066'


from alembic import op
from oslo_log import log
import sqlalchemy as sa

import storyboard

LOG = log.getLogger(__name__)


def upgrade(active_plugins=None, options=None):
    op.create_table('attachments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', storyboard.db.decorators.UTCDateTime(),
                  nullable=True),
        sa.Column('updated_at', storyboard.db.decorators.UTCDateTime(),
                  nullable=True),
        sa.Column('name', sa.Unicode(length=255), nullable=False),
        sa.Column('link', sa.UnicodeText(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False, index=True),
        sa.Column('story_id', sa.Integer(), nullable=False, index=True),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    version_info = op.get_bind().engine.dialect.server_version_info
    if version_info[-1] == "MariaDB":
        # Removes fake mysql prefix
        version_info = version_info[-4:]
    if version_info[0] < 5 or version_info[0] == 5 and version_info[1] < 6:
        LOG.warning(
            "MySQL version is lower than 5.6. Skipping full-text index")
        return

    op.execute("ALTER TABLE attachments ADD FULLTEXT attachments_fti (name)")


def downgrade(active_plugins=None, options=None):
    op.drop_table('attachments')
