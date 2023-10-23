from PIL import Image
from numpy import *
from pylab import *
from scipy import stats
import scipy.ndimage as scimage# measurements,morphology
import matplotlib.pyplot as plt

def count_items(img1_f, it):
  im_open = scimage.binary_opening( \
    img1_f,ones((9,5)), iterations=it)
  labels_open, nbr_objects_open = scimage.label(im_open)
  return labels_open


def fn(img_name,filt):
  img1 = Image.open(img_name).transpose(Image.FLIP_TOP_BOTTOM)
  rgb2xyz = (
    1, 0, 0, 0,
    1, 0, 0, 0,
    1, 0, 0, 0 )
  img1 = img1.convert("RGB", rgb2xyz)
  img1 = array(img1.convert('L'))
  img1 = histeq(img1)

  img1_f = 1 * (img1 > filt)

  return img1_f


def histeq(im,nbr_bins=256):
  data = im.flatten()
  imhist,bins = histogram(data, nbr_bins, normed=True)
  cdf = imhist.cumsum()
  cdf = 255 * cdf
  im2 = interp(im.flatten(), bins[:-1], cdf)
  return im2.reshape(im.shape)

def fig(img_name,filt, it):
  clf()
  imshow(Image.open(img_name))

  gray()
  contour(count_items(fn(img_name,filt), it), origin='image')
  show()


# 47

img = Image.open("captured_image.jpg").transpose(Image.FLIP_TOP_BOTTOM)
print(img)
# img1 = Image.open(img_name)
rgb2xyz = (
    1, 0, 0, 0,
    1, 0, 0, 0,
    1, 0, 0, 0 )
img1 = img.convert("RGB", rgb2xyz)
img1 = array(img1.convert('L'))
img1 = np.array(Image.open("captured_image.jpg").convert("L"))
a_min = stats.scoreatpercentile(img1, 5)
a_max = stats.scoreatpercentile(img1, 95)
print(a_min,a_max)

# img_f = fn("captured_image.jpg",90)
# Get brightness range - i.e. darkest and lightest pixels
# min=np.min(img1)        # result=144
# max=np.max(img1)        # result=216

# Make a LUT (Look-Up Table) to translate image values
LUT=np.zeros(256,dtype=np.uint8)
LUT[int(a_min):int(a_max)+1]=np.linspace(start=0,stop=255,num=int(a_max-a_min)+1,endpoint=True,dtype=np.uint8)

img_f = LUT[img1]
# Apply LUT and save resulting image
Image.fromarray(img_f).save('enhanced_image.jpg')

fig("enhanced_image.jpg",90, 3)

plt.imshow(img_f)

sx = scimage.sobel(img_f, axis=0, mode='constant')
sy = scimage.sobel(img_f, axis=1, mode='constant')
sob = np.hypot(sx, sy)
# plt.imshow(sob)
plt.show()