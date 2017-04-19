# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import zbw.ejDatasets


class ZbwEjdatasetsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=zbw.ejDatasets)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'zbw.ejDatasets:default')


ZBW_EJDATASETS_FIXTURE = ZbwEjdatasetsLayer()


ZBW_EJDATASETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ZBW_EJDATASETS_FIXTURE,),
    name='ZbwEjdatasetsLayer:IntegrationTesting'
)


ZBW_EJDATASETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ZBW_EJDATASETS_FIXTURE,),
    name='ZbwEjdatasetsLayer:FunctionalTesting'
)


ZBW_EJDATASETS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ZBW_EJDATASETS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ZbwEjdatasetsLayer:AcceptanceTesting'
)
