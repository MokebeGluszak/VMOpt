from datetime import datetime

from zzz_enums import *

FAKE_DATE = datetime(2005, 4, 2, 21, 37, 0)
FAKE_INT = 666
PATH_JSON_COPY_INDEXES = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\ConfigObjectsJsons\json copy lengths.txt"
PATH_JSON_CHANNELS = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\ConfigObjectsJsons\json channels.txt"
PATH_JSON_COPYLENGTHS = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\ConfigObjectsJsons\json copy lengths.txt"
PATH_DICT_SUBCAMPAIGNS = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\dicts\dict subcampaignss.txt"
PATH_DICT_FREE_TIME_LENGHTS = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\dicts\dict free time lenghts.txt"
PATH_DICT_FREE_TIME_CHANNELS = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\dicts\dict free time channels.txt"
PATH_ORDER_TEMPLATE_POLSAT = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\OrderTemplates\OrderTemplatePolsat.xlsx"
PATH_SLOWNIKI_EXISTING_DICTS_FOLDER = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\Slowniki\ExistingDicts"
PATH_SLOWNIKI_MOD_VALUES_FOLDER = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\Slowniki\ModValuesSets"
PODEJRZANY_BLOK_ID:int = 15107428739
ENCODING = "utf-8"

def get_path_schedule(schedule_type: ScheduleType) -> str:
    path: str
    if schedule_type == ScheduleType.OK_4CHANNELS_CLEAR:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1 schedule 2022-10-06 112529 Schedule czysta.txt"
    elif schedule_type == ScheduleType.ILLEGAL_CHANNELS:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1a schedule 2022-10-06 112529 Schedule czysta - wrong channels.txt"
    elif schedule_type == ScheduleType.OK_4CHANNELS_1WANTED:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1b schedule 2022-10-06 112529 Schedule wanted.txt"

    else:
        raise ValueError("Wrong schedule type")

    return path
