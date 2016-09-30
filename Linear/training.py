import numpy as np
import rawpy as rp
import imageio as iio
import numpy.linalg as la

# Read RGB values from the reference image and target image
tar_path = raw_input('Input the path of the target image:\n')
ref_path = raw_input('Input the path of the reference image:\n')
raw_ref = rp.imread(ref_path)
raw_tar = rp.imread(tar_path)
ref = raw_ref.postprocess()
tar = raw_tar.postprocess()
iio.imsave('reference.jpg',ref)
iio.imsave('target.jpg',tar)

# Read data from files
# (Approxiamate) Central positions of colored areas on the color chart
file = open('ref_color_area_ctr.txt')
ref_ctr = np.genfromtxt(file, delimiter = ',')
file.close()

file = open('tar_color_area_ctr.txt')
tar_ctr = np.genfromtxt(file, delimiter = ',')
file.close()

nr = ref_ctr.shape[0]
nt = tar_ctr.shape[0] # Foreknowledge: nr = nt = 24

# Sample from 24 colored areas on the color chart
# Take average over a 20*20 area in the colored square
ref_cset = np.zeros([nr,3])
tar_cset = np.zeros([nt,3])

for i in range(0,nr):
    ref_w = int(ref_ctr[i,0])
    ref_h = int(ref_ctr[i,1])
    tar_w = int(tar_ctr[i,0])
    tar_h = int(tar_ctr[i,1])
    ref_cset[i] = np.fix(np.mean(np.mean(ref[ref_h - 10:ref_h + 10,ref_w - 10:ref_w + 10],axis = 0),axis = 0))
    tar_cset[i] = np.fix(np.mean(np.mean(tar[tar_h - 10:tar_h + 10,tar_w - 10:tar_w + 10],axis = 0),axis = 0))

# White balacing
ref_w = ref_cset[nr - 1]
tar_w = tar_cset[nt - 1]
Wr = np.zeros([3,3])
Wt = np.zeros([3,3])
for i in range(0,3):
    Wr[i,i] = 255 / ref_w[i]
    Wt[i,i] = 255 / tar_w[i]

# Linear transformation matrix
D = np.matrix(np.empty([24,4]))
T = np.matrix(np.empty([4,3]))
ref_wb = np.matrix(ref_cset) * np.matrix(Wr)
tar_wb = np.matrix(tar_cset) * np.matrix(Wt)
D[:,0:3] = tar_wb
D[:,3] = np.ones([24,1])

vr = np.matrix(ref_wb[:,0])
vg = np.matrix(ref_wb[:,1])
vb = np.matrix(ref_wb[:,2])

ar,er,rr,sr = la.lstsq(D,vr)
ag,eg,rg,sg = la.lstsq(D,vg)
ab,eb,rb,sb = la.lstsq(D,vb)

T[:,0] = ar
T[:,1] = ag
T[:,2] = ab

np.savetxt('TransMatrix.txt',T,delimiter = ',')

# Executing transformation
tar_h = tar.shape[0]
tar_w = tar.shape[1]
tar_trans = np.empty([tar_h,tar_w,3])
temp = np.matrix(np.empty([tar_h,4]))

for i in range(0,tar_w):
    temp[:,0:3] = np.matrix(tar[:,i]) * np.matrix(Wt)
    temp[:,3] = np.ones([tar_h,1])
    tar_trans[:,i] = np.fix(temp * T * np.matrix(la.inv(Wr)))

np.clip(tar_trans,0,255,out = tar_trans)

# Export transformed target image
iio.imsave('result.jpg',tar_trans)
