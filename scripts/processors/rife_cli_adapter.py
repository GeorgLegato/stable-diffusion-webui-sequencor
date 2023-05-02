import os
import tempfile
from PIL import Image
from types import SimpleNamespace

from modules import scripts

usefulDirs = scripts.basedir().split(os.sep)[-2:]  # contains install and our extension foldername

def process(im1: Image,im2: Image, steps: int, ffprobepath: str):
    
    if (ffprobepath is not None and not ""):
        fixEnvPath(ffprobepath)

    folder = tempfile.mkdtemp("sequencor_")
    print (str(folder))

    stepfolders = []
    for i in range(steps):
        f = os.path.join(folder, "step"+str(i))
        os.mkdir(f)  # create a new directory for each step
        stepfolders.append(f)
    
    im1.save(os.path.join(stepfolders[0], "00000001.png"), "PNG")  # save image to temp dir for processing to work.
    im2.save(os.path.join(stepfolders[0], "00000002.png"), "PNG")  # save image to temp dir for processing to work.

    path = f"{usefulDirs[0]}/{usefulDirs[1]}/scripts/processors/RIFE"
    os.chdir(path)

    for i in range(steps-1):
        callRIFE(stepfolders[i],stepfolders[i+1])
 
    outv = os.path.join(folder, "interpolated.mp4")
    createVideo (stepfolders[-1], outv)
    return outv   # return path to output.mp4 file.
 
 
def callRIFE(folder1: str, folder2: str):
    os.system(f"rife-ncnn-vulkan.exe -i {folder1} -o  {folder2} -m rife-v4.6")

def createVideo(infolder, outfile):
    os.system(f"ffmpeg -framerate 30 -i {infolder}\%08d.png -c:a copy -crf 20 -c:v libx264 -pix_fmt yuv420p {outfile}")


def fixEnvPath(p):
    envpath = os.environ["PATH"]
    if p and not p in envpath:
        path_sep = ";" if os.name == "nt" else ":"
        os.environ["PATH"] = envpath + path_sep + p
