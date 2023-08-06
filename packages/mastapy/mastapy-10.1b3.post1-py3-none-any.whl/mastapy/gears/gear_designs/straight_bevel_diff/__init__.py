'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._724 import StraightBevelDiffGearDesign
    from ._725 import StraightBevelDiffGearMeshDesign
    from ._726 import StraightBevelDiffGearSetDesign
    from ._727 import StraightBevelDiffMeshedGearDesign
