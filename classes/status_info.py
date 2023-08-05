from classes.iSerializable import iSerializable
from zzz_enums import *


class StatusInfo(iSerializable):
    def __init__(
            self,
            subcampaign_id: int,
            origin: Origin,
            is_booked: bool
    ):
        self.subcampaign_id = subcampaign_id
        self.origin = origin
        self.is_booked = is_booked

    @property
    def get_is_wanted(self)->bool:
        return self.subcampaign_id>=0


    def serialize(self, export_format:ExportFormat)->dict:
        return {
            'subcampaign': self.subcampaign_id,
            'origin': self.origin.value,
            'is_booked': self.is_booked
        }

    @property
    def get_wantedness(self)->str:
        # WantedBy(Optimizer, Subcampaign(0))
        if self.get_is_wanted:
            my_str = f'WantedBy({self.origin.value}, Subcampaign({self.subcampaign_id}))'
        else:
            my_str = 'NotWanted'

        return my_str

    @property
    def get_bookedness(self)->str:

        # Booked(Subcampaign(0))
        # NotBooked

        if self.is_booked:
            my_str = f'Booked(Subcampaign({self.subcampaign_id}))'
        else:
            my_str = 'NotBooked'

        return my_str