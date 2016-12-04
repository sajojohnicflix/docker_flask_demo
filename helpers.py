import urllib2
import json
from subprocess import call


def get_manifest_url(encoding_task_id):
    api_endpoint = "http://api.icflix.com/v1.42/website/cms/screenshot/{}".format(encoding_task_id)
    req_headers = {'Authorization': 'Bearer 9db6e986-c08e-4ebe-87c7-079f34640f64'}
    try:
        request = urllib2.Request(api_endpoint, headers=req_headers)
        contents = json.loads(urllib2.urlopen(request).read())
        return contents['manifest']
    except:
        return ''


def parse_dimensions(dimensions):
    try:
        if "x" not in dimensions:
            raise "Error in dimensions format"
        width, height = dimensions.split("x")
        if not width:
            width = -1
        else:
            width = int(width)
        if not height:
            height = -1
        else:
            height = int(height)
        return width, height
    except:
        return [0, 0]


def extract_screenshot(manifest_url, time, width, height, extension):
    filename = "/tmp/screenshot.{}".format(extension)
    ffmpeg_args = [
        "ffmpeg",
        "-ss", time,
        "-y",
        "-i", manifest_url,
        "-f", "image2",
        "-frames:v", "1",
        "-vf", "scale={}:{}".format(width, height),
        filename
    ]
    call(ffmpeg_args)
    return filename


def extract_animation(manifest_url, time, width, height, extension):
    filename = "/tmp/animation.{}".format(extension)
    palette_filename = "/tmp/palette.png"
    ffmpeg_args = [
        "ffmpeg",
        "-y",
        "-ss", time,
        "-t", "2",
        "-i", manifest_url,
        "-pix_fmt", "gray",
        "-vf", "setpts=2*PTS,scale={}:{}:flags=lanczos,palettegen".format(width, height),
        palette_filename
    ]
    call(ffmpeg_args)
    ffmpeg_args = [
        "ffmpeg",
        "-y",
        "-ss", time,
        "-t", "2",
        "-i", manifest_url,
        "-i", "/tmp/palette.png",
        "-pix_fmt", "gray",
        "-filter_complex", "setpts=2*PTS,scale={}:{}:flags=lanczos[x];[x][1:v]paletteuse".format(width, height),
        filename
    ]
    call(ffmpeg_args)
    return filename
