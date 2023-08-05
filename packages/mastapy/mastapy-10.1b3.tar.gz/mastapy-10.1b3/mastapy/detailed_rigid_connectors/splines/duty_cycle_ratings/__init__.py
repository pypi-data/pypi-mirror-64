'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1006 import AGMA6123SplineJointDutyCycleRating
    from ._1007 import GBT17855SplineJointDutyCycleRating
    from ._1008 import SAESplineJointDutyCycleRating
