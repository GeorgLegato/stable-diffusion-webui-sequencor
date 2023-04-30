from modules import script_callbacks, scripts, shared
import os
import gradio as gr
import json 

usefulDirs = scripts.basedir().split(os.sep)[-2:]

def after_component(component, **kwargs):
    print ()"welcome sequencor")


def add_tab():

    # export all webui settings      
    json_object = json.dumps(shared.opts.data, indent = 4) 
    with gr.Blocks(analytics_enabled=False, css="display:none;") as ui:
            V = gr.HTML(value="<script id='sdwebui_sharedopts_script'>"+json_object+"</script>", elem_id="art-ui-tw-sh-options", elem_classes="hidden")

    return [(ui, "Sequencor", "Sequencor")]

def on_ui_settings():
    section = ('sequencor', "Sequencor Settings")

    shared.opts.add_option("sequencor_param1", shared.OptionInfo(
        True, "Move quicksettings to image setting panel ", gr.Checkbox, {"interactive": True}, section=section))

    shared.opts.add_option("sequencor_param2", shared.OptionInfo(
        True, "Bring prompts and setting into one column left side ", gr.Checkbox, {"interactive": True}, section=section))

    shared.opts.add_option("sequencor_param3", shared.OptionInfo(
        1, "If setting2prompt width, which width-ratio between both columns (0: minimize setting, 1: 50/50,  6: minimize output gallery column)", gr.Slider, {"minimum": 0, "maximum": 6, "step": 0.1}, section=section))

    shared.opts.add_option("sequencor_param4", shared.OptionInfo(
        50, "Gallery height in _absolute_ percent of your screen (not remaining height)", gr.Slider, {"minimum": 0, "maximum": 100, "step": 10}, section=section))
  
script_callbacks.on_ui_tabs(add_tab)
script_callbacks.on_after_component(after_component)
script_callbacks.on_ui_settings(on_ui_settings)
