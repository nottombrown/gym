from base64 import b64decode
from io import BytesIO
import numpy as np
from PIL import Image, ImageFile, ImagePalette
from PIL.PngImagePlugin import PngImageFile

# We always write the string "SCIF" at the beginning of our SCIF file to identify it
_SCIF_HEADER = b"SCIF\r\n\r\n"

starcraft_screen_height = 480
starcraft_screen_width = 640

class StarCraftImageFile(ImageFile.ImageFile):
    """
    Used for quickly converting StarCraft screenbuffers to various formats
    """
    format = "SCIF"
    format_description = "StarCraft Image Format"


    # StarCraft uses a fixed 256 color palette. We keep the palette here for fast decoding.
    _palette_bytes = b'\x00\x00\x00##\xff##\xff##\xff##\xff##\xff##\xff##\xff\xff\x00\xff\xde\x00\xde\xbd\x00\xbd\x9c\x00\x9c|\x00|[\x00[:\x00:\x19\x00\x19,$\x18H$\x14\\,\x14p0\x14h<$|@\x18xL,\xa8\x08\x08\x8cT0\x84`D\xa0T\x1c\xc4L\x18\xbch$\xb4p<\xd0d \xdc\x944\xe0\x94T\xec\xc4T4D(@l<HlPL\x80PP\x8c\\\\\xa0x\x00\x00\x18\x00\x104\x00\x08P$4H0@T\x144|4Ll@XtHh\x8c\x00p\x9cX\x80\xa4@h\xd4\x18\xac\xb8$$\xfcd\x94\xbcp\xa8\xcc\x8c\xc0\xd8\x94\xdc\xf4\xac\xdc\xe8\xac\xfc\xfc\xcc\xf8\xf8\xfc\xfc\x00\xf4\xe4\x90\xfc\xfc\xc0\x0c\x0c\x0c\x18\x14\x10\x1c\x1c ((080$8<DL@0LLL\\P@XXXhhhx\x84lh\x94lt\xa4|\x98\x94\x8c\x90\xb8\x94\x98\xc4\xa8\xb0\xb0\xb0\xac\xcc\xb0\xc4\xc0\xbc\xcc\xe0\xd0\xf0\xf0\xf0\x1c\x10\x08(\x18\x0c4\x10\x084 \x0c8\x10 4( D4\x08H0\x18`\x00\x00T( P@\x14\\T\x14\x84\x04\x04hL4|80pd |PP\xa44\x1c\x94l\x00\x98\\@\x8c\x804\x98tT\xb8TD\xb0\x90\x18\xb0t\\\xf4\x04\x04\xc8xT\xfchT\xe0\xa4\x84\xfc\x94h\xfc\xcc,\x10\xfc\x18\x0c\x00 \x1c\x1c,$$L(,h,0\x84 \x18\xb84<\xachh\x94d\x90\xfc|\xac\xfc\x00\xe4\xfc\x9c\x90@\xa8\x94T\xbc\xa4\\\xcc\xb8`\xe8\xd8\x80\xec\xc4\xb0\xfc\xfc8\xfc\xfc|\xfc\xfc\xa4\x08\x08\x08\x10\x10\x10\x18\x18\x18(((444L<8DDDHHXXXhth8xd\\``|\x84tt\x84\x84\x9c\xac\x8c|\xac\x98\x94\x90\x90\xb8\xb8\xb8\xe8\xf8\x8c\x14\x10T< \x90p,\xb4\x94\x04 dH\x1cP\x084\x98h0x\x88@\x9c\x0cH\xcc\xbc\xb84\xdc\xdc<\x10\x00\x00$\x00\x004\x00\x00H\x00\x00`\x18\x04\x8c(\x08\xc8\x18\x18\xe0,,\xe8  \xe8P\x14\xfc  \xe8x$\xf8\xac<\x00\x14\x00\x00(\x00\x00D\x00\x00d\x00\x08\x80\x08$\x98$<\x9c<X\xb0Xh\xb8h\x80\xc4\x80\x94\xd4\x94\x0c\x14$$<d0P\x848\\\x94Ht\xb4T\x84\xc4`\x94\xd4x\xb4\xec\x04\x04\x04\x14\x14\x14$ \x1c  $$$(,,,,0404<48@<<<<@H@DLLPX```tpp||| \x18\x10<,\x18\x10\x10\x0c\x14\x14\x18\x18\x18\x1c \x1c\x18 \x18\x1c\x1c $$\x1c ( $$(,0$,(,4000,08<,4888D8,@0<D4@P<HHHHDHPHLTTPPPT\\dddpllxtt\x88\x84\x84##\xff##\xff##\xff##\xff##\xff##\xff##\xff##\xff##\xff\xff\xff\xff'

    global_palette = ImagePalette.raw("RGB", _palette_bytes)

    def _open(self):

        # Size in pixels (width, height)
        self.size = int(640), int(480)
        self.mode = "P"  # 8-bit palette-mapped image.
        self.palette = self.global_palette.copy()

        header = self.fp.read(8)
        if header[:8] != _SCIF_HEADER:
            raise SyntaxError("not a SCIF file")

        self.tile = [
            ("raw", (0, 0) + self.size, 8, (self.mode, 0, 1))
        ]

    def to_np_rgb(self):
        """
        Returns:
            A numpy tensor with shape (width, height, 3)
        """

        # Turn the SCIF into a PNG
        png_stream = BytesIO()
        self.save(png_stream, format='png')
        png_img = Image.open(png_stream)
        assert isinstance(png_img, PngImageFile)

        # Put the PNG into RGB mode
        png_rgb = png_img.convert('RGB')

        # TODO: remove this
        pixel = png_rgb.getpixel((0, 0))
        assert pixel == (36, 40, 44)

        # 307200 tuples of (R, G, B)
        pixels = np.array(png_rgb.getdata(), dtype=np.uint8)
        reshaped_pixels = pixels.reshape([starcraft_screen_height,
                                          starcraft_screen_width,
                                          3])
        return reshaped_pixels

    def to_obs(self):
        """
        Returns:
            A 480 x 640 matrix of uint8s representing a screen dump from a starcraft game
        """
        return np.array(self.getdata(), dtype=np.uint8).reshape([480, 640])

    @classmethod
    def from_screen_buffer(cls, screendump_bytes):
        """
        Args:
            screendump_bytes: The raw bytes generated by doing a screendump from StarCraft
        """
        stream = BytesIO(_SCIF_HEADER + screendump_bytes)
        return Image.open(stream)

    @classmethod
    def from_np_array(cls, np_matrix):
        """
        Args:
            np_matrix: A 480 x 640 matrix of uint8s
        """
        return cls.from_screen_buffer(bytearray(list(np_matrix.flatten())))

    @classmethod
    def from_b64_screen_buffer(cls, b64_screen_buffer):
        """
        Args:
            b64_screen_buffer: A base-64 encoding of a StarCraft screendump
        """
        return cls.from_screen_buffer(b64decode(b64_screen_buffer))


# Register with ImageFile loaders
def _accept(prefix):
    return prefix[:8] == _SCIF_HEADER

Image.register_open("SCIF", StarCraftImageFile, _accept)
Image.register_extension("SCIF", ".scif")


