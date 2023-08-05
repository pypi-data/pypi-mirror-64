import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import LogNorm

from . import utils

FONT_SIZE = 8

COLOR_MAPS = {
    'amplitude': cm.gray,
    'intensity': cm.gray,
    'phase': cm.bwr,
    'zernike': cm.jet,  # Just to follow the general convention.
}


def plot_psf(
        imaging_system,
        axis_unit=u.um,
        colorbar=True,
        zmin=None,
        zmax=None,
        bar_ticks=None,
        bar_ticks_labels=None,
        title=None,
        fontsize=FONT_SIZE,
        subplot_layout=111,
        dpi=130,
        figsize=(5, 5),
        cmap=None,
        log_scale=True,
        **kwargs
):
    """Plots Point-Spread Function of an imaging system in matplotlib.

    :param imaging_system: imaging system to be used
    :type imaging_system: pyoptica.coherent_imaging_system
    :param axis_unit: The X,Y grid will be converted and plotted in the given unit
    :type axis_unit: astropy.Quantity of type length
    :param colorbar: Should colorbar explaining plotted values be shown
    :type colorbar: bool
    :param zmin: Minimal value to be shown
    :type zmin: float
    :param zmax: Maximal value to be shown
    :type zmax: float
    :param bar_ticks: Ticks of the colorbar
    :type bar_ticks: iterable
    :param bar_ticks_labels: Labels of the ticks of the colorbar
    :type bar_ticks: iterable
    :param title: Title of the plot
    :type title: str
    :param fontsize: Size of the font
    :type fontsize: int
    :param figsize: Size of output figure in inches
    :type figsize: (int, int)
    :param dpi: dots per inch of the resulting figure
    :type dpi: int
    :param cmap: colormap to be used
    :type cmap: matplotlib.colors.LinearSegmentedColormap
    :param log_scale: should logarithmic scale be used?
    :type: bool
    :param kwargs: all kwargs passed to matplotlib.pyplot.imshow
    :type kwargs: object
    :return: plot of asked values
    :rtype: matplotlib.figure, matplotlib.axis

    **Example**

    >>> import astropy.units as u
    >>> import pyoptica as po
    >>>
    >>> wavelength = 633.2 * u.nm
    >>> pixel_scale = 100 * u.nm
    >>> npix = 1024
    >>> na = 0.1
    >>>
    >>> img_system = po.CoherentImagingSystem(
    >>>     wavelength, pixel_scale, npix, na=na)
    >>> img_system.calc_H()  # We need to run this to precalculate the pupil!
    >>> _ = po.plotting.plot_psf(img_system, log_scale=True, zmin=10e-10)

    """
    z = np.abs(imaging_system.psf) ** 2
    if title is None:
        title = 'Point-Spread Function'
    x1, x2 = imaging_system.x[0, 0], imaging_system.x[-1, -1]
    y1, y2 = imaging_system.y[0, 0], imaging_system.y[-1, -1]
    if cmap is None:
        cmap = COLOR_MAPS['intensity']
    colorbar_title = '[arb. u.]'
    return plot_img(
        z, axis_unit, bar_ticks, bar_ticks_labels, cmap, colorbar,
        colorbar_title, dpi, figsize, fontsize, subplot_layout, title, x1, x2,
        y1, y2, zmax, zmin, log_scale, **kwargs)


