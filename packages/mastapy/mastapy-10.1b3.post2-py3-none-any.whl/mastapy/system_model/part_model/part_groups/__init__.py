'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2003 import ConcentricOrParallelPartGroup
    from ._2004 import ConcentricPartGroup
    from ._2005 import ConcentricPartGroupParallelToThis
    from ._2006 import DesignMeasurements
    from ._2007 import ParallelPartGroup
    from ._2008 import PartGroup
