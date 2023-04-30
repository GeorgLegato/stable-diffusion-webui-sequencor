import tempfile

import scripts.processors.FILM.interpolator_cli as interpolate_cli

def process(im1,im2,steps, cudapath):
    folder = tempfile.mkdtemp("sequencor_")
    print (folder.name)
    
    interpolator_cli.main(["hi there"])
    