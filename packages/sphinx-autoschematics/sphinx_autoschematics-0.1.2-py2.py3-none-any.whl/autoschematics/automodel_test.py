# coding=utf8

import pytest
import textwrap

from schematics.types import StringType
from schematics.types.compound import ListType

from sphinx.testing import util

from autoschematics.automodel import as_annotation, full_model_class_name, humanize


def test_humanize():
    assert humanize("employee_salary") == "Employee salary"


def test_full_model_class_name():
    class ExampleModel(object):
        pass

    assert (
        full_model_class_name(ExampleModel)
        == "autoschematics.automodel_test.ExampleModel"
    )


def test_as_annotation():
    assert as_annotation(StringType()) == "StringType()"
    assert as_annotation(ListType(StringType)) == "ListType(StringType())"


@pytest.fixture(scope="module")
def rootdir():
    """rootdir is a sphinx fixture that allows for specifying where our "document root" is when running marked tests"""
    return util.path(__file__).parent.parent.abspath()


@pytest.mark.sphinx("html")
def test_documenters(app):
    app.build()
    content = app.env.get_doctree("index")
    expected = textwrap.dedent(
        u"""
    
        class models.ExampleModel
        
        ExampleModel is a model for testing
        
        Just like in Sphinx .rst files you can use restructured text directives in the
        docstring to provide rich content in the generated docs.
        
        foo: Foo
        bar:
          - bar1
          - bar2
          
          
          
        bar ListType(StringType())
        
        This is bar’s docstring
        
        Required: False
        
        Default: Undefined
        
        
        
        foo StringType()
        
        Required: True
        
        Default: Undefined
        
        Choices: fizz, buzz
        
        Another value: apple=3, one=1, two=2
        
        Custom value: True
        
        
        
        sub1 ModelType(SubModel1)
        
        See models.SubModel1
        
        This is sub1’s docstring
        
        Required: False
        
        Default: Undefined
        
        
        
        sub1a ModelType(SubModel1)
        
        See models.SubModel1
        
        Required: False
        
        Default: Undefined
        
        
        
        sub2 ListType(ModelType(SubModel2))
        
        See models.SubModel2
        
        Required: False
        
        Default: Undefined
        
        
        
        
        
        
        
        class models.SubModel1
        
        This is SubModel1’s docstring
        
        
        
        name StringType()
        
        Required: False
        
        Default: Undefined
        
        
        
        
        
        
        
        class models.SubModel2
        
        This is SubModel2’s docstring
        
        
        
        name StringType()
        
        Required: False
        
        Default: Undefined
        """.rstrip()
    )
    assert content.astext() == expected
