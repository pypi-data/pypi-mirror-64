# -----------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2020 Robbie Coenmans
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

class WorkitemType(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.url = None
    
class Project(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.url = None
        self.state = None
        self.revision = 0
        self.visibility = 'private'
        self.capabilities = None

class Workitem(object):
    def __init__(self):
        self.id = None
        self.rev = 1
        self.url = None
        self.fields = None

class Area(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.structure_type = 'area'
        self.has_children = False
        self.children = []

class Iteration(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.structure_type = 'iteration'
        self.attributes = Attributes()
        self.attributes.startDate = None,
        self.attributes.finishDate = None
        self.has_children = False
        self.children = []

class Attributes(object):
    def __init__(self):
        pass

class Attachment(object):
    def __init__(self):
        self.id = None
        self.url = None

class TestPlan(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.start_date = None
        self.end_date = None

class QueryResult(object):
    def __init__(self):
        self.query_type = 'three'
        self.as_of = None
        self.columns = []
        self.rows = []

class JsonPatchOperation(object):
    def __init__(self, operation, path, value):
        self.op = operation
        self.path = path
        self.value = value

class JsonPatchDocument(list):
    def add(self, operation: JsonPatchOperation):
        self.append(operation)

class Field(object):
    def __init__(self):
        self.name = None
        self.description = None
        self.ref_name = None
        self.type = None
        self.usage = None
        self.read_only = False
        self.can_sort_by = False
        self.is_queryable = False
        self.supported_operations = []
        self.is_identity = False
        self.is_picklist = False
        self.is_picklist_suggested = False
        self.url = None