def plot_transfer_function(
        imaging_system,
        axis_unit=u.um ** -1,
        colorbar=True,
        zmin=None,
        zmax=None,
        bar_ticks=None,
        bar_ticks_labels=None,
        title=None,
        fontsize=FONT_SIZE,
        subplot_layout=111,
        dpi=130,
        figsize=(5, 5),
        cmap=None,
        log_scale=False,
        **kwargs
):
    """Plots Transfer Function H of an imaging systems in matplotlib.

    :param imaging_system: imaging system to be used
    :type imaging_system: pyoptica.coherent_imaging_system
    :param axis_unit: The X,Y grid will be converted and plotted in the given unit
    :type axis_unit: astropy.Quantity of type length
    :param colorbar: Should colorbar explaining plotted values be shown
    :type colorbar: bool
    :param zmin: Minimal value to be shown
    :type zmin: float
    :param zmax: Maximal value to be shown
    :type zmax: float
    :param bar_ticks: Ticks of the colorbar
    :type bar_ticks: iterable
    :param bar_ticks_labels: Labels of the ticks of the colorbar
    :type bar_ticks: iterable
    :param title: Title of the plot
    :type title: str
    :param fontsize: Size of the font
    :type fontsize: int
    :param figsize: Size of output figure in inches
    :type figsize: (int, int)
    :param dpi: dots per inch of the resulting figure
    :type dpi: int
    :param cmap: colormap to be used
    :type cmap: matplotlib.colors.LinearSegmentedColormap
    :param log_scale: should logarithmic scale be used?
    :type: bool
    :param kwargs: all kwargs passed to matplotlib.pyplot.imshow
    :type kwargs: object
    :return: plot of asked values
    :rtype: matplotlib.figure, matplotlib.axis

    **Example**

    >>> import astropy.units as u
    >>> import pyoptica as po

    >>> wavelength = 633.2 * u.nm
    >>> pixel_scale = 100 * u.nm
    >>> npix = 1024
    >>> na = 0.1

    >>> img_system = po.CoherentImagingSystem(
    >>>     wavelength, pixel_scale, npix, na=na)
    >>> img_system.calc_H()  # We need to run this to precalculate the pupil!
    >>> _ = po.plotting.plot_transfer_function(img_system)

    """
    z = np.abs(imaging_system.H)
    if title is None:
        title = 'Amplitude Transfer Function'
    f1, f2 = imaging_system.f[0, 0], imaging_system.f[-1, -1]
    g1, g2 = imaging_system.g[0, 0], imaging_system.g[-1, -1]
    if cmap is None:
        cmap = COLOR_MAPS['intensity']
    colorbar_title = '[arb. u.]'
    return plot_img(
        z, axis_unit, bar_ticks, bar_ticks_labels, cmap, colorbar,
        colorbar_title, dpi, figsize, fontsize, subplot_layout, title, f1, f2,
        g1, g2, zmax, zmin, log_scale, **kwargs)


def plot_wavefront(
        wavefront,
        what='intensity',
        axis_unit=u.um,
        colorbar=True,
        zmin=None,
        zmax=None,
        bar_ticks=None,
        bar_ticks_labels=None,
        title=None,
        fontsize=FONT_SIZE,
        subplot_layout=111,
        dpi=130,
        figsize=(5, 5),
        cmap=None,
        log_scale=False,
        phase_plotting_threshold=100,
        **kwargs
):
    """Plots a wavefront in matplotlib. Depending on value of `what` the following
    can be plotted: `intensity`, `amplitude`, `phase`.

    :param wavefront: wavefront to be plotted.
    :type wavefront: pyoptica.Wavefront
    :param what: What should be plotted: 'intensity', 'amplitude', 'phase'
    :type what: str
    :param axis_unit: The X,Y grid will be converted and plotted in the given unit
    :type axis_unit: astropy.Quantity of type length
    :param colorbar: Should colorbar explaining plotted values be shown
    :type colorbar: bool
    :param zmin: Minimal value to be shown
    :type zmin: float
    :param zmax: Maximal value to be shown
    :type zmax: float
    :param bar_ticks: Ticks of the colorbar
    :type bar_ticks: iterable
    :param bar_ticks_labels: Labels of the ticks of the colorbar
    :type bar_ticks: iterable
    :param title: Title of the plot
    :type title: str
    :param fontsize: Size of the font
    :type fontsize: int
    :param figsize: Size of output figure in inches
    :type figsize: (int, int)
    :param dpi: dots per inch of the resulting figure
    :type dpi: int
    :param cmap: colormap to be used
    :type cmap: matplotlib.colors.LinearSegmentedColormap
    :param log_scale: should logarithmic scale be used?
    :type: bool
    :param phase_plotting_threshold: if `wf.amplitude[x, y] < wf.amplitude.mean() / phase_plotting_threshold` it will not be plotted
    :type phase_plotting_threshold: float
    :param kwargs: all kwargs passed to matplotlib.pyplot.imshow
    :type kwargs: object
    :param kwargs: all kwargs passed to matplotlib.pyplot.imshow
    :type kwargs: object
    :return: plot of asked values
    :rtype: matplotlib.figure, matplotlib.axis

    **Example**

    >>> import astropy.units as u
    >>> import pyoptica as po

    >>> wavelength = 500 * u.nm
    >>> pixel_scale = 22 * u.um
    >>> npix = 1024
    >>> w = 6 * u.mm
    >>> h = 3 * u.mm
    >>> axis_unit = u.mm

    >>> wf = po.Wavefront(wavelength, pixel_scale, npix)
    >>> ap = po.RectangularAperture(w, h)
    >>> wf = wf * ap
    >>> _ = po.plotting.plot_wavefront(wf, axis_unit=u.mm)

    """
    if cmap is None:
        cmap = COLOR_MAPS[what]
    if what == 'intensity':
        z = wavefront.intensity
        if title is None:
            title = 'Intensity'
        colorbar_title = '[arb. u.]'
    elif what == 'amplitude':
        z = wavefront.amplitude
        if title is None:
            title = 'Amplitude'
        colorbar_title = '[arb. u.]'
    elif what == 'phase':
        z = wavefront.phase
        # Phase is plotted only for non-zero intensity values
        avg_i = np.average(wavefront.intensity[wavefront.intensity > 0])
        if phase_plotting_threshold != 0:
            no_phase_indices = np.where(
                wavefront.intensity < avg_i / phase_plotting_threshold
            )
            z[no_phase_indices] = np.nan
        if title is None:
            title = 'Phase'
        colorbar_title = '[rad]'
        if zmin is None and zmax is None:
            zmin = -np.pi
            zmax = np.pi
            bar_ticks = [-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]
            bar_ticks_labels = [
                r'$-\pi$',
                r'$-\frac{\pi}{2}$',
                r'$0$',
                r'$\frac{\pi}{2}$',
                r'$\pi$'
            ]
        cmap.set_bad((0.0, 0.0, 0))
    else:
        raise ValueError("Only 'intensity', 'amplitude', and 'phase'"
                         "can be plotted.")
    x1, x2 = wavefront.x[0, 0], wavefront.x[-1, -1]
    y1, y2 = wavefront.y[0, 0], wavefront.y[-1, -1]
    return plot_img(
        z, axis_unit, bar_ticks, bar_ticks_labels, cmap, colorbar,
        colorbar_title, dpi, figsize, fontsize, subplot_layout, title, x1, x2,
        y1, y2, zmax, zmin, log_scale, **kwargs)


