import numpy as np
from astropy import units as u
from astropy.table import Table
from astropy.visualization import quantity_support
from gammapy.extern.skimage import block_reduce
from gammapy.utils.interpolation import ScaledRegularGridInterpolator
from gammapy.utils.regions import compound_region_to_list
from .base import Map
from .geom import pix_tuple_to_idx
from .region import RegionGeom
from .utils import INVALID_INDEX

__all__ = ["RegionNDMap"]


class RegionNDMap(Map):
    """Region ND map

    Parameters
    ----------
    geom : `~gammapy.maps.RegionGeom`
        Region geometry object.
    data : `~numpy.ndarray`
        Data array. If none then an empty array will be allocated.
    dtype : str, optional
        Data type, default is float32
    meta : `dict`
        Dictionary to store meta data.
    unit : str or `~astropy.units.Unit`
        The map unit
    """

    def __init__(self, geom, data=None, dtype="float32", meta=None, unit=""):
        if data is None:
            data = np.zeros(geom.data_shape, dtype=dtype)

        self._geom = geom
        self.data = data
        self.meta = meta
        self.unit = u.Unit(unit)

    def plot(self, ax=None, **kwargs):
        """Plot region map.

        Parameters
        ----------
        ax : `~matplotlib.pyplot.Axis`
            Axis used for plotting
        **kwargs : dict
            Keyword arguments passed to `~matplotlib.pyplot.errorbar`

        Returns
        -------
        ax : `~matplotlib.pyplot.Axis`
            Axis used for plotting
        """
        import matplotlib.pyplot as plt

        ax = ax or plt.gca()

        kwargs.setdefault("fmt", ".")

        if len(self.geom.axes) > 1:
            raise TypeError(
                "Use `.plot_interactive()` if more the one extra axis is present."
            )

        axis = self.geom.axes[0]

        with quantity_support():
            xerr = (axis.center - axis.edges[:-1], axis.edges[1:] - axis.center)
            ax.errorbar(axis.center, self.quantity.squeeze(), xerr=xerr, **kwargs)

        if axis.interp == "log":
            ax.set_xscale("log")

        ax.set_xlabel(axis.name.capitalize() + f" [{axis.unit}]")

        if not self.unit.is_unity():
            ax.set_ylabel(f"Data [{self.unit}]")

        ax.set_yscale("log")
        return ax

    def plot_hist(self, ax=None, **kwargs):
        """Plot as histogram.

        kwargs are forwarded to `~matplotlib.pyplot.hist`

        Parameters
        ----------
        ax : `~matplotlib.axis` (optional)
            Axis instance to be used for the plot
        **kwargs : dict
            Keyword arguments passed to `~matplotlib.pyplot.hist`

        Returns
        -------
        ax : `~matplotlib.pyplot.Axis`
            Axis used for plotting
        """
        import matplotlib.pyplot as plt

        ax = plt.gca() if ax is None else ax

        kwargs.setdefault("histtype", "step")
        kwargs.setdefault("lw", 2)

        axis = self.geom.axes[0]

        with quantity_support():
            weights = self.data[:, 0, 0]
            ax.hist(axis.center.value, bins=axis.edges.value, weights=weights, **kwargs)

        ax.set_xlabel(axis.name.capitalize() + f" [{axis.unit}]")

        if not self.unit.is_unity():
            ax.set_ylabel(f"Data [{self.unit}]")

        ax.set_xscale("log")
        ax.set_yscale("log")
        return ax

    def plot_interactive(self):
        raise NotImplementedError(
            "Interactive plotting currently not support for RegionNDMap"
        )

    def plot_region(self, ax=None, **kwargs):
        """Plot region

        Parameters
        ----------
        ax : `~astropy.vizualisation.WCSAxes`
            Axes to plot on.
        **kwargs : dict
            Keyword arguments forwarded to `~regions.PixelRegion.as_artist`
        """
        import matplotlib.pyplot as plt
        from matplotlib.collections import PatchCollection

        if ax is None:
            ax = plt.gca()

        regions = compound_region_to_list(self.geom.region)
        artists = [region.to_pixel(wcs=ax.wcs).as_artist() for region in regions]

        patches = PatchCollection(artists, **kwargs)
        ax.add_collection(patches)
        return ax

    @classmethod
    def create(cls, region, axes=None, dtype="float32", meta=None, unit="", wcs=None):
        """

        Parameters
        ----------
        region : str or `~regions.SkyRegion`
            Region specification
        axes : list of `MapAxis`
            Non spatial axes.
        dtype : str
            Data type, default is 'float32'
        unit : str or `~astropy.units.Unit`
            Data unit.
        meta : `dict`
            Dictionary to store meta data.
        wcs : `~astropy.wcs.WCS`
            WCS projection to use for local projections of the region

        Returns
        -------
        map : `RegionNDMap`
            Region map
        """
        geom = RegionGeom.create(region=region, axes=axes, wcs=wcs)
        return cls(geom=geom, dtype=dtype, unit=unit, meta=meta)

    def downsample(self, factor, preserve_counts=True, axis="energy"):
        geom = self.geom.downsample(factor=factor, axis=axis)
        block_size = [1] * self.data.ndim
        idx = self.geom.get_axis_index_by_name(axis)
        block_size[-(idx + 1)] = factor

        func = np.nansum if preserve_counts else np.nanmean
        data = block_reduce(self.data, tuple(block_size[::-1]), func=func)

        return self._init_copy(geom=geom, data=data)

    def upsample(self, factor, preserve_counts=True, axis="energy"):
        geom = self.geom.upsample(factor=factor, axis=axis)
        data = self.interp_by_coord(geom.get_coord())

        if preserve_counts:
            data /= factor

        return self._init_copy(geom=geom, data=data)

    def fill_by_idx(self, idx, weights=None):
        idx = pix_tuple_to_idx(idx)

        msk = np.all(np.stack([t != INVALID_INDEX.int for t in idx]), axis=0)
        idx = [t[msk] for t in idx]

        if weights is not None:
            if isinstance(weights, u.Quantity):
                weights = weights.to_value(self.unit)
            weights = weights[msk]

        idx = np.ravel_multi_index(idx, self.data.T.shape)
        idx, idx_inv = np.unique(idx, return_inverse=True)
        weights = np.bincount(idx_inv, weights=weights).astype(self.data.dtype)
        self.data.T.flat[idx] += weights

    def get_by_idx(self, idxs):
        return self.data[idxs[::-1]]

    def interp_by_coord(self, coords):
        pix = self.geom.coord_to_pix(coords)
        return self.interp_by_pix(pix)

    def interp_by_pix(self, pix, method="linear", fill_value=None):
        grid_pix = [np.arange(n, dtype=float) for n in self.data.shape[::-1]]

        if np.any(np.isfinite(self.data)):
            data = self.data.copy().T
            data[~np.isfinite(data)] = 0.0
        else:
            data = self.data.T

        fn = ScaledRegularGridInterpolator(
            grid_pix, data, fill_value=fill_value, method=method
        )
        return fn(tuple(pix), clip=False)

    def set_by_idx(self, idx, value):
        self.data[idx[::-1]] = value

    @staticmethod
    def read(cls, filename):
        raise NotImplementedError

    def write(self, filename):
        raise NotImplementedError

    def to_hdulist(self):
        raise NotImplementedError

    @classmethod
    def from_hdulist(cls, hdulist, format="ogip", ogip_column="COUNTS"):
        """Create from `~astropy.io.fits.HDUList`.


        Parameters
        ----------
        hdulist : `~astropy.io.fits.HDUList`
            HDU list.
        format : {"ogip"}
            Format specification
        ogip_column : str
            OGIP data format column

        Returns
        -------
        region_nd_map : `RegionNDMap`
            Region map.
        """
        if format != "ogip":
            raise ValueError("Only 'ogip' format supported")

        table = Table.read(hdulist["SPECTRUM"])
        geom = RegionGeom.from_hdulist(hdulist, format=format)

        return cls(geom=geom, data=table[ogip_column].data, meta=table.meta)

    def crop(self):
        raise NotImplementedError("Crop is not supported by RegionNDMap")

    def pad(self):
        raise NotImplementedError("Pad is not supported by RegionNDMap")

    def sum_over_axes(self, keepdims=True):
        axis = tuple(range(self.data.ndim - 2))
        geom = self.geom.to_image()
        if keepdims:
            for ax in self.geom.axes:
                geom = geom.to_cube([ax.squash()])
        data = np.nansum(self.data, axis=axis, keepdims=keepdims)
        # TODO: summing over the axis can change the unit, handle this correctly
        return self._init_copy(geom=geom, data=data)

    def stack(self, other, weights=None):
        """Stack other region map into map.

        Parameters
        ----------
        other : `RegionNDMap`
            Other map to stack
        weights : `RegionNDMap`
            Array to be used as weights. The spatial geometry must be equivalent
            to `other` and additional axes must be broadcastable.
        """
        data = other.data

        # TODO: re-think stacking of regions. Is making the union reasonable?
        # self.geom.union(other.geom)

        if weights is not None:
            if not other.geom.to_image() == weights.geom.to_image():
                raise ValueError("Incompatible geoms between map and weights")
            data = data * weights.data

        self.data += data

    def to_table(self):
        """Convert to `~astropy.table.Table`.

        Data format specification: :ref:`gadf:ogip-pha`
        """
        energy_axis = self.geom.axes[0]
        channel = np.arange(energy_axis.nbin, dtype=np.int16)
        counts = np.array(self.data[:, 0, 0], dtype=np.int32)

        names = ["CHANNEL", "COUNTS"]
        meta = {"name": "COUNTS"}

        return Table([channel, counts], names=names, meta=meta)
