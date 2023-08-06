import numpy as np
import matplotlib.pyplot as plt

from photonpy.cpp.context import Context
from photonpy.cpp.cspline import CSpline_Calibration, CSpline
from photonpy.cpp.gaussian import Gaussian,Gauss3D_Calibration
from photonpy.cpp.estimator import Estimator
from photonpy.cpp.estim_queue import EstimQueue
from photonpy.cpp.spotdetect import PSFConvSpotDetector, SpotDetectionMethods
import photonpy.utils.multipart_tiff as tiff
import math
from photonpy.smlm.psf import psf_to_zstack
from photonpy.smlm.util import imshow_hstack
import time

def generate_storm_movie(psf:Estimator, xyzI, numframes=100, 
                         imgsize=512, bg=5, p_on=0.1):
    
    frames = np.zeros((numframes, imgsize, imgsize), dtype=np.float32)
    on_counts = np.zeros(numframes, dtype=np.int32)

    for f in range(numframes):
        on = np.random.binomial(1, p_on, len(xyzI))

        roisize = psf.sampleshape[0]
        roipos = np.clip((xyzI[:,[1,0]] - roisize/2).astype(int), 0, imgsize-roisize)
        theta = np.zeros((len(xyzI),5)) # assuming xyzIb
        theta[:,0:4] = xyzI
        theta[:,[1,0]] -= roipos
        on_spots = np.nonzero(on)[0]

        rois = psf.ExpectedValue(theta[on_spots])
        
        frames[f] = ctx.smlm.DrawROIs((imgsize,imgsize), rois, roipos[on_spots])
        frames[f] += bg
        on_counts[f] = np.sum(on)

    return frames, on_counts


def process_movie(mov, spotDetector, roisize, ctx:Context):
    imgshape = mov[0].shape
    roishape = [roisize,roisize]
    
    img_queue, roi_queue = SpotDetectionMethods(ctx).CreateQueue(imgshape, roishape, spotDetector)
    
    t0 = time.time()

    for img in mov:
        img_queue.PushFrame(img)
   
    while img_queue.NumFinishedFrames() < len(mov):
        time.sleep(0.1)
    
    dt = time.time() - t0
    print(f"Processed {len(mov)} frames in {dt:.2f} seconds. {numframes/dt:.1f} fps")

    rois, data = roi_queue.Fetch()
    return rois,data


roisize = 12
w = 64
N = 2000
pixelsize = 0.1 #um/pixel
numframes = 1000
R = w*0.4
angle = np.random.uniform(0, 2 * math.pi, N)

print(f"Depth in z: {R*pixelsize} um")

xyzI = np.zeros((N,4))
xyzI[:,0] = R * np.cos(angle) + w / 2
xyzI[:,1] = np.linspace(w//2-R,w//2+R,N)
xyzI[:,2] = R * np.sin(angle) * pixelsize
xyzI[:,3] = 1000

plt.figure()
plt.scatter(xyzI[:,0],xyzI[:,2])
plt.title(f"Ground truth")

with Context(debugMode=False) as ctx:
    psf = Gaussian(ctx).CreatePSF_XYZIBg(roisize, Gauss3D_Calibration(), cuda=True)

    print("Generating SMLM example movie")
    mov_expval, on_counts = generate_storm_movie(psf, xyzI, numframes, 
                                          imgsize=w,bg=5, p_on=5 / N)
    print("Applying poisson noise")
    mov = np.random.poisson(mov_expval)

    plt.figure()
    plt.imshow(mov[0])
    plt.title("Frame 0")
    plt.colorbar()

    bgimg = mov[0]*0
    psf_zrange = np.linspace(-R*pixelsize,R*pixelsize,50)
    psfstack = psf_to_zstack(psf, psf_zrange)

    sd = PSFConvSpotDetector(psfstack, bgimg, minPhotons=20, maxFilterSizeXY=5, debugMode=False)
    
    rois_info, rois = process_movie(mov, sd, roisize, ctx)
    print(f"#spots: {len(rois)}")
    
    initial_guess = np.ones((len(rois), 5)) * [roisize/2,roisize/2,0,0,1]
    initial_guess[:,2] = psf_zrange[rois_info['z']]
    initial_guess[:,3] = np.sum(rois,(1,2))
    
    plt.figure()
    plt.hist(rois_info['z'],bins=50)
    plt.title('Z Position initial value')

    imshow_hstack(rois)

    """
    est_queue = EstimQueue(psf)
    est_queue.Schedule(rois, ids=np.arange(len(rois)), initial=initial_guess)
    est_queue.Flush()
    est_queue.WaitUntilDone()
    r = est_queue.GetResults()
    est_queue.Destroy()

    """
    
    estim, diag, traces = psf.Estimate(rois, initial=initial_guess)
    estim[:,0] += rois_info['x']
    estim[:,1] += rois_info['y']
    
    # TODO: proper likelihood test filtering
    estim = estim[ (estim[:,2]>psf.calib.zrange[0]) & (estim[:,2]<psf.calib.zrange[1]) ]

    plt.figure()    
    plt.scatter(estim[:,0], estim[:,2])
    plt.xlabel('X [pixels]'); plt.ylabel('Z [microns]')
    plt.title('Unfiltered X-Z section')
    
