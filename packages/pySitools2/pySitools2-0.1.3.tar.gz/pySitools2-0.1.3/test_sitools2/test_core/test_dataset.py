#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Nima TRAORE"

from sitools2.clients import medoc_config as cfg
from sitools2.core.dataset import Dataset


class TestDataset:
    """Tests the class Dataset methods.

    """
    def setup_method(self):
        """Method called before one of the current class tests."""
        self.ds = Dataset(cfg.SITOOLS2_URL+'/'+cfg.AIA_LEV1_DATASET_ID)

    def test_dataset_attributes(self):
        """Tests the class Dataset attributes after initialisation."""
        assert 'aia.lev1' == self.ds.name
        assert 'access to all metadata info' == self.ds.description
        assert 188 == len(self.ds.fields_list)
        assert 188 == len(self.ds.fields_dict)
        assert 188 == len(self.ds.filter_list)
        assert 188 == len(self.ds.sort_list)
        assert 21 == len(self.ds.resources_target)

    def test_optimize_operation(self):
        """Tests optimize_operation()"""
        assert 'GTE' == self.ds.optimize_operation('GE')
        assert 'LTE' == self.ds.optimize_operation('LE')
