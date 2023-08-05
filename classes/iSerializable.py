import abc

from zzz_enums import ExportFormat


class iSerializable(abc.ABC):

    @abc.abstractmethod
    def serialize(self, export_format:ExportFormat):
        """zamienia obiekt na dict"""
