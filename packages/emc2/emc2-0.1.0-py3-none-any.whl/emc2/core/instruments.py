"""
=====================
emc2.core.instruments
=====================

This module stores example instruments.
"""
import numpy as np
import os

from .instrument import Instrument, ureg, quantity
from ..io import load_mie_file


class HSRL(Instrument):
    def __init__(self):
        """
        This stores the information for the High Resolution Spectral Lidar.
        """
        super().__init__(wavelength=0.532 * ureg.micrometer)
        self.instrument_class = "lidar"
        self.instrument_str = "HSRL"
        self.ext_OD = 4
        self.K_w = np.nan
        self.eps_liq = (1.337273 + 1.7570744e-9j)**2
        self.pt = np.nan
        self.theta = np.nan
        self.gain = np.nan
        self.Z_min_1km = np.nan
        self.lr = np.nan
        self.pr_noise_ge = np.nan
        self.pr_noise_md = np.nan
        self.tau_ge = np.nan
        self.tau_md = np.nan

        # Load mie tables
        data_path = os.path.join(os.path.dirname(__file__), 'mie_tables')
        self.mie_table["cl"] = load_mie_file(data_path + "/MieHSRL_liq.dat")
        self.mie_table["pl"] = load_mie_file(data_path + "/MieHSRL_liq.dat")
        self.mie_table["ci"] = load_mie_file(data_path + "/MieHSRL_ci.dat")
        self.mie_table["pi"] = load_mie_file(data_path + "/MieHSRL_pi.dat")


class KAZR(Instrument):
    def __init__(self, site):
        """
        This stores the information for the KAZR.
        """
        super().__init__(frequency=34.860 * ureg.GHz)
        if site.lower() not in ["sgp", "nsa", "awr"]:
            raise ValueError("Site must be one of 'sgp', 'nsa', or 'awr'!")
        self.instrument_class = "radar"
        self.ext_OD = np.nan
        self.K_w = 0.88
        self.eps_liq = (5.489262 + 2.8267679j)**2
        self.pt = 2000.
        if site.lower() == "sgp":
            self.theta = 0.19
        else:
            self.theta = 0.31
        if site.lower() == "sgp":
            self.gain = 10**5.748
            self.Z_min_1km = -51.5
        elif site.lower() == "nsa":
            self.gain = 10**5.337
            self.Z_min_1km = -49.0
        else:
            self.gain = 10**5.273
            self.Z_min_1km = -47.2
        if site.lower() == "nsa":
            self.lr = 10**0.4
            self.pr_noise_ge = 10**-6.85
            self.pr_noise_md = 10**-7.23
            self.tau_ge = 0.3
            self.tau_md = 4.0
        else:
            self.lr = np.nan
            self.pr_noise_ge = np.nan
            self.pr_noise_md = np.nan
            self.tau_ge = np.nan
            self.tau_md = np.nan
        # Load mie tables
        data_path = os.path.join(os.path.dirname(__file__), 'mie_tables')
        self.mie_table["cl"] = load_mie_file(data_path + "/MieKAZR_liq.dat")
        self.mie_table["pl"] = load_mie_file(data_path + "/MieKAZR_liq.dat")
        self.mie_table["ci"] = load_mie_file(data_path + "/MieKAZR_ci.dat")
        self.mie_table["pi"] = load_mie_file(data_path + "/MieKAZR_pi.dat")


class Ten64nm(Instrument):
    def __init__(self):
        """
        This stores the information for the 1064nm Lidar.
        """
        super().__init__(wavelength=1.064 * ureg.micrometer)
        self.instrument_class = "radar"
        self.instrument_name = "1064nm"
        self.ext_OD = 4
        self.K_w = np.nan
        self.eps_liq = (1.320416 + 1.2588968e-6j)**2
        self.pt = np.nan
        self.theta = np.nan
        self.gain = np.nan
        self.Z_min_1km = np.nan
        self.lr = np.nan
        self.pr_noise_ge = np.nan
        self.pr_noise_md = np.nan
        self.tau_ge = np.nan
        self.tau_md = np.nan
        # Load mie tables
        data_path = os.path.join(os.path.dirname(__file__), 'mie_tables')
        self.mie_table["cl"] = load_mie_file(data_path + "/Mie1064nm_liq.dat")
        self.mie_table["pl"] = load_mie_file(data_path + "/Mie1064nm_liq.dat")
        self.mie_table["ci"] = load_mie_file(data_path + "/Mie1064nm_ci.dat")
        self.mie_table["pi"] = load_mie_file(data_path + "/Mie1064nm_pi.dat")
