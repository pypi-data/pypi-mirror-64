'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1510 import BearingConnectionComponent
    from ._1511 import InternalClearanceClass
    from ._1512 import BearingToleranceClass
    from ._1513 import BearingToleranceDefinitionOptions
    from ._1514 import InnerRingTolerance
    from ._1515 import InnerSupportTolerance
    from ._1516 import InterferenceDetail
    from ._1517 import InterferenceTolerance
    from ._1518 import ITDesignation
    from ._1519 import OuterRingTolerance
    from ._1520 import OuterSupportTolerance
    from ._1521 import RaceDetail
    from ._1522 import RaceRoundnessAtAngle
    from ._1523 import RingTolerance
    from ._1524 import RoundnessSpecification
    from ._1525 import RoundnessSpecificationType
    from ._1526 import SupportDetail
    from ._1527 import SupportTolerance
    from ._1528 import SupportToleranceLocationDesignation
