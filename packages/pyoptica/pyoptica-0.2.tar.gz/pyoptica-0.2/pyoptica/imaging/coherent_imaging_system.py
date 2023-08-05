import warnings

import astropy.units as u
import numpy as np

from .. import logging
from .. import utils
from .. import zernikes
from ..wavefront import Wavefront


class CoherentImagingSystem(logging.LoggerMixin, object):
    """ A class representing fully coherent imaging systems. It is based
    on reasoning presented in [1] and [2] (numerical implementation
    suggested in Chapter 7 [3]). An optical system composed of many optical
    elements can be described by one function that _aggregates_ all properties
    of them all. In case of coherent imaging the, the image is found based on
    (eqs. 5.37-5.40 in [1], the naming convention follows that given in
    [1] *Introduction to Fourier Optics* by J.W. Goodman)

    :math:`U_{i}(u, v)=h(u, v) \otimes U_{g}(u, v),`

    where:

    :math:`U_{i}(u, v)` — the field at the image plane,
    :math:`U_{g}(u, v)` —  ideal geometrical-optics image,
    :math:`h(u, v)` — amplitude impulse function aka point-spread function

    If an imaging system is analyzed in frequency domain the equation above
    becomes (based on the convolution theorem, eqs. 6.16-6.18 in [1]):

    :math:`G_{i}(f_{U}, f_{V})=H(f_{U}, f_{V}) G_{g}(f_{U}, f_{V}),`

    where:

    :math:`G_{i}(f_{U}, f_{V}) = \mathfrak{F} \{ U_{i}(u, v)\}`

    :math:`G_{g}(f_{U}, f_{V}) = \mathfrak{F} \{ U_{g}(u, v)\}`

    :math:`H(f_u, f_v) = \mathfrak{F} \{h(u, v)\}` — Amplitude Transfer Fuction

    *THE IMAGING SYSTEM HAS A CIRCULAR APERTURE!*

    :param wavelength: Wavelength used in simulations
    :type wavelength: astropy.Quantity of type length
    :param pixel_scale: Sampling of the wavefront
    :type pixel_scale: astropy.Quantity of type 1/length
    :param npix: Number of pixels in the wavefront array
    :type npix: int
    :param m: transverse magnification of the optical system
    :type m: float
    :param na: numerical aperture defined as :math:`NA = sin\theta_{max}`
    :type na: float
    :param n_o: refractive index on the object side
    :type n_o: float
    :param n_i: refractive index on the image side
    :type n_i: float


    **Example**

    >>> import astropy.units as u
    >>> import pyoptica as po
    >>>
    >>> wavelength = 1 * u.um
    >>> pixel_scale = 10 * u.mm
    >>> npix = 1024
    >>> img_sys = po.CoherentImagingSystem(wavelength, pixel_scale, npix)

    **References**

    [1] Joseph W. Goodman (2004) -
    *Introduction to Fourier Optics*, W. H. Freeman

    [2] Kedar Khare (2016) -
    *Fourier Optics and Computational Imaging*, Wiley&Sons Ltd.

    [3] David Voelz (2011) -
    *Computational Fourier Optics Matlab Tutorial*, Spie Press

    [4] M. Born, E. Wolf (1980) -
    *Principles of Optics*, Pergamon Press (Oxford UK)

    """

    @u.quantity_input(wavelength=u.m, pixel_scale=u.m)
    def __init__(self, wavelength, pixel_scale, npix, m=1, na=1, n_o=1, n_i=1):
        self.wavelength = wavelength
        self.pixel_scale = pixel_scale
        self.npix = npix
        self.m = m
        self.na = na
        self.n_o = n_o
        self.n_i = n_i

        self.x, self.y = utils.mesh_grid(npix, pixel_scale)

        self.H = None  # Amplitude Transfer Function
        self.zernikes = dict()
        self.apodization = None

    @property
    def psf(self):
        """Calculates amplitude point-spread function (Goodman naming
        convention).

        **Example**

        >>> import astropy.units as u
        >>> import pyoptica as po
        >>>
        >>> wavelength = 1 * u.um
        >>> pixel_scale = 10 * u.mm
        >>> npix = 1024
        >>> img_sys = po.CoherentImagingSystem(wavelength, pixel_scale, npix)
        >>> img_sys.calc_H() #  Amplitude transfer function must be calculated!
        >>> img_sys.psf

        """
        if self.H is None:
            warnings.warn('Please run `calc_H` first!')
            return None
        return utils.ifft(self.H)

    @property
    def cutoff_frequency(self):
        """Gives the highest spatial frequency transmitted by the system"""
        return self.na / self.wavelength

    def calc_H(self):
        """Calculates Amplitude Transfer Function H based on the current state of
        the object (numerical aperture, magnification, aberrations,
        apodization).

        **Example**

        >>> import astropy.units as u
        >>> import pyoptica as po
        >>>
        >>> wavelength = 1 * u.um
        >>> pixel_scale = 10 * u.mm
        >>> npix = 1024
        >>> img_sys = po.CoherentImagingSystem(wavelength, pixel_scale, npix)
        >>> img_sys.calc_H() #  Pupil has to be precalculated!
        >>> img_sys.H

        """
        H_ideal = self._calc_diffraction_limited_H()
        H = self._apply_radiometric_correction(H_ideal)
        H_with_aberrations = self._apply_aberrations(H)
        self.H = H_with_aberrations

    @property
    def f(self):
        f = utils.space2freq(self.x)
        return f

    @property
    def g(self):
        g = utils.space2freq(self.y)
        return g

    def _calc_diffraction_limited_H(self):
        """
        The diffraction limited Amplitude Transfer Function is calculated:

        :math:`\left\{\begin{matrix} 1, & \text{if } f^2 +g^2 < f_0^2 \\ 0, & \text{otherwise} \end{matrix}\right.`

        :return: Diffraction limited Amplitude Transfer Function
        :rtype: np.array

        """
        rho_squared = self.f ** 2 + self.g ** 2
        H = np.where(rho_squared < self.cutoff_frequency ** 2, 1, 0)
        return H

    def _apply_radiometric_correction(self, H_ideal):
        """ If there is magnification (or reduction) in the system, the
        distribution of light entering the system will be different than the
        distribution leaving it. In order to include that in the Amplitude
        Transfer Function H, a radiometric correction has to be applied
        (following M. Born and E. Wolf [4]):

        :math:`\left ( \frac{1 - \lambda^2(f^2 +g^2)M^2}{1 - \lambda^2(f^2 +g^2)}\right )^{0.25}`

        :param H_ideal: diffraction limited Amplitude Transfer function
        :type H_ideal: np.array
        :return: Amplitude Transfer Function with radiometric correction
        :rtype: np.array

        """
        rho_squared = self.f ** 2 + self.g ** 2
        numerator = 1 - (
                    self.wavelength ** 2 * rho_squared) * self.m ** 2 / self.n_o ** 2
        denominator = 1 - (self.wavelength ** 2 * rho_squared) / self.n_i ** 2
        r = numerator / denominator
        H = np.power(H_ideal * r, 0.25)
        H = H.to(u.dimensionless_unscaled).value
        #  Maybe it would make more sense to raise an exception if NA > n
        H[~np.isfinite(H)] = 0
        return H

    def _apply_aberrations(self, H):
        """Apply aberrations from `self.zernikes` to the amplitude transfer
        function (H):

        :math:`H=H_d \cdot \exp(2 \pi i W)`

        Where `H_d` is the diffraction limited transfer function, and `W` the
        calculated wavefront.

        :param H: The diffraction limited H
        :type H: np.array
        :return: amplitude transfer function with aberrations
        :rtype: np.array

        """
        rho, theta = utils.cart2pol(self.f, self.g)
        rho = rho.to(1 / u.m) / self.cutoff_frequency.to(1 / u.m)
        wf = zernikes.construct_wavefront_from_js(self.zernikes, rho, theta)
        return H * np.exp(2.j * np.pi * wf)

    def image_wavefront(self, wf):
        """ A method to image given wavefront using:

        :math:`U_{i}(u, v)=h(u, v) \otimes U_{g}(u, v),`

        using the convolution theorem the equation is solved in the frequency
        domain:

        :math:`G_{i}(f_{U}, f_{V})=Hf(_{U}, f_{V}) G_{g}(f_{U}, f_{V}),`

        :param wf: Input wavefront
        :type wf: pyoptica.Wavefront
        :return: wavefront in the image plane;
        :rtype: pyoptica.Wavefront

        **Example**

        >>> import astropy.units as u
        >>> import pyoptica as po
        >>>
        >>> wavelength = 1 * u.um
        >>> pixel_scale = 10 * u.mm
        >>> npix = 1024
        >>> img_sys = CoherentImagingSystem(wavelength, pixel_scale, npix)
        >>> wf = Wavefront(wavelength, 1/pixel_scale/npix, npix)
        >>> imaged_wf = img_sys.image_wavefront(wf)
        >>> imaged_wf

        """
        if self.H is None:
            self.calc_H()
        self._check_wavefront_compatibility(wf)

        field_fft = utils.fft(wf.wavefront)
        multiplied = field_fft * self.H
        imaged_field = utils.ifft(multiplied)
        pix_scale = self.pixel_scale * self.m
        imaged_wavefront = Wavefront(self.wavelength, pix_scale, self.npix)
        imaged_wavefront.wavefront = imaged_field
        return imaged_wavefront

    def _check_wavefront_compatibility(self, wf):
        """Checks if wavefront is compatible with the system

        :param wf: Wavefront
        :type wf: pyoptica.Wavefront
        :raises: RuntimeError

        """
        if self.npix != wf.npix:
            raise RuntimeError('Imaging system npix != wavefront npix'
                               f'{self.npix} != {wf.npix}')
        if self.wavelength != wf.wavelength:
            raise RuntimeError(
                'Imaging system wavelength != wavefront wavlength'
                f'{self.wavelength} != {wf.wavelength}')
        if self.pixel_scale != wf.pixel_scale:
            raise RuntimeError(
                'Imaging system wavelength != wavefront wavlength'
                f'{self.pixel_scale} != {wf.pixel_scale}')

    def load_apodization(self, apodization):
        """"TODO: implement apodization"""
        pass
