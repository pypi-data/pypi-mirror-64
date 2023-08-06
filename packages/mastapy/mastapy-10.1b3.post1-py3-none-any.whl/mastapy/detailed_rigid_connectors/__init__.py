'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._968 import DetailedRigidConnectorDesign
    from ._969 import DetailedRigidConnectorHalfDesign
