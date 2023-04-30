// in case javascript needs to access setting from webui/python
function getopt(optnanme, defaultValue = true) {
    if (sdwebui_sharedopts[optnanme] === undefined) return defaultValue
    else return sdwebui_sharedopts[optnanme]
}

document.addEventListener("DOMContentLoaded", () => {
    const onload = () => {

        if (typeof gradioApp === "function") {

            shopts = gradioApp().querySelector("#sdwebui_sharedopts_script")
            if (!shopts) {
                setTimeout(onload, 2000);
                return
            }
        }
        else {
            setTimeout(onload, 2000);
        }
    };
    onload();
});
