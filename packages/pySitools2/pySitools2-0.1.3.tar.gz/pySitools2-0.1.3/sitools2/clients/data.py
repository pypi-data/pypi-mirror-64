#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Nima TRAORE"

from future.utils import viewitems


class Data:
    """Class Data.

    Data is designed to be a parent class for clients data objects
    (like GaiaData, SdoData classes...)

    Attributes defined here:
        pass

    Methods defined here:
        check_kwargs(): initialize some attributes provided in args

    """
    def __init__(self):
        """Constructor of the class Data"""
        pass

    def check_kwargs(self, params, kwargs):
        """Initializes some attributes provided in kwargs.

        When a dictionary is provided as named parameters to the
        function, the method checks if each value of the given
        dictionary is in an allowed parameters list, then initializes
        an empty dictionary with allowed attributes.

        Args:
            params: list of allowed parameters to checked
            kwargs: a dictionary

        Returns:
            dictionary

        """
        kwg_dict = {}
        for key, value in viewitems(kwargs):
            if key not in params:
                error_msg = ("Error in search:\n%s entry for the "
                             "function is not allowed\n" % key)
                raise ValueError(error_msg)
            else:
                kwg_dict[key.lower()] = value

        return kwg_dict
