'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1872 import ClutchConnection
    from ._1873 import ClutchSocket
    from ._1874 import ConceptCouplingConnection
    from ._1875 import ConceptCouplingSocket
    from ._1876 import CouplingConnection
    from ._1877 import CouplingSocket
    from ._1878 import PartToPartShearCouplingConnection
    from ._1879 import PartToPartShearCouplingSocket
    from ._1880 import SpringDamperConnection
    from ._1881 import SpringDamperSocket
    from ._1882 import TorqueConverterConnection
    from ._1883 import TorqueConverterPumpSocket
    from ._1884 import TorqueConverterTurbineSocket
