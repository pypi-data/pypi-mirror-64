'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1024 import AssemblyMethods
    from ._1025 import CalculationMethods
    from ._1026 import InterferenceFitDesign
    from ._1027 import InterferenceFitHalfDesign
    from ._1028 import StressRegions
    from ._1029 import Table4JointInterfaceTypes
