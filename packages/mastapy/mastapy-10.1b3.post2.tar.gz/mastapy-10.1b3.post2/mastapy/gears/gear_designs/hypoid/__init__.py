'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._740 import HypoidGearDesign
    from ._741 import HypoidGearMeshDesign
    from ._742 import HypoidGearSetDesign
    from ._743 import HypoidMeshedGearDesign
