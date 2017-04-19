# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from zbw.ejDatasets.testing import ZBW_EJDATASETS_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that zbw.ejDatasets is properly installed."""

    layer = ZBW_EJDATASETS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if zbw.ejDatasets is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'zbw.ejDatasets'))

    def test_browserlayer(self):
        """Test that IZbwEjdatasetsLayer is registered."""
        from zbw.ejDatasets.interfaces import (
            IZbwEjdatasetsLayer)
        from plone.browserlayer import utils
        self.assertIn(IZbwEjdatasetsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = ZBW_EJDATASETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['zbw.ejDatasets'])

    def test_product_uninstalled(self):
        """Test if zbw.ejDatasets is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'zbw.ejDatasets'))

    def test_browserlayer_removed(self):
        """Test that IZbwEjdatasetsLayer is removed."""
        from zbw.ejDatasets.interfaces import \
            IZbwEjdatasetsLayer
        from plone.browserlayer import utils
        self.assertNotIn(IZbwEjdatasetsLayer, utils.registered_layers())
