import xarray as xr
import numpy as np

from ..core import Instrument, Model
from .attenuation import calc_radar_atm_attenuation
from .psd import calc_mu_lambda
from ..core.instrument import ureg


def calc_radar_reflectivity_conv(instrument, model, hyd_type):
    """
    This estimates the radar reflectivity given a profile of liquid water mixing ratio.
    Convective DSDs are assumed.

    Parameters
    ----------
    instrument: :func:`emc2.core.Instrument` class
        The instrument to calculate the reflectivity parameters for.
    model: :func:`emc2.core.Model` class
        The model to calculate the parameters for.
    hyd_type: str
        The assumed hydrometeor type. Must be one of:
        'cl' (cloud liquid), 'ci' (cloud ice),
        'pl' (liquid precipitation), 'pi' (ice precipitation).

    Returns
    -------
    model: :func:`emc2.core.Model`
        Returns a Model with an added reflectivity field.
    """
    if not instrument.instrument_class.lower() == "radar":
        raise ValueError("Reflectivity can only be derived from a radar!")

    if hyd_type.lower() not in ['cl', 'ci', 'pl', 'pi']:
        raise ValueError("%s is not a valid hydrometeor type. Valid choices are cl, ci, pl, and pi." % hyd_type)
    q_field = model.q_names_convective[hyd_type]
    p_field = model.p_field
    t_field = model.T_field
    column_ds = model.ds

    WC = column_ds[q_field] * 1e3 * column_ds[p_field] * 1e2 / (instrument.R_d * column_ds[t_field])
    if hyd_type.lower() == "cl":
        column_ds['Ze'] = 0.031 * WC ** 1.56
    elif hyd_type.lower() == "pl":
        column_ds['Ze'] = ((WC * 1e3) / 3.4)**1.75
    else:
        Tc = column_ds[t_field] - 273.15
        if instrument.freq >= 2e9 and instrument.freq < 4e9:
            column_ds['Ze'] = 10**(((np.log10(WC) + 0.0197 * Tc + 1.7) / 0.060) / 10.)
        elif instrument.freq >= 27e9 and instrument.freq < 40e9:
            column_ds['Ze'] = 10**(((np.log10(WC) + 0.0186 * Tc + 1.63) / (0.000242 * Tc + 0.699)) / 10.)
        elif instrument.freq >= 75e9 and instrument.freq < 110e9:
            column_ds['Ze'] = 10**(((np.log10(WC) + 0.00706 * Tc + 0.992) / (0.000580 * Tc + 0.0923)) / 10.)
        else:
            column_ds['Ze'] = 10**(((np.log10(WC) + 0.0186 * Tc + 1.63) / (0.000242 * Tc + 0.0699)) / 10.)
    column_ds['Ze'] = 10 * np.log10(column_ds["Ze"])
    column_ds['Ze'].attrs["long_name"] = "Radar reflectivity factor"
    column_ds['Ze'].attrs["units"] = "dBZ"
    model.ds = column_ds
    return model


