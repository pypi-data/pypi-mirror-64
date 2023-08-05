# -*- coding: utf-8 -*-

import logging

from spaceone.core.service import *
from spaceone.secret.error.custom import *
from spaceone.secret.manager.identity_manager import IdentityManager
from spaceone.secret.manager.secret_manager import SecretManager
from spaceone.secret.manager.secret_group_manager import SecretGroupManager
from spaceone.secret.manager.secret_connector_manager import SecretConnectorManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class SecretService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_mgr: SecretManager = self.locator.get_manager('SecretManager')

    @transaction
    @check_required(['name', 'data', 'domain_id'])
    def create(self, params):
        """ Create secret

        Args:
            params (dict): {
                'name': 'str',
                'data': 'dict',
                'tags': 'dict',
                'schema_id': 'str',
                'project_id': 'str',
                'domain_id': 'str
            }

        Returns:
            secret_vo
        """

        if 'project_id' in params:
            self._check_project(params['project_id'], params['domain_id'])

        secret_vo = self.secret_mgr.create_secret(params)

        secret_conn_mgr: SecretConnectorManager = self.locator.get_manager('SecretConnectorManager')
        secret_conn_mgr.create_secret(secret_vo.secret_id, params)

        return secret_vo

    @transaction
    @check_required(['secret_id', 'domain_id'])
    def update(self, params):
        """ Update secret

        Args:
            params (dict): {
                'secret_id': 'str',
                'name': 'str' ,
                'tags': 'dict',
                'project_id': 'str',
                'release_project': 'bool',
                'domain_id': 'str'
            }

        Returns:
            secret_vo
        """

        domain_id = params['domain_id']
        secret_id = params['secret_id']
        project_id = params.get('project_id')
        release_project = params.get('release_project', False)

        secret_vo = self.secret_mgr.get_secret(secret_id, domain_id)

        if release_project:
            params['project_id'] = None
        else:
            if project_id:
                self._check_project(project_id, domain_id)

        secret_vo = self.secret_mgr.update_secret_by_vo(params, secret_vo)

        return secret_vo

    @transaction
    @check_required(['secret_id', 'domain_id'])
    def delete(self, params):
        """ Delete secret

        Args:
            params (dict): {
                'secret_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            None
        """

        domain_id = params['domain_id']
        secret_id = params['secret_id']

        secret_vo = self.secret_mgr.get_secret(secret_id, domain_id)

        secret_conn_mgr: SecretConnectorManager = self.locator.get_manager('SecretConnectorManager')
        secret_conn_mgr.delete_secret(secret_id)

        self.secret_mgr.delete_secret_by_vo(secret_vo)

    @transaction
    @check_required(['secret_id', 'domain_id'])
    def get_data(self, params):
        """ Get secret data through backend Secret service

        Args:
            params (dict): {
                'secret_id': 'str',
                'secret_group_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            secret_data (dict)
            environment (dict)
        """

        domain_id = params['domain_id']
        secret_id = params['secret_id']
        secret_group_id = params.get('secret_group_id')

        secret_vo = self.secret_mgr.get_secret(secret_id, domain_id)

        secret_data = self._get_secret_data(secret_id)
        environment = self._get_secret_environment(secret_vo, secret_group_id, domain_id)

        return secret_data, environment

    @transaction
    @check_required(['secret_id', 'domain_id'])
    def get(self, params):
        """ Get secret

        Args:
            params (dict): {
                'secret_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            secret_vo
        """

        return self.secret_mgr.get_secret(params['secret_id'], params['domain_id'])

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(['secret_id', 'name', 'secret_group_id', 'domain_id'])
    def list(self, params):
        """ List secrets

        Args:
            params (dict): {
                'secret_id': 'str',
                'name': 'str',
                'include_secret_group': 'bool',
                'secret_group_id': 'str',
                'query': 'dict',
                'domain_id': 'str'
            }

        Returns:
            results (list)
            total_count (int)
        """


        query = params.get('query', {})
        include_secret_group = params.get('include_secret_group', False)
        secret_vos, total_count = self.secret_mgr.list_secrets(query, include_secret_group)

        if include_secret_group:
            secret_vos = self.secret_mgr.get_related_secret_groups(secret_vos)

        return secret_vos, total_count

    def _get_secret_environment(self, secret_vo, secret_group_id, domain_id):
        if secret_group_id:
            self.secret_group_mgr: SecretGroupManager = self.locator.get_manager('SecretGroupManager')
            secret_group_vo = self.secret_group_mgr.get_secret_group(secret_group_id, domain_id)
            secret_group_map_vo = self._get_secret_group_map(secret_group_vo, secret_vo)

            environment = secret_group_vo.environment
            environment.update(secret_group_map_vo.environment)
            return environment
        else:
            return {}

    def _get_secret_data(self, secret_id):
        secret_conn_mgr: SecretConnectorManager = self.locator.get_manager('SecretConnectorManager')
        return secret_conn_mgr.get_secret(secret_id)

    def _check_project(self, project_id, domain_id):
        identity_mgr: IdentityManager = self.locator.get_manager('IdentityManager')
        identity_mgr.get_project(project_id, domain_id)

        return True

    def _get_secret_group_map(self, secret_group_vo, secret_vo):
        secret_group_map_vos, total_count = self._list_secret_group_map(secret_group_vo, secret_vo)

        if total_count == 0:
            raise ERROR_NOT_EXIST_SECRET_IN_GROUP(secret_id=secret_vo.secret_id,
                                                  secret_group_id=secret_group_vo.secret_group_id)

        return secret_group_map_vos[0]

    def _list_secret_group_map(self, secret_group_vo, secret_vo):
        query = {
            'filter': [
                {'k': 'secret_group_id', 'v': secret_group_vo.secret_group_id, 'o': 'eq'},
                {'k': 'secret_id', 'v': secret_vo.secret_id, 'o': 'eq'}
            ]
        }

        return self.secret_group_mgr.list_secret_group_maps(query)
