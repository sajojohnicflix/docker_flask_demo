from flask import Flask, send_file
import helpers

app = Flask(__name__)


@app.route('/catalogue/screenshot/<encoding_task_id>.<extension>/<time>')
@app.route('/catalogue/screenshot/<encoding_task_id>.<extension>/<time>/<dimensions>')
def get_screenshot(encoding_task_id, time, dimensions, extension):
    manifest_url = helpers.get_manifest_url(encoding_task_id)
    width, height = helpers.parse_dimensions(dimensions)
    if extension == "gif":
        screenshot = helpers.extract_animation(manifest_url, time, width, height, extension)
    else:
        screenshot = helpers.extract_screenshot(manifest_url, time, width, height, extension)
    return send_file(screenshot)


@app.route('/health')
def hello():
    return "service healthy"

if __name__ == '__main__':
    app.run()