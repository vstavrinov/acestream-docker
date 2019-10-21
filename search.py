import sys
from distutils.util import split_quoted

from flask import Flask, request, Response

from acestream_search.acestream_search import main as engine, get_options, __version__

app = Flask(__name__)
if sys.version_info[0] > 2:
    def u_code(string):
        return string
else:
    def u_code(string):
        return string.encode("utf8")


def get_args():
    opts = {'prog': request.base_url}
    for item in request.args:
        opts[item] = u_code(request.args[item])
    if 'name' in opts:
        opts['name'] = split_quoted(opts['name'])
    args = get_options(opts)
    return args


@app.route('/search.m3u8')
def main():
    args = get_args()
    # return str(args)
    if args.xml_epg:
        content_type = 'text/xml'
    elif args.json:
        content_type = 'application/json'
    else:
        content_type = 'application/x-mpegURL'

    def generate():
        for page in engine(args):
            yield page + '\n'

    if 'version' in args:
        return Response(__version__ + '\n', content_type='text/plain')
    if 'help' in args:
        return Response(args.help, content_type='text/plain')
    if 'usage' in args:
        return Response(args.usage, content_type='text/plain')
    return Response(generate(), content_type=content_type)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
