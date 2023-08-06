'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1262 import ScriptingSetup
    from ._1263 import UserDefinedPropertyKey
