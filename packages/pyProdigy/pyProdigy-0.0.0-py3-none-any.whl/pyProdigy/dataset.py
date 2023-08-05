#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

from .par_const import pbband, get_goodpix

class DataSet(object):
    """
    DataSet class contains the data descriptor/definition and utilities to manipulate them
    """

    def __init__(self, dict):
        """
        This class contains the dataset parameters and has a set of methods to
        set up processing parameters

        :param dict: dictionary of parameters
        """

        self.ovis = dict['ovis']
        self.datacolumn = dict['datacolumn']
        self.resolution = dict['resolution']
        self.band = dict['band']
        self.field = dict['field']
        self.all_spw = dict['all_spw']
        self.ch_spw = dict['ch_spw']
        self.bw_spw = dict['bw_spw']
        self.pol = dict['pol']

        # Field of view (rough estimate per band) in arcsec
        self.fov = pbband[self.band]

        # set the full spw string
        self.all_spw_string = self._set_all_spw_string()

        # continuum spws defines?
        self.has_cont_spw = False

    def _set_all_spw_string(self):
        """
        sets the spw strings for all spw and for continuum
        :return: string with all spw and string of spw for continuum
        """

        for ii in range(len(self.all_spw)):
            if ii == 0:
                allspw = self.all_spw[ii]
            else:
                allspw = allspw+','+self.all_spw[ii]

        return allspw

    def get_cont_spw_string(self, min_cont_bw=None):
        """
        returns the string containing the continuum spw
        if min_cont_bw is set, returns only the spw that are wider than the min_cont_bw (MHz)

        :param min_cont_bw: minimum bandwidth for spw, in MHz
        :return: the string of continuum channels
        """

        if min_cont_bw:
            nn = 0
            for ii in range(len(self.all_spw)):
                if self.bw_spw[ii] > min_cont_bw:
                    if nn == 0:
                        self.cont_spw_string = self.all_spw[ii]
                        self.cont_spw_elements = [ii]
                    else:
                        self.cont_spw_string = self.cont_spw_string+','+self.all_spw[ii]
                        self.cont_spw_elements.append(ii)
                        self.cont_spw_elements = []
                    nn += 1
            if nn == 0:
                #print("Warning; no spectral windows are broader than {0}, cont_spw is empty!".format(self.min_cont_bw))
                self.cont_spw_string = ''
        else:
            self.cont_spw_string = self.all_spw_string
            self.cont_spw_elements = range(len(self.all_spw))

        self.has_cont_spw = True
        return self.cont_spw_string

    def get_cont_chavg_width(self, max_ch_width=117.):
        """
        Returns the number of channels to average per spw
        :param max_ch_width: max continuum bandwidth per channel
        :return:
        """

        if self.has_cont_spw:
            self.cont_chavg_width = []
            for ii in self.cont_spw_elements:
                self.cont_chavg_width.append(int(round(self.ch_spw[ii] / max((self.bw_spw[ii] / max_ch_width), 1.0))))
        else:
            print("Error: you first need to define the continuum spw with cont_spw_string()")
            self.cont_chavg_width = [1]

        return self.cont_chavg_width

    def get_cell_imsize(self,ffov=1.0,nsamp=4.):
        """
        defines the imsize and pixel size

        :param ffov: fraction of the field of view to be covered
        :param nsamp: number of pixels per resolution element
        :return:
        """

        pix = self.resolution/float(nsamp)
        minpix = int(self.fov*ffov/pix)+1
        self.imsize  = get_goodpix(minpix)
        self.cell = '{0:5.3f}arcsec'.format(pix)

