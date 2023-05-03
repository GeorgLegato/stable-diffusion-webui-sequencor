import os
import tempfile
from PIL import Image
from types import SimpleNamespace

from modules import scripts

usefulDirs = scripts.basedir().split(os.sep)[-2:]  # contains install and our extension foldername
cwd_old=None

def process(im1: Image,im2: Image, steps: int, ffprobepath: str, RIFEEXE: str):
    
    assert RIFEEXE is not None,"Sequencor: RIFE: Please define the name of rife executable in settings"
    assert RIFEEXE is not "",  "Sequencor: RIFE: Please define the name of rife executable in settings"
    
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

    set_cwd()
    try:
        for i in range(steps-1):
            callRIFE(stepfolders[i],stepfolders[i+1], RIFEEXE)
    except Exception:
        restore_cwd()
        pass
    restore_cwd()

    outv = os.path.join(folder, "interpolated.mp4")

    createVideo (stepfolders[-1], outv)
    return outv   # return path to output.mp4 file.
 
 
def set_cwd():
    global cwd_old
    cwd_old=os.getcwd()
    path = f"{usefulDirs[0]}/{usefulDirs[1]}/scripts/processors/RIFE"
    os.chdir(path)

def restore_cwd():
    global cwd_old
    os.chdir(cwd_old)
 
def callRIFE(folder1: str, folder2: str, r):
    os.system(f"{r} -i {folder1} -o  {folder2} -m rife-v4.6")
    workaround_del_last_image(folder2)


def workaround_del_last_image(directory_path):

    files = os.listdir(directory_path)

    latest_file = None
    latest_file_mtime = -1

    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime > latest_file_mtime:
                latest_file = file
                latest_file_mtime = file_mtime

    if latest_file:
        file_to_delete = os.path.join(directory_path, latest_file)
        os.remove(file_to_delete)
        print(f"Die Datei {latest_file} wurde gelöscht.")
    else:
        print(f"Keine Datei im Verzeichnis {directory_path} gefunden.")

def createVideo(infolder, outfile):
    os.system(f"ffmpeg -framerate 30 -i {infolder}\%08d.png -c:a copy -crf 20 -c:v libx264 -pix_fmt yuv420p {outfile}")

def fixEnvPath(p):
    envpath = os.environ["PATH"]
    if p and not p in envpath:
        path_sep = ";" if os.name == "nt" else ":"
        os.environ["PATH"] = envpath + path_sep + p
