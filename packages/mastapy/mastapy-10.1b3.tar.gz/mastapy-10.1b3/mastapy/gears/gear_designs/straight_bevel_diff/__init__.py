'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._716 import StraightBevelDiffGearDesign
    from ._717 import StraightBevelDiffGearMeshDesign
    from ._718 import StraightBevelDiffGearSetDesign
    from ._719 import StraightBevelDiffMeshedGearDesign