def calc_radar_moments(instrument, model, is_conv,
                       OD_from_sfc=True, **kwargs):
    """
    Calculates the reflectivity, doppler velocity, and spectral width
    in a given column for the given radar.

    Parameters
    ----------
    instrument: Instrument
        The instrument to simulate. The instrument must be a radar.
    model: Model
        The model to generate the parameters for.
    is_conv: bool
        True if the cell is convective
    z_field: str
        The name of the altitude field to use.
    OD_from_sfc: bool
        If True, then calculate optical depth from the surface.
    Additional keyword arguments are passed into
    :func:`emc2.simulator.reflectivity.calc_radar_reflectivity_conv` and
    :func:`emc2.simulator.attenuation.calc_radar_atm_attenuation`.

    Returns
    -------
    model: :func:`emc2.core.Model`
        The xarray Dataset containing the calculated radar moments.
    """

    hyd_types = ["cl", "ci", "pl", "pi"]
    hyd_names_dict = {'cl': 'cloud liquid particles', 'pl': 'liquid precipitation',
                      'ci': 'cloud ice particles', 'pi': 'liquid ice precipitation'}
    if not instrument.instrument_class.lower() == "radar":
        raise ValueError("Reflectivity can only be derived from a radar!")

    p_field = model.p_field
    t_field = model.T_field
    z_field = model.z_field
    column_ds = model.ds

    if is_conv:
        q_names = model.q_names_convective
        for hyd_type in hyd_types:
            temp_ds = calc_radar_reflectivity_conv(instrument, model, hyd_type)

            var_name = "sub_col_Ze_%s_conv" % hyd_type
            column_ds[var_name] = temp_ds.ds["Ze"]
            if "sub_col_Ze_tot_conv" in column_ds.variables.keys():
                column_ds["sub_col_Ze_tot_conv"] += 10**(column_ds[var_name] / 10)
            else:
                column_ds["sub_col_Ze_tot_conv"] = 10**(column_ds[var_name] / 10)
            column_ds[var_name].attrs["long_name"] = \
                "Radar reflectivity factor from %s in convective clouds" % hyd_type
            column_ds[var_name].attrs["units"] = "dBZ"

        column_ds["sub_col_Ze_tot_conv"] = 10 * np.log10(column_ds["sub_col_Ze_tot_conv"])

        kappa_ds = calc_radar_atm_attenuation(instrument, model)
        kappa_f = 6 * np.pi / instrument.wavelength * 1e-6 * model.Rho_hyd["cl"].magnitude
        WC = column_ds[q_names["cl"]] + column_ds[q_names["pl"]] * 1e3 * \
            column_ds[p_field] / (instrument.R_d * column_ds[t_field])
        dz = np.diff(column_ds[z_field].values, axis=0,
                     prepend=0.)

        if OD_from_sfc:
            WC_new = np.zeros_like(WC)
            WC_new[:, 1:] = WC[:, :-1]
            liq_ext = np.cumsum(kappa_f * dz * WC_new, axis=1)
            atm_ext = np.cumsum(kappa_ds.ds["kappa_att"].values * dz, axis=1)
        else:
            WC_new = np.zeros_like(WC)
            WC_new[:, 1:] = WC[:, :-1]
            liq_ext = np.flip(np.cumsum(kappa_f * dz * WC_new), axis=1)
            atm_ext = np.flip(np.cumsum(kappa_ds.ds["kappa_att"].values * dz), axis=1)

        if len(liq_ext.shape) == 1:
            liq_ext = liq_ext[:, np.newaxis]
        if len(atm_ext.shape) == 1:
            atm_ext = atm_ext[:, np.newaxis]
        liq_ext = xr.DataArray(liq_ext, dims=(model.time_dim, model.height_dim))
        atm_ext = xr.DataArray(atm_ext, dims=(model.time_dim, model.height_dim))

        column_ds["sub_col_Ze_att_tot_conv"] = column_ds["sub_col_Ze_tot_conv"] / \
            10**(2 * liq_ext / 10.) / 10**(2 * atm_ext / 10.)
        column_ds["sub_col_Ze_tot_conv"] = column_ds["sub_col_Ze_tot_conv"].where(
            column_ds["sub_col_Ze_tot_conv"] != 0)
        column_ds["sub_col_Ze_att_tot_conv"].attrs["long_name"] = \
            "Radar reflectivity factor from all hydrometeors in convection accounting for gaseous attenuation"
        column_ds["sub_col_Ze_att_tot_conv"].attrs["units"] = "dBZ"
        column_ds["sub_col_Ze_tot_conv"].attrs["long_name"] = \
            "Radar reflectivity factor from all hydrometeors in convection"
        column_ds["sub_col_Ze_tot_conv"].attrs["units"] = "dBZ"
        model.ds = column_ds
        return model

    q_names = model.q_names_stratiform
    n_names = model.N_field
    frac_names = model.strat_frac_names
    Dims = column_ds["strat_q_subcolumns_cl"].values.shape

    moment_denom_tot = np.zeros(Dims)
    V_d_numer_tot = np.zeros(Dims)
    sigma_d_numer_tot = np.zeros(Dims)
    od_tot = np.zeros(Dims)

    for hyd_type in ["pi", "pl", "ci", "cl"]:
        num_diam = len(instrument.mie_table[hyd_type]["p_diam"].values)
        if hyd_type == "pi":
            column_ds["sub_col_Ze_tot_strat"] = xr.DataArray(
                np.zeros(Dims), dims=column_ds.strat_q_subcolumns_cl.dims)
            column_ds["sub_col_Vd_tot_strat"] = xr.DataArray(
                np.zeros(Dims), dims=column_ds.strat_q_subcolumns_cl.dims)
            column_ds["sub_col_sigma_d_tot_strat"] = xr.DataArray(
                np.zeros(Dims), dims=column_ds.strat_q_subcolumns_cl.dims)
        column_ds["sub_col_Ze_%s_strat" % hyd_type] = xr.DataArray(
            np.zeros(Dims), dims=column_ds.strat_q_subcolumns_cl.dims)
        column_ds["sub_col_Vd_%s_strat" % hyd_type] = xr.DataArray(
            np.zeros(Dims), dims=column_ds.strat_q_subcolumns_cl.dims)
        column_ds["sub_col_sigma_d_%s_strat" % hyd_type] = xr.DataArray(
            np.zeros(Dims), dims=column_ds.strat_q_subcolumns_cl.dims)
        dD = instrument.mie_table[hyd_type]["p_diam"].values[1] - \
            instrument.mie_table[hyd_type]["p_diam"].values[0]
        fits_ds = calc_mu_lambda(model, hyd_type, subcolumns=True, **kwargs).ds
        total_hydrometeor = column_ds[frac_names[hyd_type]] * column_ds[n_names[hyd_type]]
        if hyd_type == "cl":
            for tt in range(Dims[1]):
                if tt % 100 == 0:
                    print('Stratiform moment for class %s progress: %d/%d' % (hyd_type, tt, Dims[1]))
                for k in range(Dims[2]):
                    if total_hydrometeor.values[tt, k] == 0:
                        continue

                    N_0_tmp = fits_ds["N_0"][:, tt, k].values.max(axis=0) * np.ones(
                        (model.num_subcolumns, num_diam))
                    lambda_tmp = fits_ds["lambda"][:, tt, k].values.max(axis=0) * np.ones(
                        (model.num_subcolumns, num_diam))
                    p_diam = (instrument.mie_table[hyd_type]["p_diam"].values * 2)
                    p_diam_tiled = np.tile(
                        instrument.mie_table[hyd_type]["p_diam"], (model.num_subcolumns, 1))
                    mu_temp = np.tile(fits_ds["mu"].values[:, tt, k], (num_diam, 1)).T
                    N_D = N_0_tmp * p_diam_tiled ** mu_temp * np.exp(-lambda_tmp * p_diam_tiled)
                    Calc_tmp = instrument.mie_table[hyd_type]["beta_p"].values * N_D
                    tmp_od = instrument.mie_table[hyd_type]["alpha_p"].values * N_D
                    tmp_od = (tmp_od.sum(axis=1) / 2.0 + tmp_od[:, 1:-1].sum(axis=1)) * dD
                    moment_denom = (Calc_tmp.sum(axis=1) / 2.0 + Calc_tmp[:, 1:-1].sum(axis=1)) * dD
                    moment_denom = moment_denom.astype('float64')
                    column_ds["sub_col_Ze_%s_strat" % hyd_type][:, tt, k] = \
                        (moment_denom * instrument.wavelength**4) / (instrument.K_w * np.pi**5) * 1e-6

                    v_tmp = model.vel_param_a[hyd_type] * p_diam**model.vel_param_b[hyd_type]
                    v_tmp = v_tmp.magnitude
                    Calc_tmp2 = v_tmp * Calc_tmp.astype('float64')
                    V_d_numer = (Calc_tmp2.sum(axis=1) / 2.0 + Calc_tmp2[:, 1:-1].sum(axis=1)) * dD
                    column_ds["sub_col_Vd_%s_strat" % hyd_type][:, tt, k] = -V_d_numer / moment_denom
                    Calc_tmp2 = (v_tmp -
                                 np.tile(column_ds["sub_col_Vd_%s_strat" % hyd_type][:, tt, k].values,
                                         (num_diam, 1)).T) ** 2 * Calc_tmp
                    sigma_d_numer = (Calc_tmp2.sum(axis=1) / 2.0 + Calc_tmp2[:, 1:-1].sum(axis=1)) * dD
                    column_ds["sub_col_sigma_d_%s_strat" % hyd_type][:, tt, k] = \
                        np.sqrt(sigma_d_numer / moment_denom)
                    V_d_numer_tot[:, tt, k] += V_d_numer
                    moment_denom_tot[:, tt, k] += moment_denom
                    od_tot[:, tt, k] += tmp_od
        else:
            p_diam_tiled = np.tile(
                instrument.mie_table[hyd_type]["p_diam"], (model.num_subcolumns, 1))
            sub_q_array = column_ds["strat_q_subcolumns_%s" % hyd_type].values
            v_tmp = model.vel_param_a[hyd_type] * p_diam_tiled ** model.vel_param_b[hyd_type]

            for tt in range(Dims[1]):
                if tt % 50 == 0:
                    print('Stratiform moment for class %s progress: %d/%d' % (hyd_type, tt, Dims[1]))
                for k in range(Dims[2]):
                    if total_hydrometeor.values[tt, k] == 0:
                        continue
                    N_0_tmp = fits_ds["N_0"][:, tt, k].values.max(axis=0)
                    lambda_tmp = fits_ds["lambda"][:, tt, k].values.max(axis=0)
                    mu = fits_ds["mu"][:, tt, k].values.max(axis=0)
                    N_D = N_0_tmp * np.exp(-lambda_tmp * p_diam_tiled) * p_diam_tiled**mu
                    Calc_tmp = np.tile(instrument.mie_table[hyd_type]["beta_p"].values,
                                       (model.num_subcolumns, 1)) * N_D
                    tmp_od = np.tile(
                        instrument.mie_table[hyd_type]["alpha_p"].values, (model.num_subcolumns, 1)) * N_D
                    tmp_od = (tmp_od.sum(axis=1) / 2 + tmp_od[:, 1:-1].sum(axis=1)) * dD
                    tmp_od = np.where(sub_q_array[:, tt, k] == 0, 0, tmp_od)
                    moment_denom = (Calc_tmp.sum(axis=1) / 2. + Calc_tmp[:, 1:-1].sum(axis=1)) * dD
                    moment_denom = np.where(sub_q_array[:, tt, k] == 0, np.nan, moment_denom)
                    column_ds["sub_col_Ze_%s_strat" % hyd_type][:, tt, k] = \
                        (moment_denom * instrument.wavelength ** 4) / (instrument.K_w * np.pi ** 5) * 1e-6
                    Calc_tmp2 = Calc_tmp * v_tmp.magnitude
                    V_d_numer = (Calc_tmp2.sum(axis=1) / 2. + Calc_tmp2[:, 1:-1].sum(axis=1)) * dD
                    V_d_numer = np.where(sub_q_array[:, tt, k] == 0, np.nan, V_d_numer)
                    column_ds["sub_col_Vd_%s_strat" % hyd_type][:, tt, k] = -V_d_numer / moment_denom
                    Calc_tmp2 = (v_tmp.magnitude - np.tile(
                        column_ds["sub_col_Vd_%s_strat" % hyd_type][:, tt, k].values,
                        (num_diam, 1)).T)**2 * Calc_tmp
                    Calc_tmp2 = (Calc_tmp2.sum(axis=1) / 2. + Calc_tmp2[:, 1:-1].sum(axis=1)) * dD
                    sigma_d_numer = np.where(sub_q_array[:, tt, k] == 0, np.nan, Calc_tmp2)
                    column_ds["sub_col_sigma_d_%s_strat" % hyd_type][:, tt, k] = \
                        np.sqrt(sigma_d_numer / moment_denom)
                    V_d_numer_tot[:, tt, k] += V_d_numer
                    moment_denom_tot[:, tt, k] += moment_denom
                    od_tot[:, tt, k] += tmp_od

        if "sub_col_Ze_tot_strat" in column_ds.variables.keys():
            column_ds["sub_col_Ze_tot_strat"] += column_ds["sub_col_Ze_%s_strat" % hyd_type].fillna(0)
        else:
            column_ds["sub_col_Ze_tot_strat"] = column_ds["sub_col_Ze_%s_strat" % hyd_type].fillna(0)

        column_ds["sub_col_Ze_%s_strat" % hyd_type] = 10 * np.log10(column_ds["sub_col_Ze_%s_strat" % hyd_type])
        column_ds["sub_col_Vd_%s_strat" % hyd_type] = column_ds["sub_col_Vd_%s_strat" % hyd_type].where(
            column_ds["sub_col_Vd_%s_strat" % hyd_type] != 0)
        column_ds["sub_col_sigma_d_%s_strat" % hyd_type] = column_ds["sub_col_Vd_%s_strat" % hyd_type].where(
            column_ds["sub_col_sigma_d_%s_strat" % hyd_type] != 0)
        column_ds["sub_col_Vd_tot_strat"] = xr.DataArray(-V_d_numer_tot / moment_denom_tot,
                                                         dims=column_ds["sub_col_Ze_tot_strat"].dims)

        column_ds["sub_col_Ze_%s_strat" % hyd_type].attrs["long_name"] = \
            "Radar reflectivity factor from %s in stratiform clouds" % hyd_names_dict[hyd_type]
        column_ds["sub_col_Ze_%s_strat" % hyd_type].attrs["units"] = "dBZ"
        column_ds["sub_col_Vd_%s_strat" % hyd_type].attrs["long_name"] = \
            "Doppler velocity from %s in stratiform clouds" % hyd_names_dict[hyd_type]
        column_ds["sub_col_Vd_%s_strat" % hyd_type].attrs["units"] = "m s-1"
        column_ds["sub_col_sigma_d_%s_strat" % hyd_type].attrs["long_name"] = \
            "Spectral width from %s in stratiform clouds" % hyd_names_dict[hyd_type]
        column_ds["sub_col_sigma_d_%s_strat" % hyd_type].attrs["units"] = "m s-1"
        print("Generating stratiform radar moments for hydrometeor class %s" % hyd_type)
        if hyd_type == "cl":
            for tt in range(Dims[1]):
                if tt % 50 == 0:
                    print('Stratiform moment for class %s progress: %d/%d' % (hyd_type, tt, Dims[1]))
                for k in range(Dims[2]):
                    if total_hydrometeor.values[tt, k] == 0:
                        continue
                    N_0_tmp = fits_ds["N_0"].values[:, tt, k]
                    p_diam = instrument.mie_table[hyd_type]["p_diam"].values
                    N_0_tmp, d_diam_tmp = np.meshgrid(N_0_tmp, p_diam)
                    lambda_tmp = fits_ds["lambda"].values[:, tt, k]
                    lambda_tmp, d_diam_tmp = np.meshgrid(lambda_tmp, p_diam)
                    mu_temp = fits_ds["mu"].values[:, tt, k] * np.ones_like(lambda_tmp)
                    N_D = N_0_tmp * d_diam_tmp ** mu_temp * np.exp(-lambda_tmp * d_diam_tmp)
                    Calc_tmp = np.tile(
                        instrument.mie_table[hyd_type]["beta_p"].values, (model.num_subcolumns, 1)) * N_D.T
                    moment_denom = (Calc_tmp.sum(axis=1) / 2.0 + Calc_tmp[:, 1:-1].sum(axis=1)) * dD
                    v_tmp = model.vel_param_a[hyd_type] * p_diam ** model.vel_param_b[hyd_type]
                    v_tmp = v_tmp.magnitude
                    Calc_tmp2 = (v_tmp - np.tile(
                        column_ds["sub_col_Vd_tot_strat"][:, tt, k].values, (num_diam, 1)).T) ** 2 * Calc_tmp
                    sigma_d_numer = (Calc_tmp2.sum(axis=1) / 2.0 + Calc_tmp2[:, 1:-1].sum(axis=1)) * dD
                    column_ds["sub_col_sigma_d_tot_strat"][:, tt, k] = np.sqrt(sigma_d_numer / moment_denom)

        else:
            mu = fits_ds["mu"].values.max()
            p_diam_tiled = np.tile(
                instrument.mie_table[hyd_type]["p_diam"], (model.num_subcolumns, 1))
            v_tmp = model.vel_param_a[hyd_type] * p_diam_tiled ** model.vel_param_b[hyd_type]
            v_tmp = v_tmp.magnitude
            sub_q_array = column_ds["strat_q_subcolumns_%s" % hyd_type].values
            for tt in range(Dims[1]):
                if tt % 50 == 0:
                    print('Stratiform moment for class %s progress: %d/%d' % (hyd_type, tt, Dims[1]))
                for k in range(Dims[2]):
                    if total_hydrometeor.values[tt, k] == 0:
                        continue
                    N_0_tmp = fits_ds["N_0"][:, tt, k].values.max(axis=0)
                    lambda_tmp = fits_ds["lambda"][:, tt, k].values.max(axis=0)
                    N_D = N_0_tmp * p_diam_tiled ** mu * np.exp(-lambda_tmp * p_diam_tiled)
                    Calc_tmp = np.tile(
                        instrument.mie_table[hyd_type]["beta_p"].values,
                        (model.num_subcolumns, 1)) * N_D
                    moment_denom = (Calc_tmp.sum(axis=1) / 2. + Calc_tmp[:, 1:-1].sum(axis=1)) * dD
                    moment_denom = np.where(sub_q_array[:, tt, k] == 0, 0, moment_denom)
                    Calc_tmp2 = (v_tmp - np.tile(
                        column_ds["sub_col_Vd_tot_strat"][:, tt, k].values, (num_diam, 1)).T) ** 2 * Calc_tmp
                    Calc_tmp2 = (Calc_tmp2.sum(axis=1) / 2. + Calc_tmp2[:, 1:-1].sum(axis=1)) * dD
                    sigma_d_numer = np.where(sub_q_array[:, tt, k] == 0, 0, Calc_tmp2)
                    column_ds["sub_col_sigma_d_%s_strat" % hyd_type][:, tt, k] = \
                        np.sqrt(sigma_d_numer / moment_denom)
                    sigma_d_numer_tot[:, tt, k] += sigma_d_numer

    column_ds["sub_col_sigma_d_tot_strat"] = xr.DataArray(np.sqrt(sigma_d_numer_tot / moment_denom_tot),
                                                          dims=column_ds["sub_col_Vd_tot_strat"].dims)
    kappa_ds = calc_radar_atm_attenuation(instrument, model)

    if OD_from_sfc:
        dz = np.diff(column_ds[z_field].values, axis=1, prepend=0)
        dz = np.tile(dz, (Dims[0], 1, 1))
        od_tot = np.cumsum(dz * od_tot, axis=1)
        atm_ext = np.cumsum(dz / 1e3 * kappa_ds.ds['kappa_att'].values, axis=2)
    else:
        dz = np.diff(column_ds[z_field].values, prepend=0)
        dz = np.tile(dz, (Dims[0], 1, 1))
        od_tot = np.flip(np.cumsum(np.flip(dz * od_tot, axis=1), axis=1), axis=2)
        atm_ext = np.flip(np.cumsum(np.flip(dz / 1e3 * kappa_ds.ds['kappa_att'].values, axis=1), axis=1), axis=2)

    column_ds['sub_col_Ze_att_tot_strat'] = \
        column_ds['sub_col_Ze_tot_strat'] * np.exp(-2 * od_tot) / 10**(2 * atm_ext / 10)
    column_ds['sub_col_Ze_tot_strat'] = column_ds['sub_col_Ze_tot_strat'].where(
        column_ds['sub_col_Ze_tot_strat'] != 0)
    column_ds['sub_col_Ze_att_tot_strat'] = column_ds['sub_col_Ze_tot_strat'].where(
        column_ds['sub_col_Ze_att_tot_strat'] != 0)
    column_ds['sub_col_Ze_tot_strat'] = 10 * np.log10(column_ds['sub_col_Ze_tot_strat'])
    column_ds['sub_col_Ze_att_tot_strat'] = 10 * np.log10(column_ds['sub_col_Ze_att_tot_strat'])
    column_ds['sub_col_Vd_tot_strat'] = column_ds['sub_col_Vd_tot_strat'].where(
        column_ds['sub_col_Vd_tot_strat'] != 0)
    column_ds['sub_col_sigma_d_tot_strat'] = column_ds['sub_col_sigma_d_tot_strat'].where(
        column_ds['sub_col_sigma_d_tot_strat'] != 0)

    column_ds['sub_col_Ze_att_tot_strat'].attrs["long_name"] = \
        "Radar reflectivity factor in stratiform clouds factoring in gaseous atteunation"
    column_ds['sub_col_Ze_att_tot_strat'].attrs["units"] = "dBZ"
    column_ds['sub_col_Ze_tot_strat'].attrs["long_name"] = \
        "Radar reflectivity factor in stratiform clouds"
    column_ds['sub_col_Ze_tot_strat'].attrs["units"] = "dBZ"
    column_ds['sub_col_Vd_tot_strat'].attrs["long_name"] = \
        "Doppler velocity in stratiform clouds"
    column_ds['sub_col_Vd_tot_strat'].attrs["units"] = "m s-1"
    column_ds['sub_col_sigma_d_tot_strat'].attrs["long_name"] = \
        "Spectral width in stratiform clouds"
    column_ds['sub_col_sigma_d_tot_strat'].attrs["units"] = "m s-1"
    model.ds = column_ds

    return model
