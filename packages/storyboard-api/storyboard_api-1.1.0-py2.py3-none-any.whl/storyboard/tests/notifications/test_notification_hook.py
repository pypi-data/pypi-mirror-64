# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
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
# implied. See the License for the specific language governing permissions and
# limitations under the License.

from mock import Mock
from mock import patch
from storyboard.api.v1.v1_controller import V1Controller
from storyboard.api.v1.wmodels import Task as TaskWmodel
import storyboard.common.hook_priorities as priority
from storyboard.db.models import Task
from storyboard.notifications.notification_hook import NotificationHook
from storyboard.tests.db import base
from wsme.rest.json import tojson


class TestNotificationHook(base.BaseDbTestCase):

    def test_priority(self):
        """Assert that this hook has default priority."""
        self.assertEqual(NotificationHook.priority, priority.DEFAULT)

    def test_parse(self):
        """Test various permutations of the notification parser."""

        notifier = NotificationHook()

        self.assertEqual(
            ('project_group', '1', None, None),
            notifier.parse('/v1/project_groups/1')
        )
        self.assertEqual(
            ('project_group', '2', None, None),
            notifier.parse('/v1/project_groups/2')
        )
        self.assertEqual(
            ('project_group', '2', 'project', '1'),
            notifier.parse('/v1/project_groups/2/projects/1')
        )

        self.assertEqual(
            ('project', '2', None, None),
            notifier.parse('/v1/projects/2')
        )

        self.assertEqual(
            ('story', '2', None, None),
            notifier.parse('/v1/stories/2')
        )
        self.assertEqual(
            ('story', '2', 'comment', None),
            notifier.parse('/v1/stories/2/comments')
        )
        self.assertEqual(
            ('story', '2', 'comment', '4'),
            notifier.parse('/v1/stories/2/comments/4')
        )
        self.assertEqual(
            ('task', '2', None, None),
            notifier.parse('/v1/tasks/2')
        )
        self.assertEqual(
            (None, None, None, None),
            notifier.parse('/v1/openid/authorize')
        )

    def test_singularize_resource(self):
        """Enforce singularization for all first level resources. This acts
        as a catchall to make sure that newly added resources are registered
        in the singularization method.
        """
        n = NotificationHook()

        # Extract all resource names from the root level resource.
        keys = vars(V1Controller).keys()
        for key in keys:
            # Strip out private things.
            if key[0:2] == '__':
                continue

            singular = n.singularize_resource(key)
            self.assertIsNotNone(singular)

        # Special case some second-level cases that matter:
        self.assertEqual('comment',
                         n.singularize_resource('comments'))

        # Confirm that the expected values are returned.
        self.assertEqual('story',
                         n.singularize_resource('stories'))
        self.assertEqual('project',
                         n.singularize_resource('projects'))
        self.assertEqual('project_group',
                         n.singularize_resource('project_groups'))
        self.assertEqual('timeline_event',
                         n.singularize_resource('timeline_events'))
        self.assertEqual('user',
                         n.singularize_resource('users'))
        self.assertEqual('team',
                         n.singularize_resource('teams'))
        self.assertEqual('tag',
                         n.singularize_resource('tags'))
        self.assertEqual('task_status',
                         n.singularize_resource('task_statuses'))
        self.assertEqual('subscription',
                         n.singularize_resource('subscriptions'))
        self.assertEqual('subscription_event',
                         n.singularize_resource('subscription_events'))
        self.assertEqual('systeminfo',
                         n.singularize_resource('systeminfo'))
        self.assertEqual('openid',
                         n.singularize_resource('openid'))

    def test_get_original_resource_invalid_options(self):
        """Assert that the get_original_resource method behaves as expected
        when receiving invalid values.
        """
        n = NotificationHook()

        # Test no resource
        self.assertIsNone(n.get_original_resource(None, None))

        # Test invalid resource.
        self.assertIsNone(n.get_original_resource('invalid', 1))

        # Test no resource_id
        self.assertIsNone(n.get_original_resource('story', None))

        # Test invalid (gone) resource_id.
        self.assertIsNone(n.get_original_resource('story', 1000000))

    @patch('storyboard.db.api.base.entity_get')
    def test_get_original_resource_valid_options(self, mock_entity_get):
        """Assert that the get_original_resource method behaves as expected
        when receiving valid values.
        """
        n = NotificationHook()

        # Mock entity_get method to return a sample Task
        sample_task = Task(id=1,
                           creator_id=1,
                           title='Test',
                           status='inprogress',
                           story_id=1,
                           project_id=1,
                           assignee_id=1,
                           priority='medium')
        mock_entity_get.return_value = sample_task

        sample_task_wmodel = TaskWmodel.from_db_model(sample_task)
        old_entity_values = n.get_original_resource('task', 1)

        self.assertEqual(old_entity_values['id'],
                         sample_task_wmodel.id)
        self.assertEqual(old_entity_values['creator_id'],
                         sample_task_wmodel.creator_id)
        self.assertEqual(old_entity_values['title'],
                         sample_task_wmodel.title)
        self.assertEqual(old_entity_values['status'],
                         sample_task_wmodel.status)
        self.assertEqual(old_entity_values['story_id'],
                         sample_task_wmodel.story_id)
        self.assertEqual(old_entity_values['project_id'],
                         sample_task_wmodel.project_id)
        self.assertEqual(old_entity_values['assignee_id'],
                         sample_task_wmodel.assignee_id)

    @patch('storyboard.db.api.base.entity_get')
    def test_old_entity_values_set_on_state_by_before(self, mock_entity_get):
        """Tests that the values of the resource being changed by the
        request are retrieved in the before method and stored in the
        state object as variable 'old_returned_values'.
        """
        n = NotificationHook()

        # Mocking state object to simulate a 'PUT' request for task
        # resource 1
        mock_state = Mock()
        mock_state.request.method = 'PUT'
        mock_state.request.path = '/v1/tasks/1'

        # Mock entity_get method to return a sample Task
        sample_task = Task(id=1,
                           creator_id=1,
                           title='Test',
                           status='inprogress',
                           story_id=1,
                           project_id=1,
                           assignee_id=1,
                           priority='medium')
        mock_entity_get.return_value = sample_task

        sample_task_wmodel = TaskWmodel.from_db_model(sample_task)
        n.before(mock_state)

        self.assertEqual(mock_state.old_entity_values['id'],
                         sample_task_wmodel.id)
        self.assertEqual(mock_state.old_entity_values['creator_id'],
                         sample_task_wmodel.creator_id)
        self.assertEqual(mock_state.old_entity_values['title'],
                         sample_task_wmodel.title)
        self.assertEqual(mock_state.old_entity_values['status'],
                         sample_task_wmodel.status)
        self.assertEqual(mock_state.old_entity_values['story_id'],
                         sample_task_wmodel.story_id)
        self.assertEqual(mock_state.old_entity_values['project_id'],
                         sample_task_wmodel.project_id)
        self.assertEqual(mock_state.old_entity_values['assignee_id'],
                         sample_task_wmodel.assignee_id)

    @patch('storyboard.notifications.notification_hook.publish')
    @patch.object(NotificationHook, 'get_original_resource')
    def test_after_publishes_payload(self, mock_get_original_resource,
                                     mock_publish):
        n = NotificationHook()

        sample_original_task = TaskWmodel.from_db_model(Task(id=1,
                           creator_id=1,
                           title='Test',
                           status='inprogress',
                           story_id=1,
                           project_id=1,
                           assignee_id=1,
                           priority='medium'))

        sample_modified_task = TaskWmodel.from_db_model(Task(id=1,
                           creator_id=1,
                           title='Test',
                           status='merged',
                           story_id=1,
                           project_id=1,
                           assignee_id=1,
                           priority='medium'))

        sot_json = tojson(TaskWmodel, sample_original_task)
        smt_json = tojson(TaskWmodel, sample_modified_task)

        # Mocking state object to simulate a 'PUT' request for task
        # resource 1
        mock_state = Mock()
        mock_state.request.current_user_id = '1'
        mock_state.request.method = 'PUT'
        mock_state.request.headers = {'Referer': 'http://localhost/'}
        mock_state.request.query_string = ''
        mock_state.request.path = '/v1/tasks/1'
        mock_state.response.status_code = 200
        mock_state.old_entity_values = sot_json
        mock_get_original_resource.return_value = smt_json

        n.after(mock_state)
        mock_publish.assert_called_with(
            author_id=mock_state.request.current_user_id,
            method=mock_state.request.method,
            url=mock_state.request.headers['Referer'],
            path=mock_state.request.path,
            query_string=mock_state.request.query_string,
            status=mock_state.response.status_code,
            resource='task',
            resource_id='1',
            sub_resource=None,
            sub_resource_id=None,
            resource_before=sot_json,
            resource_after=smt_json)
