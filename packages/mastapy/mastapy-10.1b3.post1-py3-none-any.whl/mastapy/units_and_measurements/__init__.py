'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._6499 import MeasurementType
    from ._6500 import MeasurementTypeExtensions
