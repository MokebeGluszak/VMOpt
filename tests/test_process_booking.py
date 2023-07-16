import os
from unittest import TestCase

from a_main import process_booking

from classes.exceptions import *
from zzz_enums import *


class TestProcessBooking(TestCase):

    def test_valid(self):
        result_schedule_path = process_booking(Supplier.POLSAT, BookingQuality.OK, ScheduleType.OK_4CHANNELS_CLEAR)
        self.assertTrue(os.path.exists(result_schedule_path))


    def test_absent_channels_in_schedule(self):

        try:
            process_booking(Supplier.POLSAT, BookingQuality.ABSENT_CHANNELS, ScheduleType.OK_4CHANNELS_CLEAR)
        except MergerException as e:
            self.assertEqual(ExceptionType.MERGER_ABSENT_CHANNELS, e.exception_type)

    def test_illegal_channels_in_booking(self):

        try:
            process_booking(Supplier.POLSAT, BookingQuality.ILLEGAL_CHANNELS, ScheduleType.OK_4CHANNELS_CLEAR)
        except MergerException as e:
            self.assertEqual(ExceptionType.MERGER_ILLEGAL_CHANNELS_IN_BOOKING, e.exception_type)

    def test_illegal_channels_in_schedule(self):

        try:
            process_booking(Supplier.POLSAT, BookingQuality.OK, ScheduleType.ILLEGAL_CHANNELS)
        except MergerException as e:
            self.assertEqual(ExceptionType.MERGER_ILLEGAL_CHANNELS_IN_SCHEDULE, e.exception_type)


    def test_illegal(self):
        pass