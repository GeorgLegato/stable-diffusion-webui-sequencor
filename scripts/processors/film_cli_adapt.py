import os.path
import tempfile
from PIL import Image
from types import SimpleNamespace

import scripts.processors.FILM.interpolator_cli as interpolate_cli
from modules import scripts

usefulDirs = scripts.basedir().split(os.sep)[-2:]  # contains install and our extension foldername

def process(im1: Image,im2: Image, steps: int, cudapath: str, ffprobepath: str):
    
    if (cudapath is not None and not ""):
        fixEnvPath(cudapath)
    if (ffprobepath is not None and not ""):
        fixEnvPath(ffprobepath)

    
    folder = tempfile.mkdtemp("sequencor_")
    print (str(folder))
    
    im1.save(os.path.join(folder, "1.png"), "PNG")  # save image to temp dir for processing to work.
    im2.save(os.path.join(folder, "2.png"), "PNG")  # save image to temp dir for processing to work.
    
    model_path=f"./{usefulDirs[0]}/{usefulDirs[1]}/scripts/processors/FILM/pretrained_models/film_net/Style/saved_model"

    interpolate_cli._PATTERN = SimpleNamespace(value= str(folder))
    interpolate_cli._MODEL_PATH = SimpleNamespace(value=model_path)
    interpolate_cli._TIMES_TO_INTERPOLATE = SimpleNamespace(value=steps)
    interpolate_cli._FPS = SimpleNamespace(value= 30)
    interpolate_cli._ALIGN = SimpleNamespace(value=64)
    interpolate_cli._BLOCK_HEIGHT = SimpleNamespace(value= 1)
    interpolate_cli._BLOCK_WIDTH = SimpleNamespace(value=1)
    interpolate_cli._OUTPUT_VIDEO = SimpleNamespace(value=True)

    interpolate_cli.main( [f"--pattern {str(folder)} --model {model_path} --times_to_interpolate {str(steps)}"])
 
    return os.path.join(folder, "interpolated.mp4")  # return path to output.mp4 file.
 
 
    
def fixEnvPath(p):
    envpath = os.environ["PATH"]
    if p and not p in envpath:
        path_sep = ";" if os.name == "nt" else ":"
        os.environ["PATH"] = envpath + path_sep + p

    """
$env:Path +=";s:\KI\frame-interpolation\cuda\bin;s:\KI\frame-interpolation\cuda\include;s:\KI\frame-interpolation\cuda\lib;"
python -m eval.interpolator_cli  --pattern s:\KI\GL_ImageBlender_CSS\img --model_path pretrained_models/film_net/Style/saved_model --times_to_interpolate 1 
ffmpeg -framerate 30 -i frame_%03d.png -c:v libx264 -pix_fmt yuv420p output.mp4
    
    """
