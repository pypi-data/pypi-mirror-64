'''_951.py

GearMeshDesignAnalysis
'''


from mastapy.gears.analysis import (
    _947, _948, _949, _950,
    _945
)
from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical import _395, _399, _400
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel import (
    _557, _558, _559, _560,
    _570, _571, _576
)
from mastapy.gears.ltca import _613
from mastapy.gears.ltca.cylindrical import _627
from mastapy.gears.ltca.conical import _638
from mastapy.gears.load_case import _644
from mastapy.gears.load_case.worm import _647
from mastapy.gears.load_case.face import _650
from mastapy.gears.load_case.cylindrical import _653
from mastapy.gears.load_case.conical import _656
from mastapy.gears.load_case.concept import _659
from mastapy.gears.load_case.bevel import _662
from mastapy.gears.gear_twod_fe_analysis import _667
from mastapy.gears.gear_designs.face import _756
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _844, _845
from mastapy.gears.fe_model import _929
from mastapy.gears.fe_model.cylindrical import _933
from mastapy.gears.fe_model.conical import _936
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_DESIGN_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearMeshDesignAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshDesignAnalysis',)


class GearMeshDesignAnalysis(_945.AbstractGearMeshAnalysis):
    '''GearMeshDesignAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_DESIGN_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshDesignAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_a(self) -> '_947.GearDesignAnalysis':
        '''GearDesignAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_947.GearDesignAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_manufacturing_config(self) -> '_395.CylindricalGearManufacturingConfig':
        '''CylindricalGearManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _395.CylindricalGearManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_395.CylindricalGearManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_manufactured_gear_duty_cycle(self) -> '_399.CylindricalManufacturedGearDutyCycle':
        '''CylindricalManufacturedGearDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _399.CylindricalManufacturedGearDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalManufacturedGearDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_399.CylindricalManufacturedGearDutyCycle)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_manufactured_gear_load_case(self) -> '_400.CylindricalManufacturedGearLoadCase':
        '''CylindricalManufacturedGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _400.CylindricalManufacturedGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalManufacturedGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_400.CylindricalManufacturedGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_manufacturing_analysis(self) -> '_557.ConicalGearManufacturingAnalysis':
        '''ConicalGearManufacturingAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _557.ConicalGearManufacturingAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearManufacturingAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_557.ConicalGearManufacturingAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_manufacturing_config(self) -> '_558.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _558.ConicalGearManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_558.ConicalGearManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_micro_geometry_config(self) -> '_559.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _559.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_559.ConicalGearMicroGeometryConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_micro_geometry_config_base(self) -> '_560.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _560.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_560.ConicalGearMicroGeometryConfigBase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_pinion_manufacturing_config(self) -> '_570.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _570.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_570.ConicalPinionManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_pinion_micro_geometry_config(self) -> '_571.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _571.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_571.ConicalPinionMicroGeometryConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_wheel_manufacturing_config(self) -> '_576.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _576.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_576.ConicalWheelManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_load_distribution_analysis(self) -> '_613.GearLoadDistributionAnalysis':
        '''GearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _613.GearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_613.GearLoadDistributionAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_load_distribution_analysis(self) -> '_627.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _627.CylindricalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_627.CylindricalGearLoadDistributionAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_load_distribution_analysis(self) -> '_638.ConicalGearLoadDistributionAnalysis':
        '''ConicalGearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _638.ConicalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_638.ConicalGearLoadDistributionAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_load_case_base(self) -> '_644.GearLoadCaseBase':
        '''GearLoadCaseBase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _644.GearLoadCaseBase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearLoadCaseBase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_644.GearLoadCaseBase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_worm_gear_load_case(self) -> '_647.WormGearLoadCase':
        '''WormGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _647.WormGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_647.WormGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_load_case(self) -> '_650.FaceGearLoadCase':
        '''FaceGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _650.FaceGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_650.FaceGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_load_case(self) -> '_653.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _653.CylindricalGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_653.CylindricalGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_load_case(self) -> '_656.ConicalGearLoadCase':
        '''ConicalGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _656.ConicalGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_656.ConicalGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_concept_gear_load_case(self) -> '_659.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _659.ConceptGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConceptGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_659.ConceptGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_bevel_load_case(self) -> '_662.BevelLoadCase':
        '''BevelLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _662.BevelLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_662.BevelLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_tiff_analysis(self) -> '_667.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _667.CylindricalGearTIFFAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearTIFFAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_667.CylindricalGearTIFFAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_micro_geometry(self) -> '_756.FaceGearMicroGeometry':
        '''FaceGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _756.FaceGearMicroGeometry.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_756.FaceGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_micro_geometry(self) -> '_844.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _844.CylindricalGearMicroGeometry.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_844.CylindricalGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_micro_geometry_duty_cycle(self) -> '_845.CylindricalGearMicroGeometryDutyCycle':
        '''CylindricalGearMicroGeometryDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _845.CylindricalGearMicroGeometryDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearMicroGeometryDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_845.CylindricalGearMicroGeometryDutyCycle)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_fe_model(self) -> '_929.GearFEModel':
        '''GearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _929.GearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_929.GearFEModel)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_fe_model(self) -> '_933.CylindricalGearFEModel':
        '''CylindricalGearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _933.CylindricalGearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_933.CylindricalGearFEModel)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_fe_model(self) -> '_936.ConicalGearFEModel':
        '''ConicalGearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _936.ConicalGearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_936.ConicalGearFEModel)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_implementation_analysis(self) -> '_948.GearImplementationAnalysis':
        '''GearImplementationAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _948.GearImplementationAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_948.GearImplementationAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_implementation_analysis_duty_cycle(self) -> '_949.GearImplementationAnalysisDutyCycle':
        '''GearImplementationAnalysisDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _949.GearImplementationAnalysisDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationAnalysisDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_949.GearImplementationAnalysisDutyCycle)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_implementation_detail(self) -> '_950.GearImplementationDetail':
        '''GearImplementationDetail: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _950.GearImplementationDetail.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationDetail. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_950.GearImplementationDetail)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_b(self) -> '_947.GearDesignAnalysis':
        '''GearDesignAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_947.GearDesignAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_manufacturing_config(self) -> '_395.CylindricalGearManufacturingConfig':
        '''CylindricalGearManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _395.CylindricalGearManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_395.CylindricalGearManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_manufactured_gear_duty_cycle(self) -> '_399.CylindricalManufacturedGearDutyCycle':
        '''CylindricalManufacturedGearDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _399.CylindricalManufacturedGearDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalManufacturedGearDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_399.CylindricalManufacturedGearDutyCycle)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_manufactured_gear_load_case(self) -> '_400.CylindricalManufacturedGearLoadCase':
        '''CylindricalManufacturedGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _400.CylindricalManufacturedGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalManufacturedGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_400.CylindricalManufacturedGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_manufacturing_analysis(self) -> '_557.ConicalGearManufacturingAnalysis':
        '''ConicalGearManufacturingAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _557.ConicalGearManufacturingAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearManufacturingAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_557.ConicalGearManufacturingAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_manufacturing_config(self) -> '_558.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _558.ConicalGearManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_558.ConicalGearManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_micro_geometry_config(self) -> '_559.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _559.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_559.ConicalGearMicroGeometryConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_micro_geometry_config_base(self) -> '_560.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _560.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_560.ConicalGearMicroGeometryConfigBase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_pinion_manufacturing_config(self) -> '_570.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _570.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_570.ConicalPinionManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_pinion_micro_geometry_config(self) -> '_571.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _571.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_571.ConicalPinionMicroGeometryConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_wheel_manufacturing_config(self) -> '_576.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _576.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_576.ConicalWheelManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_load_distribution_analysis(self) -> '_613.GearLoadDistributionAnalysis':
        '''GearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _613.GearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_613.GearLoadDistributionAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_load_distribution_analysis(self) -> '_627.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _627.CylindricalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_627.CylindricalGearLoadDistributionAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_load_distribution_analysis(self) -> '_638.ConicalGearLoadDistributionAnalysis':
        '''ConicalGearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _638.ConicalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_638.ConicalGearLoadDistributionAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_load_case_base(self) -> '_644.GearLoadCaseBase':
        '''GearLoadCaseBase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _644.GearLoadCaseBase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearLoadCaseBase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_644.GearLoadCaseBase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_worm_gear_load_case(self) -> '_647.WormGearLoadCase':
        '''WormGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _647.WormGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_647.WormGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_load_case(self) -> '_650.FaceGearLoadCase':
        '''FaceGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _650.FaceGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_650.FaceGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_load_case(self) -> '_653.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _653.CylindricalGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_653.CylindricalGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_load_case(self) -> '_656.ConicalGearLoadCase':
        '''ConicalGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _656.ConicalGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_656.ConicalGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_concept_gear_load_case(self) -> '_659.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _659.ConceptGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConceptGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_659.ConceptGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_bevel_load_case(self) -> '_662.BevelLoadCase':
        '''BevelLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _662.BevelLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_662.BevelLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_tiff_analysis(self) -> '_667.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _667.CylindricalGearTIFFAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearTIFFAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_667.CylindricalGearTIFFAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_micro_geometry(self) -> '_756.FaceGearMicroGeometry':
        '''FaceGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _756.FaceGearMicroGeometry.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_756.FaceGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_micro_geometry(self) -> '_844.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _844.CylindricalGearMicroGeometry.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_844.CylindricalGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_micro_geometry_duty_cycle(self) -> '_845.CylindricalGearMicroGeometryDutyCycle':
        '''CylindricalGearMicroGeometryDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _845.CylindricalGearMicroGeometryDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearMicroGeometryDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_845.CylindricalGearMicroGeometryDutyCycle)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_fe_model(self) -> '_929.GearFEModel':
        '''GearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _929.GearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_929.GearFEModel)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_fe_model(self) -> '_933.CylindricalGearFEModel':
        '''CylindricalGearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _933.CylindricalGearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_933.CylindricalGearFEModel)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_fe_model(self) -> '_936.ConicalGearFEModel':
        '''ConicalGearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _936.ConicalGearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_936.ConicalGearFEModel)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_implementation_analysis(self) -> '_948.GearImplementationAnalysis':
        '''GearImplementationAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _948.GearImplementationAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_948.GearImplementationAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_implementation_analysis_duty_cycle(self) -> '_949.GearImplementationAnalysisDutyCycle':
        '''GearImplementationAnalysisDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _949.GearImplementationAnalysisDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationAnalysisDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_949.GearImplementationAnalysisDutyCycle)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_implementation_detail(self) -> '_950.GearImplementationDetail':
        '''GearImplementationDetail: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _950.GearImplementationDetail.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationDetail. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_950.GearImplementationDetail)(self.wrapped.GearB) if self.wrapped.GearB else None
