'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._740 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._741 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._742 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._743 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
