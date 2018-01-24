#!/usr/bin/env python
# -*- coding: utf-8 -*-

import humidity_converter as hc

# RH, temperature in C, pressure in hPa
h = hc.humidity_converter(50, 25, 1013.25)
h.prettify_print()
