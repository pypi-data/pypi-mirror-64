'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2091 import BoostPressureInputOptions
    from ._2092 import InputPowerInputOptions
    from ._2093 import PressureRatioInputOptions
    from ._2094 import RotorSetDataInputFileOptions
    from ._2095 import RotorSetMeasuredPoint
    from ._2096 import RotorSpeedInputOptions
    from ._2097 import SuperchargerMap
    from ._2098 import SuperchargerMaps
    from ._2099 import SuperchargerRotorSet
    from ._2100 import SuperchargerRotorSetDatabase
    from ._2101 import YVariableForImportedData