def plot_zernike(
        zernike_array,
        rho,
        theta,
        axis_unit=u.dimensionless_unscaled,
        colorbar=True,
        zmin=None,
        zmax=None,
        bar_ticks=None,
        bar_ticks_labels=None,
        title=None,
        fontsize=FONT_SIZE,
        subplot_layout=111,
        dpi=130,
        figsize=(5, 5),
        cmap=None,
        log_scale=False,
        **kwargs
):
    """Plots Zernike distribution in matplotlib.

    :param zernike_array: array representing a polynomial
    :type zernike_array: numpy.array
    :param rho: radial coordinates of the plane,
    :type rho: numpy.array
    :param theta: angle coordinate of the plane
    :type theta: numpy.array
    :param axis_unit: The X,Y grid will be converted and plotted in the given unit
    :type axis_unit: astropy.Quantity of type length
    :param colorbar: Should colorbar explaining plotted values be shown
    :type colorbar: bool
    :param zmin: Minimal value to be shown
    :type zmin: float
    :param zmax: Maximal value to be shown
    :type zmax: float
    :param bar_ticks: Ticks of the colorbar
    :type bar_ticks: iterable
    :param bar_ticks_labels: Labels of the ticks of the colorbar
    :type bar_ticks: iterable
    :param title: Title of the plot
    :type title: str
    :param fontsize: Size of the font
    :type fontsize: int
    :param figsize: Size of output figure in inches
    :type figsize: (int, int)
    :param dpi: dots per inch of the resulting figure
    :type dpi: int
    :param cmap: colormap to be used
    :type cmap: matplotlib.colors.LinearSegmentedColormap
    :param log_scale: should logarithmic scale be used?
    :type: bool
    :param kwargs: all kwargs passed to matplotlib.pyplot.imshow
    :type kwargs: object
    :return: plot of asked values
    :rtype: matplotlib.figure, matplotlib.axis

    **Example**

    >>> import astropy.units as u
    >>> import numpy as np
    >>> import pyoptica as po
    >>>
    >>> npix = 101
    >>> pixel_scale = 0.5 * u.m
    >>> x, y = po.utils.mesh_grid(npix, pixel_scale)
    >>> r_max = .48 * npix * pixel_scale
    >>> r, theta = po.utils.cart2pol(x, y)
    >>> r = r / r_max
    >>>
    >>> m, n = -1, 3
    >>> z = po.zernike(m, n, r, theta, fill_value=np.nan)
    >>> _ = po.plotting.plot_zernike(z, r, theta, title=f'Zernike m={m}, n={n}')

    """
    if title is None:
        title = 'Zernike Distribution'
    x, y = utils.pol2cart(rho, theta)
    x1, x2 = x[0, 0], x[-1, -1]
    y1, y2 = y[0, 0], y[-1, -1]
    if cmap is None:
        cmap = COLOR_MAPS['zernike']
    if zmin is None and zmax is None:
        zmax = np.nanmax(zernike_array)
        zmin = np.nanmin(zernike_array)
        zmax = max(abs(zmax), abs(zmin))
        zmin = -zmax
    colorbar_title = '[arb. u.]'
    return plot_img(
        zernike_array, axis_unit, bar_ticks, bar_ticks_labels, cmap, colorbar,
        colorbar_title, dpi, figsize, fontsize, subplot_layout, title, x1, x2,
        y1, y2, zmax, zmin, log_scale, **kwargs)


