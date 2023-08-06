'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._6479 import MeasurementType
    from ._6480 import MeasurementTypeExtensions
