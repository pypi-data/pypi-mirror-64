# -*- coding: utf-8 -*-

import logging

from spaceone.core.manager import BaseManager
from spaceone.secret.connector.aws_secret_manager_connector import AWSSecretManagerConnector

_LOGGER = logging.getLogger(__name__)


class SecretConnectorManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_conn: AWSSecretManagerConnector = self.locator.get_connector('AWSSecretManagerConnector')

    def create_secret(self, secret_id, params):
        def _rollback(secret_id):
            _LOGGER.info(f'[ROLLBACK] Delete secret data in secret store : {secret_id}')
            self.secret_conn.delete_secret(secret_id)

        self.transaction.add_rollback(_rollback, secret_id)
        return self.secret_conn.create_secret(secret_id, params)

    def delete_secret(self, secret_id):
        self.secret_conn.delete_secret(secret_id)

    def get_secret(self, secret_id):
        return self.secret_conn.get_secret(secret_id)
