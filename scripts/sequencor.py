import os
import json 
from modules import script_callbacks, scripts, shared, sd_models
import gradio as gr
from webui import wrap_gradio_gpu_call

from scripts.processors import film_cli_adapt,rife_cli_adapter

usefulDirs = scripts.basedir().split(os.sep)[-2:]

def after_component(component, **kwargs):
    print ("welcome sequencor")

def unloadModel():
    sd_models.unload_model_weights()

def create_interpol(im1,im2,steps, processor, doUnloadModel: bool, multiple, folder) -> str:
    print (f"{im1},{im2},{steps},{processor}")
    
    if (processor == "F.I.L.M"):
        if doUnloadModel:
            unloadModel()
                    
        video_path = film_cli_adapt.process(im1,im2,steps, shared.opts.data.get("sequencor_cuda_dlls_path"), shared.opts.data.get("sequencor_ffprobepath"))
        return video_path
    elif (processor == "RIFE"):
        if doUnloadModel:
            unloadModel()
                    
        video_path = rife_cli_adapter.process(im1,im2,steps, shared.opts.data.get("sequencor_ffprobepath"),shared.opts.data.get("sequencor_rifeexe"))
        return video_path
    else:
        raise gr.Error (f"Processoe {processor} is not supported")




def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths

def add_tab():
    # export all webui settings      
    #json_object = json.dumps(shared.opts.data, indent = 4) 
    with gr.Blocks(analytics_enabled=False, css="display:none;") as ui:
            #gr.HTML(value="<script id='sdwebui_sharedopts_script'>"+json_object+"</script>", elem_id="art-ui-tw-sh-options", elem_classes="hidden")

            with gr.Row():
                multifile_output = gr.File()
                uploadMulti  = gr.UploadButton("Click to Upload Files", file_types=["image"], file_count="multiple")
                uploadMulti.upload(upload_file, uploadMulti, multifile_output)

                uploadFolder = gr.UploadButton("Click to Upload Files", file_types=["folder"], file_count="multiple")


                image1 =gr.Image(type="pil", label="Image #1")
                image2 =gr.Image(type="pil", label="Image #2")

            with gr.Row():    
                steps = gr.Slider(label="Interpolation steps (2^x)", minimum=1, maximum=16, value=1, step=1)
                processor = gr.Radio(choices=["RIFE","F.I.L.M","Infinite Zoom"],value="RIFE", label="Select processor")
                unload_model = gr.Checkbox(value=True,label="Unload model to free VRAM for processing")
                
            with gr.Row():
                generate_btn = gr.Button(value="Generate video", variant="primary")
                interrupt = gr.Button(value="Interrupt", elem_id="interrupt_training")

            with gr.Row():    
                output_video = gr.Video(label="Output").style(width=512, height=512)

            generate_btn.click(
                fn=create_interpol,
                inputs=[image1,image2,steps, processor, unload_model, uploadMulti, uploadFolder],
                outputs=output_video
            )
    
    return [(ui, "Sequencor", "Sequencor")]

def on_ui_settings():
    section = ('sequencor', "Sequencor Settings")

    shared.opts.add_option("sequencor_url_ffmpeg", shared.OptionInfo(
        "<H2>FFMPEG: <a href='https://github.com/BtbN/FFmpeg-Builds/releases'>Download FFMPEG/FFPROBE for your OS (static compiled, large version)</a>", "Download, unpack it somewhere and enter tha path below", gr.HTML, {}, section=section))

    shared.opts.add_option("sequencor_ffprobepath", shared.OptionInfo(
        "", "Point to your FFMPEG/FFPROBE installation path",
        gr.Textbox, {"interactive": True}, section=section,)
    )

    shared.opts.add_option("sequencor_hr", shared.OptionInfo("<p><hr><p>","", gr.HTML, {}, section=section))

    shared.opts.add_option("sequencor_url_film_model", shared.OptionInfo(
        "<H2>FILM: <a href='https://civitai.com/api/download/models/58973'>Download pretrained model from civitai</a>", "Download Model, unpack it into this extensionfolder/processors/FILM/pretrained_models", gr.HTML, {}, section=section))

    shared.opts.add_option("sequencor_cuda_dlls_path", shared.OptionInfo(
        "", "If empty, use sd-webui torch/cuda-resources. If problems, bring your own cuda path here ", gr.Textbox, {"interactive": True}, section=section))

    shared.opts.add_option("sequencor_hr2", shared.OptionInfo("<p><hr><p>", "",gr.HTML, {}, section=section))

    shared.opts.add_option("sequencor_url_rife", shared.OptionInfo(
        "<H2>RIFE: <a href='https://github.com/nihui/realsr-ncnn-vulkan/releases'>Download your os variant of RIFE</a>", "Unpack it into this extensionfolder/processors/RIFE", gr.HTML, {}, section=section))

    shared.opts.add_option("sequencor_rifeexe", shared.OptionInfo(
        "rife-ncnn-vulkan.exe", "Name of the rife executable in above installation path.",
        gr.Textbox, {"interactive": True}, section=section,)
    )
  
script_callbacks.on_ui_tabs(add_tab)
#script_callbacks.on_after_component(after_component)
script_callbacks.on_ui_settings(on_ui_settings)
