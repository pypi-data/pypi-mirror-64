#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.auth import UserAssignedIdentity, ClientSecretAuthentication
import sys
import os
import tests.config as cfg


class AuthTests(unittest.TestCase):
    def setUp(self):
        # self.managed_identity = MsiAuthentication()

        self.user_assigned_identity = UserAssignedIdentity(
            cfg.auth["resource_group"],
            cfg.auth["managed_identity"],
            subscription_id=cfg.auth["subscription_id"],
        )

    def test_exists(self):
        self.assertTrue(self.user_assigned_identity is not None)

    def test_secret_credentials_by_params(self):
        self.client_secret_credentials = ClientSecretAuthentication(
            cfg.auth["tenant_id"],
            cfg.auth["subscription_id"],
            cfg.auth["client_id"],
            cfg.auth["client_secret"],
        )
        print(self.client_secret_credentials.get_credentials())

    def test_secret_credentials_by_env(self):
        os.environ["AZURE_TENANT_ID"] = cfg.auth["tenant_id"]
        os.environ["AZURE_SUBSCRIPTION_ID"] = cfg.auth["subscription_id"]
        os.environ["AZURE_CLIENT_ID"] = cfg.auth["client_id"]
        os.environ["AZURE_CLIENT_SECRET"] = cfg.auth["client_secret"]

        self.client_secret_credentials = ClientSecretAuthentication()
        print(self.client_secret_credentials.get_credentials())

    def test_container_group_identity(self):
        self.assertTrue(
            self.user_assigned_identity.get_container_group_identity() is not None
        )

    def test_managed_identity(self):
        self.assertTrue(self.user_assigned_identity is not None)


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()
