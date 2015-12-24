
import os
import sys
import unittest
import yaml
from upm.util.Assert import *

import mtm.ioc.Container as Container
from mtm.ioc.Inject import Inject
import mtm.ioc.Assertions as Assertions

from upm.util.VarManager import VarManager
from upm.config.ConfigYaml import ConfigYaml

ScriptDir = os.path.dirname(os.path.realpath(__file__))

class TestConfigYaml(unittest.TestCase):
    def setUp(self):
        Container.clear()

    def testSimple(self):
        yamlPath = ScriptDir + '/ExampleConfig.yaml'
        Container.bind('ConfigYaml').toSingle(ConfigYaml, [yamlPath])
        config = Container.resolve('ConfigYaml')

        assertIsEqual(config.getString('date'), '2012-08-06')
        assertIsEqual(config.getString('receipt'), 'Oz-Ware Purchase Invoice')

        assertIsEqual(config.getList('places'), ['New Jersey', 'New York'])
        assertRaisesAny(lambda: config.getString('places'))
        assertRaisesAny(lambda: config.getDictionary('places'))

        assertIsEqual(config.getDictionary('customer'),
          {'first_name': 'Dorothy', 'family_name': 'Gale'})

        # Tests YAML references
        assertIsEqual(config.getString('foo1'), config.getString('receipt'))

    def testMultiple(self):
        Container.bind('ConfigYaml').toSingle(ConfigYaml, [ScriptDir + '/ExampleConfig.yaml', ScriptDir + '/ExampleConfig2.yaml'])
        config = Container.resolve('ConfigYaml')

        # From 1
        assertIsEqual(config.getString('receipt'), 'Oz-Ware Purchase Invoice')

        # From 2
        assertIsEqual(config.getString('thing1'), 'Foo')

        # Second one should override
        assertIsEqual(config.getString('foo2'), 'ipsum')

        assertIsEqual(config.getString('nest1', 'firstName'), 'Dorothy')

        # Test concatenating lists together
        assertIsEqual(config.getList('list1'), ['lorem', 'ipsum', 'asdf', 'joe', 'frank'])

        # Test concatenating dictionaries together
        assertIsEqual(config.getDictionary('dict1'), {'joe': 5, 'mary': 15, 'kate': 5, 'jim': 10})

if __name__ == '__main__':
    unittest.main()