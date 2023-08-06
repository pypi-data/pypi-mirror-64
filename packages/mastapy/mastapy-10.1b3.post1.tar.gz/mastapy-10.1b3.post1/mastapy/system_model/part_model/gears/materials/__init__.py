'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2102 import GearMaterialExpertSystemMaterialDetails
    from ._2103 import GearMaterialExpertSystemMaterialOptions
