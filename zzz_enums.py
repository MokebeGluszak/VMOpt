from enum import Enum

class BehaviourIfNotExists(Enum):
    Create = "Create"
    Break  = "Break"

class Supplier(Enum):
    TVP = "TVP"
    TVN = "TVN"
    POLSAT = "Polsat"


class MatchLevel(Enum):
    NO_TIMEBAND = "No timeband"
    NO_MATCH = "No match"
    TIME = "Time"
    RATECARD = "Ratecard"
    ID = "ID"


class Origin(Enum):
    NotWanted = "NotWanted"
    Optimizer = "Optimizer"
    Manual = "Manual"
    Station = "Station"

    @classmethod
    def get_from_str(cls, my_str):
        for origin in cls:
            if origin.value == my_str:
                return origin
        raise ValueError("No such origin: " + my_str)


class ExportFormat(Enum):
    ChannelBreak = "ChannelBreak"
    ScheduleBreak_minerwa = "ScheduleBreak_minerwa"
    ScheduleBreak_rozkminki = "ScheduleBreak_rozkminki"
    Irrelevant = "Irrelevant"


class BookingQuality(Enum):
    OK = "OK"
    ABSENT_CHANNELS = "Absent channels"
    ILLEGAL_CHANNELS = "Illegal channels"
    FUCKED_UP_DATES = "Fucked up dates"


class FreeTimesQuality(Enum):
    OK = "OK"


class ScheduleType(Enum):
    OK_4CHANNELS_CLEAR = "OK_4channels"
    ILLEGAL_CHANNELS = "Illegal channels"
    OK_4CHANNELS_1WANTED = "OK_4channels_1wanted"


class ExceptionType(Enum):
    MERGER_GENERIC = "There are unjoined values \n _UnjoinedValues_ \n in merge operation \n _Caption_  \n that are absent in schedule:"
    MERGER_ILLEGAL_CHANNELS_IN_BOOKING = "Unknown channels \n _UnjoinedValues_ \n in imported booking'"
    MERGER_ILLEGAL_CHANNELS_IN_SCHEDULE = "Unknown channels \n _UnjoinedValues_ \n in imported schedule'"
    MERGER_ABSENT_CHANNELS = "There are channels in booking that are absent in schedule\n _UnjoinedValues_:"


class DfProcessorType(Enum):
    FREE_TIMES_POLSAT = "Free times Polsat"
    HISTORY_ORG = "History"
    BOOKING_POLSAT = "Booking Polsat"
    SCHEDULE = "SCHEDULE"
    SCHEDULE_INFO = "Schedule info"


class CannonColumnsSet(Enum):
    DoNotCheck = "DoNotCheck"
    BookingProcessed = "BookingProcessed"
    Matching = "Matching"
    ScheduleProcessedFull = "ScheduleProcessedFull"
    ScheduleMatching = "ScheduleMatching"
    ScheduleOrg = "ScheduleOrg"


class FileType(Enum):
    XLSX = ".xlsx"
    CSV = ".csv"


class SlownikType(Enum):
    CHANNELS = "channels"
    SUBCAMPAIGNS = "subcampaigns"
    WOLNE_CZASY_LENGTHS = "wolne_czasy_lengths"
