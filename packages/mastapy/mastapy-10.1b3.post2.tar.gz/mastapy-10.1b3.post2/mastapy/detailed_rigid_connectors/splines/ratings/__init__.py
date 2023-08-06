'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._996 import AGMA6123SplineHalfRating
    from ._997 import AGMA6123SplineJointRating
    from ._998 import DIN5466SplineHalfRating
    from ._999 import DIN5466SplineRating
    from ._1000 import GBT17855SplineHalfRating
    from ._1001 import GBT17855SplineJointRating
    from ._1002 import SAESplineHalfRating
    from ._1003 import SAESplineJointRating
    from ._1004 import SplineHalfRating
    from ._1005 import SplineJointRating
