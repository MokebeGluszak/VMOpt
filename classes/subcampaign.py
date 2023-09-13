from dataclasses import dataclass


@dataclass
class Subcampaign():
    id : int
    name : str
    length: int
    @property
    def get_hash(self):
        hash = "_".join([str(self.id), self.name, str(self.length)])
        return hash
