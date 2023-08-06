# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 09:55:26 2020

@author: vincent
"""

import unittest
import datetime as dt

from std_date_tools import is_date_dst_october, is_date_dst_march, get_dst_dates_oct_in_range, is_date_dst, get_num_ptus_on_date

class Test_date_stuff(unittest.TestCase):
    def test_num_ptus_normal_date(self):
        self.assertEqual(get_num_ptus_on_date(dt.datetime(2020,2,11)),96)

    def test_num_ptus_normal_date_with_tz(self):
        self.assertEqual(get_num_ptus_on_date(dt.datetime(2020,2,11),'Europe/Amsterdam'),96)


    def test_num_ptus_normal_date_with_utc(self):
        self.assertEqual(get_num_ptus_on_date(dt.datetime(2020,2,11),'UTC'),96)

    def test_num_ptus_dst_october(self):
        self.assertEqual(get_num_ptus_on_date(dt.datetime(2019,10,27)),100)

    def test_num_ptus_dst_october_utc(self):
        self.assertEqual(get_num_ptus_on_date(dt.datetime(2019,10,27),'UTC'),96)

    def test_num_ptus_dst_march(self):
        self.assertEqual(get_num_ptus_on_date(dt.datetime(2020,3,29)),92)

    def test_is_date_dst_october_true(self):
        self.assertEqual(is_date_dst_october(dt.datetime(2019,10,27)),True)

    def test_is_date_dst_october_false(self):
        self.assertEqual(is_date_dst_october(dt.datetime(2019,10,28)),False)

    def test_is_date_dst_march_true(self):
        self.assertEqual(is_date_dst_march(dt.datetime(2020,3,29)),True)

    def test_is_date_dst_march_false(self):
        self.assertEqual(is_date_dst_march(dt.datetime(2020,3,28)),False)


    def test_get_dst_dates_oct_in_range1(self):
        ll = [dt.datetime(2019,10,27),dt.datetime(2020,10,25)]
        self.assertEqual(get_dst_dates_oct_in_range(dt.date(2019,1,1), dt.date(2020,12,31)),ll)

    def test_is_date_dst(self):
        self.assertEqual(is_date_dst_march(dt.datetime(2020,3,29)),True)

    def test_is_date_dst1(self):
        self.assertEqual(is_date_dst(dt.datetime(2020,3,30)),False)

    def test_is_date_dst2(self):
        self.assertEqual(is_date_dst(dt.datetime(2020,12,5)),False)

if __name__ == '__main__':
    unittest.main()
