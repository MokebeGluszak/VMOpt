import dataclasses

import c_matching_algorithm as m
from classes.booking import Booking
from classes.booking_report import BookingReport
from classes.free_times import FreeTimes
from classes.schedule import Schedule
from d_booking_algorithm import get_booking_report
from zzz_ordersTools import check_time_space_consistency


@dataclasses.dataclass
class MatchingProcessor:
    schedule: Schedule
    booking: Booking
    free_times: FreeTimes
    _booking_report: BookingReport = None
    _booking: Booking = None

    def process_booking(
        self,
    ) -> None:


        check_time_space_consistency(self.booking.df, self.schedule.df, "Booking")
        m.match_channel_breaks_step1_id(self.booking.get_unmatched_channel_breaks, self.schedule.schedule_breaks)
        m.match_channel_breaks_step2_timebands(self.booking.get_unmatched_channel_breaks, self.schedule.get_timebands_dict)
        self.booking_report = get_booking_report(self.schedule.schedule_breaks, self.booking.channel_breaks, self.schedule.get_subcampaigns_dict)  # modyfikuje schedule brejki

        # t.export_df(schedule.df, "1a schedule_processed")
        # t.export_df(booking.df, "1b booking_processed")
        # # t.export_df(df_matching, "2 matching")
        # df_channelBreaks = booking.get_df()
        # t.export_df(df_channelBreaks, "channel breaks")
        # t.export_df(df_channelsMapping, "channels_mapping")

    def process_free_times(self)-> None:
        pass

    @property
    def booking_report(self) -> BookingReport:
        return self._booking_report

    @booking_report.setter
    def booking_report(self, value: BookingReport) -> None:
        self._booking_report = value