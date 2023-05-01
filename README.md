# stable-diffusion-webui-sequencor
Work in progress: An extension for StableDiffusion WebUI - Automatic1111 and Vladmandic´s cut.

It takes any image sequence and process *some* interpolation between them in order to generate animations into movie file.

First processors will be Google F.I.L.M to interpolate semantically between images in a soft way.
Second idea is to have the interpolation routine from InfiniteZoom on board, to rework/rerun a video if there small glithces to be fixed.

# Example screenshots
![image](https://user-images.githubusercontent.com/7210708/235451383-954460ed-27cb-433e-a523-b717f4558a5e.png)


# Installation
Very poor, yet:
Development is currrently using Vladmandics WebUi-Fork. 
The contained "install.py" is somehow not called or just not processing the requirements.txt.

* install extension via url 
* in settings of that extension is a URL, download the model-zip (from civitai. https://civitai.com/models/54606)
* unzip it to this_extensionfolder/scripts/processors/FILM    (creates pretrained_models folder)
* open terminal, cd to vlad/
* ```venv\Scripts\activate```
* ```cd extensions/stable-diffusion-webui-sequencor```
* ```pip install -r requirements.txt``` (needs torchvision, some cli tools)
* restart vlad/auto1111

good luck

## Settings
nothing to set so far.


## known bugs
* after interpolation FILM, VRAM is occupied by this model. need a unload-button or - mechanism
* Infinite Zoom not implemented

### Extension-Setting-Tab



