#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Nima TRAORE"

from sitools2.clients import medoc_config as cfg
from sitools2.clients.client_medoc import ClientMedoc
from sitools2.clients.euvsyn_data import EuvsynData


class EuvsynClientMedoc(ClientMedoc):
    """Class giving easy way to interrogate IDOC/MEDOC sitools interface.

    EuvsynClientMedoc inherits from the ClientMedoc class which provides
    some generic methods to interact with sitools interface:
        - search() method is called to recover the data list (the list
            of output data is defined in the configuration file
            as EUVSYN_OUTPUT_OPTION_LIST: each element of the list can be
            commented or uncommented in order to customize the output)
        - get() method is called to download data files as TAR or ZIP

    Attributes defined here:
        dataset_data_class: name of the class defining the client data
        dataset_id: ID of the IDOC/MEDOC client
        dataset_uri: dataset URI
        plugin_id: client plugin ID to be used for downloading
        primary_key: dataset primary key

    Methods defined here:
        get_class_name(): return the class name
        get_item_file(): downloads files for each dataset object

    Examples:
        >>> from sitools2 import EuvsynClientMedoc
        >>> from datetime import datetime
        >>> d1 = datetime(2009, 7, 6, 0, 0, 0)
        >>> d2 = datetime(2009, 7, 10, 0, 0, 0)
        >>> euvsyn = EuvsynClientMedoc()
        >>> euvsyn_data_list = euvsyn.search(DATES=[d1, d2], NB_RES_MAX=10)
        >>> euvsyn.get(DATA_LIST=euvsyn_data_list, TARGET_DIR='results', DOWNLOAD_TYPE='TAR')

    """
    def __init__(self):
        """Constructor of the class EuvsynClientMedoc."""
        ClientMedoc.__init__(self)
        self.dataset_uri = cfg.EUV_SYN_DATASET_ID
        self.dataset_id = "EUVSYN"
        self.dataset_data_class = EuvsynData
        self.primary_key = 'index'
        self.plugin_id = "pluginEITSYNtar"

    def get_class_name(self):
        """Return the class name in string format."""
        return 'EuvsynClientMedoc'

    def get_item_file(self, data_list=None, target_dir=None, **kwargs):
        pass
