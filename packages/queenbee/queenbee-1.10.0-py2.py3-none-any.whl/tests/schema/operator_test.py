import yaml
from tests.base.io_test import BaseIOTest
from tests.base.value_error import BaseValueErrorTest

from queenbee.schema.operator import Operator

class TestIO(BaseIOTest):

    klass = Operator

class TestValueError(BaseValueErrorTest):

    klass = Operator