def plot_img(
        z, axis_unit, bar_ticks, bar_ticks_labels, cmap, colorbar,
        colorbar_title, dpi, figsize, fontsize, subplot_layout, title, x1, x2,
        y1, y2, zmax, zmin, log_scale, **kwargs):
    """A base function for plotting a 2D distribution in matplotlib.
    :param z: array to be plotted
    :type z: np.array
    :param axis_unit: The X,Y grid will be converted and plotted in the unit
    :type axis_unit: astropy.Quantity of type length
    :param bar_ticks: Ticks of the colorbar
    :type bar_ticks: iterable
    :param bar_ticks_labels: Labels of the ticks of the colorbar
    :type bar_ticks: iterable
    :param cmap: colormap to be used
    :type cmap: matplotlib.colors.LinearSegmentedColormap
    :param colorbar: Should colorbar explaining plotted values be shown
    :type colorbar: bool
    :param colorbar_title: Title of the colorbar
    :type colorbar_title: str
    :param dpi: dots per inch of the resulting figure
    :type dpi: int
    :param figsize: Size of output figure in inches
    :type figsize: (int, int)
    :param fontsize: Size of the font
    :type fontsize: int
    :param subplot_layout: layout in case of many plots
    :type subplot_layout: int
    :param title: Title of the plot
    :type title: str
    :param x1: minimum value on OX-axis
    :type x1: float
    :param x2: maximum value on OX-axis
    :type x2: float
    :param y1: minimum value on OY-axis
    :type y1: float
    :param y2: maximum value on OY-axis
    :type y2: float
    :param zmin: minimum value on OZ-axis
    :type zmin: float
    :param zmax: maximum value on OZ-axis
    :type zmax: float
    :param log_scale: should logarithmic scale be used>
    :type log_scale: bool
    :param kwargs: all kwargs passed to matplotlib.pyplot.imshow
    :type kwargs: object
    :return: plot of asked values
    :rtype: matplotlib.figure, matplotlib.axis

    """
    axis_title = axis_unit.to_string()
    fig = plt.figure(dpi=dpi, figsize=figsize)
    ax = fig.add_subplot(subplot_layout)
    extent = [i.to(axis_unit).value for i in [x1, x2, y1, y2]]
    if log_scale is True:
        norm = LogNorm(vmin=zmin, vmax=zmax)
    else:
        norm = None
    plot = ax.imshow(
        z, vmin=zmin, vmax=zmax, cmap=cmap, interpolation=None, extent=extent,
        norm=norm, **kwargs
    )
    ax.set_title(title)
    ax.set_xlabel(axis_title)
    ax.set_ylabel(axis_title)
    if colorbar is True:
        # The magic values make sure the colorbar looks good...
        # Found the on the internet.
        c_bar = plt.colorbar(plot, fraction=0.046, pad=0.04)
        c_bar.ax.set_title(colorbar_title, fontsize=fontsize)
        if bar_ticks is not None:
            c_bar.set_ticks(bar_ticks)
        if bar_ticks_labels is not None:
            c_bar.set_ticklabels(bar_ticks_labels)
        c_bar.ax.tick_params(labelsize=fontsize)

    set_font_of_plot(ax, fontsize)
    plt.tight_layout()
    return fig, plot, ax


def set_font_of_plot(plot, font_size=FONT_SIZE):
    """Sets font of a plot
    :param plot: matplotlib.axes
        Plot on which font should be adjusted
    :param font_size: int

    """
    plot.title.set_fontsize(font_size)
    labels = [plot.xaxis.label, plot.yaxis.label] + \
             plot.get_xticklabels() + plot.get_yticklabels()
    for item in labels:
        item.set_fontsize(font_size)
