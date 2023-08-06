# Licensed under a 3-clause BSD style license - see LICENSE.rst
import numpy as np
from astropy import units as u
from astropy.coordinates import Angle
from astropy.io import fits
from astropy.table import Table
from astropy.utils import lazyproperty
from gammapy.maps import MapAxis
from gammapy.utils.array import array_stats_str
from gammapy.utils.interpolation import ScaledRegularGridInterpolator
from gammapy.utils.scripts import make_path
from .psf_table import EnergyDependentTablePSF, TablePSF

__all__ = ["PSF3D"]


class PSF3D:
    """PSF with axes: energy, offset, rad.

    Data format specification: :ref:`gadf:psf_table`

    Parameters
    ----------
    energy_lo : `~astropy.units.Quantity`
        Energy bins lower edges (1-dim)
    energy_hi : `~astropy.units.Quantity`
        Energy bins upper edges (1-dim)
    offset : `~astropy.coordinates.Angle`
        Offset angle (1-dim)
    rad_lo : `~astropy.coordinates.Angle`
        Offset angle bins lower edges
    rad_hi : `~astropy.coordinates.Angle`
        Offset angle bins upper edges
    psf_value : `~astropy.units.Quantity`
        PSF (3-dim with axes: psf[rad_index, offset_index, energy_index]
    energy_thresh_lo : `~astropy.units.Quantity`
        Lower energy threshold.
    energy_thresh_hi : `~astropy.units.Quantity`
        Upper energy threshold.
    """

    def __init__(
        self,
        energy_lo,
        energy_hi,
        offset,
        rad_lo,
        rad_hi,
        psf_value,
        energy_thresh_lo=u.Quantity(0.1, "TeV"),
        energy_thresh_hi=u.Quantity(100, "TeV"),
        interp_kwargs=None,
    ):
        self.energy_lo = energy_lo.to("TeV")
        self.energy_hi = energy_hi.to("TeV")
        self.offset = Angle(offset)
        self.rad_lo = Angle(rad_lo)
        self.rad_hi = Angle(rad_hi)
        self.psf_value = psf_value.to("sr^-1")
        self.energy_thresh_lo = energy_thresh_lo.to("TeV")
        self.energy_thresh_hi = energy_thresh_hi.to("TeV")

        self._interp_kwargs = interp_kwargs or {}

    @lazyproperty
    def _interpolate(self):
        energy = self._energy_logcenter()
        offset = self.offset.to("deg")
        rad = self._rad_center()

        return ScaledRegularGridInterpolator(
            points=(rad, offset, energy), values=self.psf_value, **self._interp_kwargs
        )

    def info(self):
        """Print some basic info.
        """
        ss = "\nSummary PSF3D info\n"
        ss += "---------------------\n"
        ss += array_stats_str(self.energy_lo, "energy_lo")
        ss += array_stats_str(self.energy_hi, "energy_hi")
        ss += array_stats_str(self.offset, "offset")
        ss += array_stats_str(self.rad_lo, "rad_lo")
        ss += array_stats_str(self.rad_hi, "rad_hi")
        ss += array_stats_str(self.psf_value, "psf_value")

        # TODO: should quote containment values also

        return ss

    def _energy_logcenter(self):
        """Get logcenters of energy bins.

        Returns
        -------
        energies : `~astropy.units.Quantity`
            Logcenters of energy bins
        """
        return np.sqrt(self.energy_lo * self.energy_hi)

    def _rad_center(self):
        """Get centers of rad bins (`~astropy.coordinates.Angle` in deg).
        """
        return ((self.rad_hi + self.rad_lo) / 2).to("deg")

    @classmethod
    def read(cls, filename, hdu="PSF_2D_TABLE"):
        """Create `PSF3D` from FITS file.

        Parameters
        ----------
        filename : str
            File name
        hdu : str
            HDU name
        """
        table = Table.read(make_path(filename), hdu=hdu)
        return cls.from_table(table)

    @classmethod
    def from_table(cls, table):
        """Create `PSF3D` from `~astropy.table.Table`.

        Parameters
        ----------
        table : `~astropy.table.Table`
            Table Table-PSF info.
        """
        theta_lo = table["THETA_LO"].quantity[0]
        theta_hi = table["THETA_HI"].quantity[0]
        offset = (theta_hi + theta_lo) / 2
        offset = Angle(offset, unit=table["THETA_LO"].unit)

        energy_lo = table["ENERG_LO"].quantity[0]
        energy_hi = table["ENERG_HI"].quantity[0]

        rad_lo = table["RAD_LO"].quantity[0]
        rad_hi = table["RAD_HI"].quantity[0]

        psf_value = table["RPSF"].quantity[0]

        opts = {}
        try:
            opts["energy_thresh_lo"] = u.Quantity(table.meta["LO_THRES"], "TeV")
            opts["energy_thresh_hi"] = u.Quantity(table.meta["HI_THRES"], "TeV")
        except KeyError:
            pass

        return cls(energy_lo, energy_hi, offset, rad_lo, rad_hi, psf_value, **opts)

    def to_fits(self):
        """
        Convert PSF table data to FITS HDU list.

        Returns
        -------
        hdu_list : `~astropy.io.fits.HDUList`
            PSF in HDU list format.
        """
        # Set up data
        names = [
            "ENERG_LO",
            "ENERG_HI",
            "THETA_LO",
            "THETA_HI",
            "RAD_LO",
            "RAD_HI",
            "RPSF",
        ]
        units = ["TeV", "TeV", "deg", "deg", "deg", "deg", "sr^-1"]
        data = [
            self.energy_lo,
            self.energy_hi,
            self.offset,
            self.offset,
            self.rad_lo,
            self.rad_hi,
            self.psf_value,
        ]

        table = Table()
        for name_, data_, unit_ in zip(names, data, units):
            table[name_] = [data_]
            table[name_].unit = unit_

        hdu = fits.BinTableHDU(table)
        hdu.header["LO_THRES"] = self.energy_thresh_lo.value
        hdu.header["HI_THRES"] = self.energy_thresh_hi.value

        return fits.HDUList([fits.PrimaryHDU(), hdu])

    def write(self, filename, *args, **kwargs):
        """Write PSF to FITS file.

        Calls `~astropy.io.fits.HDUList.writeto`, forwarding all arguments.
        """
        self.to_fits().writeto(filename, *args, **kwargs)

    def evaluate(self, energy=None, offset=None, rad=None):
        """Interpolate PSF value at a given offset and energy.

        Parameters
        ----------
        energy : `~astropy.units.Quantity`
            energy value
        offset : `~astropy.coordinates.Angle`
            Offset in the field of view
        rad : `~astropy.coordinates.Angle`
            Offset wrt source position

        Returns
        -------
        values : `~astropy.units.Quantity`
            Interpolated value
        """
        if energy is None:
            energy = self._energy_logcenter()
        if offset is None:
            offset = self.offset
        if rad is None:
            rad = self._rad_center()

        rad = np.atleast_1d(u.Quantity(rad))
        offset = np.atleast_1d(u.Quantity(offset))
        energy = np.atleast_1d(u.Quantity(energy))
        return self._interpolate(
            (
                rad[:, np.newaxis, np.newaxis],
                offset[np.newaxis, :, np.newaxis],
                energy[np.newaxis, np.newaxis, :],
            )
        )

    def to_energy_dependent_table_psf(self, theta="0 deg", rad=None, exposure=None):
        """
        Convert PSF3D in EnergyDependentTablePSF.

        Parameters
        ----------
        theta : `~astropy.coordinates.Angle`
            Offset in the field of view
        rad : `~astropy.coordinates.Angle`
            Offset from PSF center used for evaluating the PSF on a grid.
            Default is the ``rad`` from this PSF.
        exposure : `~astropy.units.Quantity`
            Energy dependent exposure. Should be in units equivalent to 'cm^2 s'.
            Default exposure = 1.

        Returns
        -------
        table_psf : `~gammapy.irf.EnergyDependentTablePSF`
            Energy-dependent PSF
        """
        theta = Angle(theta)
        energies = self._energy_logcenter()

        if rad is None:
            rad = self._rad_center()
        else:
            rad = Angle(rad)

        psf_value = self.evaluate(offset=theta, rad=rad).squeeze()
        return EnergyDependentTablePSF(
            energy=energies, rad=rad, exposure=exposure, psf_value=psf_value.T
        )

    def to_table_psf(self, energy, theta="0 deg", **kwargs):
        """Create `~gammapy.irf.TablePSF` at one given energy.

        Parameters
        ----------
        energy : `~astropy.units.Quantity`
            Energy
        theta : `~astropy.coordinates.Angle`
            Offset in the field of view. Default theta = 0 deg

        Returns
        -------
        psf : `~gammapy.irf.TablePSF`
            Table PSF
        """
        energy = u.Quantity(energy)
        theta = Angle(theta)
        psf_value = self.evaluate(energy, theta).squeeze()
        rad = self._rad_center()
        return TablePSF(rad, psf_value, **kwargs)

    def containment_radius(
        self, energy, theta="0 deg", fraction=0.68, interp_kwargs=None
    ):
        """Containment radius.

        Parameters
        ----------
        energy : `~astropy.units.Quantity`
            Energy
        theta : `~astropy.coordinates.Angle`
            Offset in the field of view. Default theta = 0 deg
        fraction : float
            Containment fraction. Default fraction = 0.68

        Returns
        -------
        radius : `~astropy.units.Quantity`
            Containment radius in deg
        """
        energy = np.atleast_1d(u.Quantity(energy))
        theta = np.atleast_1d(u.Quantity(theta))

        radii = []
        for t in theta:
            psf = self.to_energy_dependent_table_psf(theta=t)
            radii.append(psf.containment_radius(energy, fraction=fraction))

        return u.Quantity(radii).T.squeeze()

    def plot_containment_vs_energy(
        self, fractions=[0.68, 0.95], thetas=Angle([0, 1], "deg"), ax=None
    ):
        """Plot containment fraction as a function of energy.
        """
        import matplotlib.pyplot as plt

        ax = plt.gca() if ax is None else ax

        energy = MapAxis.from_energy_bounds(
            self.energy_lo[0], self.energy_hi[-1], 100
        ).edges

        for theta in thetas:
            for fraction in fractions:
                radius = self.containment_radius(energy, theta, fraction)
                label = f"{theta.deg} deg, {100 * fraction:.1f}%"
                ax.plot(energy.value, radius.value, label=label)

        ax.semilogx()
        ax.legend(loc="best")
        ax.set_xlabel("Energy (TeV)")
        ax.set_ylabel("Containment radius (deg)")

    def plot_psf_vs_rad(self, theta="0 deg", energy=u.Quantity(1, "TeV")):
        """Plot PSF vs rad.

        Parameters
        ----------
        energy : `~astropy.units.Quantity`
            Energy. Default energy = 1 TeV
        theta : `~astropy.coordinates.Angle`
            Offset in the field of view. Default theta = 0 deg
        """
        theta = Angle(theta)
        table = self.to_table_psf(energy=energy, theta=theta)
        return table.plot_psf_vs_rad()

    def plot_containment(
        self, fraction=0.68, ax=None, show_safe_energy=False, add_cbar=True, **kwargs
    ):
        """
        Plot containment image with energy and theta axes.

        Parameters
        ----------
        fraction : float
            Containment fraction between 0 and 1.
        add_cbar : bool
            Add a colorbar
        """
        import matplotlib.pyplot as plt

        ax = plt.gca() if ax is None else ax

        energy = self._energy_logcenter()
        offset = self.offset

        # Set up and compute data
        containment = self.containment_radius(energy, offset, fraction)

        # plotting defaults
        kwargs.setdefault("cmap", "GnBu")
        kwargs.setdefault("vmin", np.nanmin(containment.value))
        kwargs.setdefault("vmax", np.nanmax(containment.value))

        # Plotting
        x = energy.value
        y = offset.value
        caxes = ax.pcolormesh(x, y, containment.value.T, **kwargs)

        # Axes labels and ticks, colobar
        ax.semilogx()
        ax.set_ylabel(f"Offset ({offset.unit})")
        ax.set_xlabel(f"Energy ({energy.unit})")
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())

        if show_safe_energy:
            self._plot_safe_energy_range(ax)

        if add_cbar:
            label = f"Containment radius R{100 * fraction:.0f} ({containment.unit})"
            ax.figure.colorbar(caxes, ax=ax, label=label)

        return ax

    def _plot_safe_energy_range(self, ax):
        """add safe energy range lines to the plot"""
        esafe = self.energy_thresh_lo
        omin = self.offset.value.min()
        omax = self.offset.value.max()
        ax.hlines(y=esafe.value, xmin=omin, xmax=omax)
        label = f"Safe energy threshold: {esafe:3.2f}"
        ax.text(x=0.1, y=0.9 * esafe.value, s=label, va="top")

    def peek(self, figsize=(15, 5)):
        """Quick-look summary plots."""
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=figsize)

        self.plot_containment(fraction=0.68, ax=axes[0])
        self.plot_containment(fraction=0.95, ax=axes[1])
        self.plot_containment_vs_energy(ax=axes[2])

        # TODO: implement this plot
        # psf = self.psf_at_energy_and_theta(energy='1 TeV', theta='1 deg')
        # psf.plot_components(ax=axes[2])

        plt.tight_layout()
