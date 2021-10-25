# COS737 Assignment 3
# Ezra Fielding, 3869003

import numpy as np
from numpy.fft import fft2, ifft2
import tifffile
from PIL import Image

class StegCrypt(object):
    """
    Information Hiding with Data Diffusion using Convolutional
    Encoding for Super-encryption. Hides an image, the 'Plaintext',
    in a chosen camouflage image, the 'Covertext' to produce a
    'Stegotext' image. Also performs decryption of the stegotext
    image using the input covertext as a key.

    Code adapted from:
    Blackledge, J., Tobin, P., Myeza, J. and Adolfo,
    C.M., 2017. Information Hiding with Data Diffusion
    Using Convolutional Encoding for Super-Encryption.
    """

    # Hidden utility functions
    def _key_generator(self, channel):
        channel = channel * 1e10
        # 32-bit integer required for random seed in numpy
        key = int(np.floor(np.sqrt(np.sum(channel ** 2)))
        % 2 ** 32)
        return key
    
    def _hide_data(self, covertext, sdiffuse, c):
        return ifft2(c * fft2(sdiffuse) + fft2(covertext)).real
    
    def _recover_data(self, covertext, stegotext):
        return ifft2(fft2(stegotext) - fft2(covertext)).real
    
    def _image_diffusion(self, plaintext, covertext):
        plaintext = fft2(plaintext)
        covertext = fft2(covertext)
        p = np.abs(covertext ** 2)
        p[p == 0] = 1.
        diffuse = plaintext * covertext / p
        diffuse = ifft2(diffuse).real
        return diffuse / diffuse.max()
    
    def _inverse_image_diffusion(self, diffuse, covertext):
        diffuse = fft2(diffuse)
        covertext = fft2(covertext)
        plaintext = covertext.conj() * diffuse
        plaintext = ifft2(plaintext).real
        return plaintext / plaintext.max()
    
    def _stochastic_diffusion(self, diffuse, key):
        np.random.seed(key)
        arr_noise = fft2(np.random.rand(*diffuse.shape))
        p = np.abs(arr_noise ** 2)
        p[p == 0] = 1
        diffuse = fft2(diffuse)
        sdiffuse = diffuse * arr_noise / p
        sdiffuse = ifft2(sdiffuse).real
        return sdiffuse / sdiffuse.max()
    
    def _inverse_stochastic_diffusion(self, sdiffuse, key):
        np.random.seed(key)
        noise = fft2(np.random.rand(*sdiffuse.shape))
        sdiffuse = fft2(sdiffuse)
        diffuse = noise.conj() * sdiffuse
        diffuse = ifft2(diffuse).real
        return diffuse / diffuse.max()
    
    def encrypt(self, plaintext, covertext):
        """
        Hides the plaintext image within the provided covertext image
        Parameters
        ==========
            plaintext : array-like, shape (rows, columns, channels)
                        The plaintext image to hide.
                        Values must be ranging from 0 to 1
            covertext : array-like, shape (rows, columns, channels)
                        The covertext image in which to hide the plaintext.
            Values must be ranging from 0 to 1
                        Information Hiding with Data Diffusion using ... 347
        Returns
        =======
            stegotext : array-like, shape (rows, columns, channels)
                        The stegotext image
        """
        c = 0.0001
        if len(covertext.shape) != 2 and len(covertext.shape) != 3:
            raise Exception(ValueError, \
            "Input arrays must be 2- or 3-dimensional")

        # Ensure inputs have the same shape
        if not np.array_equal(covertext.shape, plaintext.shape):
            raise Exception(ValueError, \
            "Covertext and Plaintext shape do not match")

        covertext_2D = False
        if len(covertext.shape) == 2:
            covertext = covertext[:, :, None]
            plaintext = plaintext[:, :, None]
            covertext_2D = True
            
        # Ensure images are 64-bit floating point
        plaintext = plaintext.astype('float64')
        covertext = covertext.astype('float64')
        stegotext = np.zeros_like(covertext)

        for i in range(plaintext.shape[-1]):
            plaintext_channel = plaintext[:, :, i]
            covertext_channel = covertext[:, :, i]
            key = self._key_generator(covertext_channel)

            # Hide each of the channels
            diff = self._image_diffusion(plaintext_channel,covertext_channel)
            sdiff = self._stochastic_diffusion(diff, key)
            stegotext[:, :, i] = self._hide_data(covertext_channel,sdiff, c)
        
        if covertext_2D:
            stegotext = stegotext[:, :, 0]
        return stegotext
    
    def decrypt(self, stegotext, covertext):
        """
        Hides the plaintext image within the provided
        covertext image
        Parameters
        ==========
            stegotext : array-like, shape (rows, columns, channels)
                        The stegotext image in which the plaintext
                        image is hidden.
            covertext : array-like, shape (rows, columns, channels)
                        The covertext image (the key)
                        Values must be ranging from 0 to 1
        Returns
        =======
            plaintext : array-like, shape (rows, columns, channels)
                        The hidden plaintext image
        """

        if len(covertext.shape) != 2 and len(covertext.shape) != 3:
            raise Exception(ValueError, \
            "Input arrays must be 2- or 3-dimensional")

        # Ensure inputs have the same shape
        if not np.array_equal(covertext.shape, stegotext.shape):
            raise Exception(ValueError, \
            "Covertext and Stegotext shape do not match")

        covertext_2D = False
        if len(covertext.shape) == 2:
            covertext = covertext[:, :, None]
            stegotext = stegotext[:, :, None]
            covertext_2D = True

        stegotext = stegotext.astype('float64')
        covertext = covertext.astype('float64')
        plaintext = np.zeros_like(stegotext)

        for i in range(stegotext.shape[-1]):
            covertext_channel = covertext[:, :, i]
            stegotext_channel = stegotext[:, :, i]
            key = self._key_generator(covertext_channel)

            # Recover the plaintext channel
            sdiff = self._recover_data(covertext_channel,\
            stegotext_channel)
            diff = self._inverse_stochastic_diffusion(sdiff, key)
            plaintext[:, :, i] = \
            self._inverse_image_diffusion(diff, covertext_channel)
        
        if covertext_2D == True:
            plaintext = plaintext[:, :, 0]

        return plaintext
    
    def save_stegotext_tiff(self, stegotext, filename):
        """
        Save stegotext as tiff file
        Parameters
        ==========
            stegotext : array-like, shape (rows, columns, channels)
                        The stegotext to save
            filename : str
                       The filename to save the stegotext
        Returns
        =======
            self : object
        """

        tifffile.imsave(filename, stegotext)
        return self

    def save_image(self, image, filename):
        """
        Save image as jpeg file
        Parameters
        ==========
            image : array-like, shape (rows, columns, channels)
                    The image to save
            filename : str
                       The filename to save the image
        Returns
        =======
            self : object
        """
        # Rescales Image and converts to uint8 for PIL
        rescale = (255.0 / image.max() * (image - image.min())).astype(np.uint8)
        # Saves Image
        Image.fromarray(rescale).save(filename)
        return self

    def open_stegotext_tiff(self, filename):
        """
        Open a stegotext from a tiff file
        Parameters
        ==========
            filename : str
                       The filename to of the stegotext image
        Returns
        =======
            stegotext : array-like, shape (rows, columns, channels)
                        The stegotext array
        """
        # Checks if file name is empty
        if filename == "":
            # Raises exception if filename is missing
            raise Exception(IOError, "No file selected")

        stegotext = tifffile.imread(filename)

        if stegotext.dtype != 'float64':
            raise Exception(IOError, "Improperly saved stegotext file")

        return stegotext

    def open_img(self, filename):
        """
        Open a image from a file
        Parameters
        ==========
            filename : str
                       The filename to of the stegotext image
        Returns
        =======
            img_array : array-like, shape (rows, columns, channels)
                        The image array
        """
        # Checks if file name is empty
        if filename == "":
            # Raises exception if filename is missing
            raise Exception(IOError, "No file selected")
        # Open Image File
        image = Image.open(filename)
        # COnvert Image to array
        img_array = np.array(image, dtype=np.float64)
        # Normalizes image array if required
        if img_array.max() > 1.0:
            img_array /= 255

        return img_array