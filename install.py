import launch

if not launch.is_installed("imageio"):
    launch.run_pip("install imageio", "requirements 0 for Infinite-Zoom")
if not launch.is_installed("imageio-ffmpeg"):
    launch.run_pip("install imageio-ffmpeg", "requirements 1 for Infinite-Zoom")



"""
import launch
import os
import pkg_resources

req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")

with open(req_file) as file:
    for package in file:
        try:
            package = package.strip()
            if '==' in package:
                package_name, package_version = package.split('==')
                installed_version = pkg_resources.get_distribution(package_name).version
                if installed_version != package_version:
                    launch.run_pip(f"install {package}", f"sd-webui-controlnet requirement: changing {package_name} version from {installed_version} to {package_version}")
            elif not launch.is_installed(package):
                launch.run_pip(f"install {package}", f"sd-webui-controlnet requirement: {package}")
        except Exception as e:
            print(e)
            print(f'Warning: Failed to install {package}, some preprocessors may not work.')
"""