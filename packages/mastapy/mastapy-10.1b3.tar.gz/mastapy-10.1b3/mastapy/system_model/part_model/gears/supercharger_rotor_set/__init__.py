'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2071 import BoostPressureInputOptions
    from ._2072 import InputPowerInputOptions
    from ._2073 import PressureRatioInputOptions
    from ._2074 import RotorSetDataInputFileOptions
    from ._2075 import RotorSetMeasuredPoint
    from ._2076 import RotorSpeedInputOptions
    from ._2077 import SuperchargerMap
    from ._2078 import SuperchargerMaps
    from ._2079 import SuperchargerRotorSet
    from ._2080 import SuperchargerRotorSetDatabase
    from ._2081 import YVariableForImportedData
