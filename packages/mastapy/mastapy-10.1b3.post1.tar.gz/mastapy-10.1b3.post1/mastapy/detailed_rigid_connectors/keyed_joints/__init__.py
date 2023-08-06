'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1018 import KeyedJointDesign
    from ._1019 import KeyTypes
    from ._1020 import KeywayJointHalfDesign
    from ._1021 import NumberOfKeys
