""" Test to make sure that the view match the fixtures"""
import os
from testscenarios.testcase import TestWithScenarios
from testtools import TestCase
from jenkins_jobs_addons import views
from tests.base import get_scenarios, BaseTestCase


class TestCaseModulePublishers(TestWithScenarios, TestCase, BaseTestCase):
    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')
    scenarios = get_scenarios(fixtures_path)
    klass = views.Views
