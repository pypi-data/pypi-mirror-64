#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "Nima TRAORE"

from datetime import datetime
import pytest

from sitools2.clients.sdo_data import SdoData


class TestSdoData:
    """Tests the class SdoData methods.

    """
    def setup_method(self):
        """Setup method"""
        self.data = {'get': 'http://sdo.ias.u-psud.fr/SDO/...1230681651',
                     'recnum': 171963897,
                     'sunum': 775321065,
                     'series_name': 'aia.lev1',
                     'date__obs': datetime(2016, 1, 1, 0, 0, 13, 627),
                     'wavelnth': 335, 'ias_location': '/SUM12/D775321065',
                     'exptime': 2.9008089999999997,
                     't_rec_index': 1230681651,
                     'ias_path': 'http://idoc-medoc.ias.u-psud.fr//s.../S00000'}
        self.sdd = SdoData(self.data)

    def test_compute_attributes(self):
        """Tests compute_attributes()"""
        data = self.data
        sdd = self.sdd
        assert data['get'] == sdd.url
        assert data['recnum'] == sdd.recnum
        assert data['sunum'] == sdd.sunum
        assert data['series_name'] == sdd.series_name
        assert data['date__obs'] == sdd.date_obs
        assert data['wavelnth'] == sdd.wave
        assert data['exptime'] == sdd.exptime
        assert data['t_rec_index'] == sdd.t_rec_index
        assert data['ias_location'] == sdd.ias_location

    def test_get_ias_path(self):
        """Tests get_ias_path()"""
        sdd = self.sdd
        assert 'http://idoc-medoc.ias.u-psud.fr//s.../S00000' == \
            sdd.get_ias_path()

    def test_get_filename_and_create_target_dir(self):
        """Tests get_filename_and_create_target_dir()"""
        sdd = self.sdd
        assert 'aia.lev1_335A_2016-01-01T00-00-13_171963897.' == \
               sdd.get_filename_and_create_target_dir(None, None)

    def test_scan_segment(self):
        """Tests scan_segment()"""
        sdd = self.sdd
        assert (['image_lev1'],
                [],
                'http://sdo.ias.u-psud.fr/SDO/...1230681651;segment=image_lev1') == \
            sdd.scan_segment(None, None, None)

    def test_is_keywords(self):
        """Tests is_keywords()"""
        sdd = self.sdd
        with pytest.raises(ValueError):
            assert sdd.is_keywords('')
        with pytest.raises(TypeError):
            assert sdd.is_keywords('QUALITY')
        assert sdd.is_keywords(['QUALITY']) is True
