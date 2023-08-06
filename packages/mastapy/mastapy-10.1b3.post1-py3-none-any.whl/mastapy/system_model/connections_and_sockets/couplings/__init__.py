'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1892 import ClutchConnection
    from ._1893 import ClutchSocket
    from ._1894 import ConceptCouplingConnection
    from ._1895 import ConceptCouplingSocket
    from ._1896 import CouplingConnection
    from ._1897 import CouplingSocket
    from ._1898 import PartToPartShearCouplingConnection
    from ._1899 import PartToPartShearCouplingSocket
    from ._1900 import SpringDamperConnection
    from ._1901 import SpringDamperSocket
    from ._1902 import TorqueConverterConnection
    from ._1903 import TorqueConverterPumpSocket
    from ._1904 import TorqueConverterTurbineSocket
