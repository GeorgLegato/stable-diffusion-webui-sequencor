from modules import script_callbacks, scripts, shared
import os
import json 
import gradio as gr
from webui import wrap_gradio_gpu_call

usefulDirs = scripts.basedir().split(os.sep)[-2:]

def after_component(component, **kwargs):
    print ("welcome sequencor")



def create_interpol(im1,im2,steps, processor):
    print (f"{im1},{im2},{steps}")

def add_tab():
    # export all webui settings      
    #json_object = json.dumps(shared.opts.data, indent = 4) 
    with gr.Blocks(analytics_enabled=False, css="display:none;") as ui:
            #gr.HTML(value="<script id='sdwebui_sharedopts_script'>"+json_object+"</script>", elem_id="art-ui-tw-sh-options", elem_classes="hidden")

            with gr.Row():
                image1 =gr.Image(type="pil", label="Image #1")
                image2 =gr.Image(type="pil", label="Image #2")

            with gr.Row():    
                steps = gr.Slider(label="Interpolation steps (2^x)", minimum=1, maximum=8, value=1)
                processor = gr.Radio(choices=["F.I.L.M","Infinite Zoom"],value="F.I.L.M", label="Select processor")
                
            with gr.Row():
                generate_btn = gr.Button(value="Generate video", variant="primary")
                interrupt = gr.Button(value="Interrupt", elem_id="interrupt_training")

            with gr.Row():    
                output_video = gr.Video(label="Output").style(width=512, height=512)

            generate_btn.click(
                fn=wrap_gradio_gpu_call(create_interpol, extra_outputs=[None, "", ""]),
                inputs=[image1,image2,steps, processor],
                outputs=[output_video]
            )
    
    return [(ui, "Sequencor", "Sequencor")]

def on_ui_settings():
    section = ('sequencor', "Sequencor Settings")

    shared.opts.add_option("sequencor_cuda_dlls_path", shared.OptionInfo(
        "", "If empty, use sd-webui torch/cuda-resources. If problems, bring your own cuda path here ", gr.Textbox, {"interactive": True}, section=section))

    shared.opts.add_option("sequencor_url_model", shared.OptionInfo(
        "<a href='https://civitai.com/api/download/models/58973'>Download pretraind model from civitai</a>", "Download Model, unpack it into this extensionfolder/pretrained_models", gr.HTML, {}, section=section))

  
script_callbacks.on_ui_tabs(add_tab)
#script_callbacks.on_after_component(after_component)
script_callbacks.on_ui_settings(on_ui_settings)
