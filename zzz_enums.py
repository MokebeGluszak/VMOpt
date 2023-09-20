from enum import Enum


class BehaviourIfNotExists(Enum):
    Create = "Create"
    Break = "Break"


class Supplier(Enum):
    TVP = "TVP"
    TVN = "TVN"
    POLSAT = "Polsat"

class BookingFile(Enum):
    PolsatWrongDates = r"C:\Users\macie\PycharmProjects\VMOpt\Source\Orders\2 booking polsat wrong dates.xlsx"
    PolsatFake = r"C:\Users\macie\PycharmProjects\VMOpt\Source\Orders\2 booking polsat fake.xlsx"
    PolsatOkRatecard = r"C:\Users\macie\PycharmProjects\VMOpt\Source\Orders\bookings\polsat\ABBOTT_LABORATORIES_POLAND_SP_Z_O_O - Polsat cennik(3).xlsx"

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


class FreeTimesQuality(Enum):
    OK = "OK"


class OptimisationDefType(Enum):
    OK = r"C:\Users\macie\PycharmProjects\VMOpt\Source\optimisation json ok.json"
    INVALID_ITEMS = (r"C:\Users\macie\PycharmProjects\VMOpt\Source\optimisationJson ok.txttt")


class ScheduleType(Enum):
    OK9 = r"C:\Users\macie\PycharmProjects\VMOpt\Source\Orders\schedule\OK last 6 weeks tg01 All 30-64 RFP OOH after export.xlsx"
    OK9_small = r"C:\Users\macie\PycharmProjects\VMOpt\Source\Orders\schedule\OK last 6 weeks tg01 All 30-64 RFP OOH small after export.xlsx"
    # ILLEGAL_CHANNELS = "Illegal channels"
    # OK_4CHANNELS_1WANTED = "OK_4channels_1wanted"

class ScheduleLoadMode(Enum):
    Optimisation = "Optimisation"
    Booking = "Booking"
class ExceptionType(Enum):
    MERGER_GENERIC = "There are unjoined values \n _UnjoinedValues_ \n in merge operation \n _Caption_  \n that are absent in schedule:"
    MERGER_ILLEGAL_CHANNELS_IN_BOOKING = (
        "Unknown channels \n _UnjoinedValues_ \n in imported booking'"
    )
    MERGER_ILLEGAL_CHANNELS_IN_SCHEDULE = (
        "Unknown channels \n _UnjoinedValues_ \n in imported schedule'"
    )
    MERGER_ABSENT_CHANNELS = (
        "There are channels in booking that are absent in schedule\n _UnjoinedValues_:"
    )


class QuantityConstraintType(Enum):
    CHANNEL = "channel"
    CHANNELGROUP = "channelGroup"
    TIMEBAND = "timeband"
    WEEK = "week"


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


class DataType(Enum):
    INT = "int"
    FlOAT = "float"
    STR = "str"
    BOOL = "bool"
    DATETIME64 = "datetime64[s]"
    DATE = "date"
    TIME = "time"


class OptimisationStep(Enum):
    Step1ShrConstraints = "Step1FulfillConstraints"
    Step2Total = "Step2Total"
    Step3Decrement = "Step3Decrement"


class BlockOperation(Enum):
    PickUp = "PickUp"
    Drop = "Drop"

class RepetitionType(Enum):
    BeforeWeekly= "ProgBefore/Weekly"
    AfterWeekly= "ProgAfter/Weekly"
    BeforeTotal= "ProgBefore/Total"
    AfterTotal= "ProgAfter/Total"