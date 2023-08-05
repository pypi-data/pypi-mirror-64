'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1010 import KeyedJointDesign
    from ._1011 import KeyTypes
    from ._1012 import KeywayJointHalfDesign
    from ._1013 import NumberOfKeys
