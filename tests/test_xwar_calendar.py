from unittest import TestCase

import pandas as pd
from pytz import UTC

from trading_calendars.exchange_calendar_xwar import XWARExchangeCalendar

from .test_trading_calendar import ExchangeCalendarTestBase


class XWARCalendarTestCase(ExchangeCalendarTestBase, TestCase):

    answer_key_filename = 'xwar'
    calendar_class = XWARExchangeCalendar

    # The XWAR is open from 9:00AM to 5:00PM.
    MAX_SESSION_HOURS = 8

    # In 2019 in Warsaw, daylight savings began on March 31st and ended on
    # October 27th.
    DAYLIGHT_SAVINGS_DATES = ['2019-04-01', '2019-10-28']

    HAVE_EARLY_CLOSES = False

    def test_regular_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2019-01-01', tz=UTC),  # New Year's Day
            pd.Timestamp('2017-01-06', tz=UTC),  # Epiphany
            pd.Timestamp('2019-04-19', tz=UTC),  # Good Friday
            pd.Timestamp('2019-04-22', tz=UTC),  # Easter Monday
            pd.Timestamp('2019-05-01', tz=UTC),  # Labour Day
            pd.Timestamp('2019-05-03', tz=UTC),  # Constitution Day
            pd.Timestamp('2019-06-20', tz=UTC),  # Corpus Christi
            pd.Timestamp('2019-08-15', tz=UTC),  # Armed Forces Day
            pd.Timestamp('2019-11-01', tz=UTC),  # All Saints' Day
            pd.Timestamp('2019-11-11', tz=UTC),  # Independence Day
            pd.Timestamp('2019-12-24', tz=UTC),  # Christmas Eve
            pd.Timestamp('2019-12-25', tz=UTC),  # Christmas Day
            pd.Timestamp('2019-12-26', tz=UTC),  # Boxing Day
            pd.Timestamp('2019-12-31', tz=UTC),  # New Year's Eve
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_holidays_fall_on_weekend(self):
        all_sessions = self.calendar.all_sessions

        # All holidays falling on a weekend should not be made up, so verify
        # that the surrounding Fridays/Mondays are trading days.
        expected_sessions = [
            # New Year's Eve on a Saturday and New Year's Day on a Sunday.
            pd.Timestamp('2016-12-30', tz=UTC),
            pd.Timestamp('2017-01-02', tz=UTC),
            # Epiphany (January 6th) on a Sunday.
            pd.Timestamp('2019-01-04', tz=UTC),
            pd.Timestamp('2019-01-07', tz=UTC),
            # Labour Day (May 1st) on a Sunday.
            pd.Timestamp('2016-04-29', tz=UTC),
            pd.Timestamp('2016-05-02', tz=UTC),
            # Constitution Day (May 3rd) on a Saturday.
            pd.Timestamp('2014-05-02', tz=UTC),
            pd.Timestamp('2014-05-05', tz=UTC),
            # Armed Forces Day (August 15th) on a Saturday.
            pd.Timestamp('2015-08-14', tz=UTC),
            pd.Timestamp('2015-08-17', tz=UTC),
            # All Saints' Day (November 1st) on a Sunday.
            pd.Timestamp('2015-10-30', tz=UTC),
            pd.Timestamp('2015-11-02', tz=UTC),
            # Independence Day (November 11th) on a Saturday.
            pd.Timestamp('2017-11-10', tz=UTC),
            pd.Timestamp('2017-11-13', tz=UTC),
            # Christmas Eve on a Saturday and Christmas on a Sunday. Note that
            # Monday the 26th is Boxing Day, so check the 27th.
            pd.Timestamp('2016-12-23', tz=UTC),
            pd.Timestamp('2016-12-27', tz=UTC),
        ]

        for session_label in expected_sessions:
            self.assertIn(session_label, all_sessions)

    def test_adhoc_holidays(self):
        all_sessions = self.calendar.all_sessions

        expected_holidays = [
            pd.Timestamp('2005-04-08', tz=UTC),  # Pope's Funeral.
            pd.Timestamp('2007-12-31', tz=UTC),  # New Year's Eve (adhoc).
            pd.Timestamp('2008-05-02', tz=UTC),  # Exchange Holiday.
            pd.Timestamp('2009-01-02', tz=UTC),  # Exchange Holiday.
            pd.Timestamp('2013-04-16', tz=UTC),  # Exchange Holiday.
            pd.Timestamp('2018-01-02', tz=UTC),  # Exchange Holiday.
            pd.Timestamp('2018-11-12', tz=UTC),  # Independence Holiday.
        ]

        for holiday_label in expected_holidays:
            self.assertNotIn(holiday_label, all_sessions)

    def test_new_years_eve(self):
        """
        New Year's Eve did not become a holiday until 2011.
        """
        all_sessions = self.calendar.all_sessions

        self.assertIn(pd.Timestamp('2008-12-31', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2009-12-31', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2010-12-31', tz=UTC), all_sessions)

        for year in range(2011, 2019):
            self.assertNotIn(
                pd.Timestamp('{}-12-31'.format(year), tz=UTC),
                all_sessions,
            )

    def test_epiphany(self):
        """
        The Epiphany did not become a holiday until 2011.
        """
        all_sessions = self.calendar.all_sessions

        self.assertIn(pd.Timestamp('2006-01-06', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2009-01-06', tz=UTC), all_sessions)
        self.assertIn(pd.Timestamp('2010-01-06', tz=UTC), all_sessions)

        for year in range(2011, 2019):
            self.assertNotIn(
                pd.Timestamp('{}-01-06'.format(year), tz=UTC),
                all_sessions,
            )
