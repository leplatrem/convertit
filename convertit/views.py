import os
import urllib2
from functools import partial
from mimetypes import guess_extension
from uuid import uuid4

import magic
from pyramid.httpexceptions import (
    HTTPError,
    HTTPBadRequest,
    HTTPFound,
)
from pyramid.url import static_url
from pyramid.view import view_config

from convertit.helpers import (
    remove_files_older_than,
    render_converted_name,
)


def remove_old_files(request):
    settings = request.registry.settings
    downloads_path = settings['convertit.downloads_path']
    converted_path = settings['convertit.converted_path']
    downloads_max_age = settings['convertit.downloads_max_age']
    converted_max_age = settings['convertit.converted_max_age']

    remove_files_older_than(int(downloads_max_age), downloads_path)
    remove_files_older_than(int(converted_max_age), converted_path)


def save(request, file_):
    downloads_path = request.registry.settings['convertit.downloads_path']
    target_file = os.path.join(downloads_path, str(uuid4()))
    with open(target_file, 'w') as f:
        f.write(file_.read())
    return target_file


def download(request, url):
    message = "Sorry, there was an error fetching the document. Reason: %s"
    try:
        response = urllib2.urlopen(url)
        return save(request, response)
    except ValueError as e:
        raise HTTPBadRequest(message % str(e))
    except urllib2.HTTPError as e:
        raise HTTPError(message % str(e), status_int=e.getcode())
    except urllib2.URLError as e:
        raise HTTPBadRequest(message % str(e))


def get_input_mimetype(request, input_filepath):
    guessed_mimetype = magic.from_file(input_filepath, mime=True)
    input_mimetype = request.GET.get('from', guessed_mimetype)

    if not input_mimetype:
        raise HTTPBadRequest('Can not guess mimetype')

    return input_mimetype


def get_converter(request, input_mimetype, output_mimetype):
    converters = request.registry.convertit

    if (input_mimetype, output_mimetype) not in converters:
        message = 'Unsupported transform: from %s to %s'
        raise HTTPBadRequest(message % (input_mimetype, output_mimetype))

    return converters[(input_mimetype, output_mimetype)]


def output_basename_from_url(request, extension, url):
    settings = request.registry.settings
    name_template = settings['convertit.converted_name']
    return render_converted_name(name_template, url, extension)


@view_config(route_name='home', request_method='GET')
def home_get_view(request):
    url = request.GET.get('url')
    if url is None:
        return HTTPBadRequest('Missing parameter: url')

    input_filepath = download(request, url)
    output_basename_generator = partial(output_basename_from_url, url=url)

    return home_view(request, input_filepath, output_basename_generator)


@view_config(route_name='home', request_method='POST')
def home_post_view(request):
    settings = request.registry.settings
    field = settings['convertit.post_field']
    uploaded = request.POST.get(field)
    input_filepath = save(request, uploaded.file)

    filename = os.path.splitext(uploaded.filename)[0]

    def output_basename_generator(request, extension):
        return '%s%s' % (filename, extension)

    return home_view(request, input_filepath, output_basename_generator)


def home_view(request, input_filepath, output_basename_generator):
    settings = request.registry.settings
    converted_path = settings['convertit.converted_path']

    input_mimetype = get_input_mimetype(request, input_filepath)

    output_mimetype = request.GET.get('to', 'application/pdf')
    output_extension = guess_extension(output_mimetype)
    output_basename = output_basename_generator(request, output_extension)
    output_filepath = os.path.join(converted_path, output_basename)

    remove_old_files(request)

    convert = get_converter(request, input_mimetype, output_mimetype)

    try:
        convert(input_filepath, output_filepath)
    except Exception as e:
        message = "Sorry, an error occured during convertion: %s"
        return HTTPBadRequest(message % str(e))

    return HTTPFound(static_url(output_filepath, request),
                     content_disposition='attachement; filename=%s' %
                     output_basename)
