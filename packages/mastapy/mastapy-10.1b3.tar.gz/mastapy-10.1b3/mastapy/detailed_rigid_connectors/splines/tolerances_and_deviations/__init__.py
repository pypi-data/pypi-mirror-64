'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._994 import FitAndTolerance
    from ._995 import SAESplineTolerances
