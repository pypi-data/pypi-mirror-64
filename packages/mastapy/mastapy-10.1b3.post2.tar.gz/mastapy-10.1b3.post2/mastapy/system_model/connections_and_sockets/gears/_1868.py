'''_1868.py

WormGearMesh
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.worm import _713
from mastapy.system_model.connections_and_sockets.gears import _1852
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMesh',)


class WormGearMesh(_1852.GearMesh):
    '''WormGearMesh

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMesh.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def meshing_angle(self) -> 'float':
        '''float: 'MeshingAngle' is the original name of this property.'''

        return self.wrapped.MeshingAngle

    @meshing_angle.setter
    def meshing_angle(self, value: 'float'):
        self.wrapped.MeshingAngle = float(value) if value else 0.0

    @property
    def worm_gear_mesh_design(self) -> '_713.WormGearMeshDesign':
        '''WormGearMeshDesign: 'WormGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_713.WormGearMeshDesign)(self.wrapped.WormGearMeshDesign) if self.wrapped.WormGearMeshDesign else None
