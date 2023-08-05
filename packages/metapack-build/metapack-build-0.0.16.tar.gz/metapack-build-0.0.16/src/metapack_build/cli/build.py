# Copyright (c) 2019 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE

"""

"""

import argparse
import re
from pathlib import Path
from time import time

from metapack import MetapackDoc
from metapack.cli.core import (MetapackCliMemo, err, extract_path_name,
                               get_lib_module_dict, prt, update_name,
                               write_doc)
from metapack.package import Downloader
from metapack_build.build import (make_csv_package, make_excel_package,
                                  make_filesystem_package, make_zip_package)
from metapack_build.core import process_schemas
from rowgenerators import parse_app_url
from rowgenerators.util import clean_cache
from tableintuit import RowIntuitError

last_dl_message = time()


def build_downloader_callback(msg_type, message, read_len, total_len):
    global last_dl_message
    if time() > last_dl_message + 5:
        print("\rDownloading {} {} {} bytes ".format(msg_type, message, total_len), end='')
        last_dl_message = time()


downloader = Downloader.get_instance()


def build(subparsers):
    """
    Build source packages.

    The mp build program runs all of the resources listed in a Metatab file and
    produces one or more Metapack packages with those resources localized. It
    will always try to produce a Filesystem package, and may optionally produce
    Excel, Zip and CSV packages.

    Typical usage is to be run inside a source package directory with

    .. code-block:: bash

        $ mp build

    To build all of the package types:

    .. code-block:: bash

        $ mp build -fezc

    By default, packages are built with versioned names. The
    ``--nonversion-name`` option will create file packages with
    non-versioned name, and the ``--nonversioned-link`` option will
    produce a non-versioned soft link pointing to the versioned file.


    """

    parser = subparsers.add_parser(
        'build',
        help='Build derived packages',
        description=build.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='')

    parser.set_defaults(run_command=run_metapack)

    parser.add_argument('metatabfile', nargs='?',
                        help="Path or URL to a metatab file. If not provided, defaults to 'metadata.csv'. "
                        )

    parser.add_argument('-p', '--profile', help="Name of a BOTO or AWS credentails profile", required=False)

    parser.add_argument('-D', '--package-directory', help="Write Zip, Excel and CSV packages to an alternate directory",
                        required=False)

    parser.add_argument('-F', '--force', action='store_true', default=False,
                        help='Force some operations, like updating the name and building packages')

    parser.add_argument('-R', '--reuse-resources', action='store_true', default=False,
                        help='When building Filesystem package, try to reuse resources built in prior build')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-n', '--nonversion-name', action='store_true', default=False,
                       help='Write file packages with non-versioned names')

    group.add_argument('-N', '--nonversion-link', action='store_true', default=False,
                       help='Create links with nonversioned names to file packages')

    parser.set_defaults(handler=None)

    # Derived Package Group

    derived_group = parser.add_argument_group('Derived Packages', 'Generate other types of packages')

    derived_group.add_argument('-e', '--excel', action='store_true', default=False,
                               help='Create an excel archive from a metatab file')

    derived_group.add_argument('-z', '--zip', action='store_true', default=False,
                               help='Create a zip archive from a metatab file')

    derived_group.add_argument('-f', '--filesystem', action='store_true', default=False,
                               help='Create a filesystem archive from a metatab file')

    derived_group.add_argument('-c', '--csv', action='store_true', default=False,
                               help='Create a CSV archive from a metatab file')

    # Administration Group

    admin_group = parser.add_argument_group('Administration', 'Information and administration')

    admin_group.add_argument('--clean-cache', default=False, action='store_true',
                             help="Clean the download cache")

    admin_group.add_argument('-C', '--clean', default=False, action='store_true',
                             help="For some operations, like updating schemas, clear the section of existing terms first")


def run_metapack(args):
    from rowgenerators.rowpipe.exceptions import TooManyCastingErrors

    downloader.set_callback((build_downloader_callback))

    m = MetapackCliMemo(args, downloader)

    if m.args.profile:
        from metatab.s3 import set_s3_profile
        set_s3_profile(m.args.profile)

    try:
        for handler in (metatab_derived_handler, metatab_admin_handler):
            handler(m)
    except TooManyCastingErrors as e:
        prt('Casting Errors:')
        for error in e.errors:
            prt(error)
        if m.args.exceptions:
            raise e
        else:
            err(e)
    except Exception as e:
        raise
        if m.args.exceptions:
            raise e
        else:
            err(e)

    clean_cache(m.cache)


def metatab_derived_handler(m):
    """Create local Zip, Excel and Filesystem packages

    :param m:
    :param skip_if_exists:
    :return:
    """
    from metapack.util import get_materialized_data_cache
    from shutil import rmtree

    create_list = []
    url = None

    doc = MetapackDoc(m.mt_file)

    env = get_lib_module_dict(doc)

    package_dir = m.package_root

    if m.args.package_directory:
        # If this is set, the FS package will be built to m.package_root, but the
        # file packages will be built to package_dir
        package_dir = parse_app_url(m.args.package_directory)

    update_name(m.mt_file, fail_on_missing=False, report_unchanged=False)

    process_schemas(m.mt_file, cache=m.cache, clean=m.args.clean, report_found=False)

    nv_name = m.args.nonversion_name
    nv_link = m.args.nonversion_link

    # Remove any data that may have been cached , for instance, from Jupyter notebooks
    rmtree(get_materialized_data_cache(doc), ignore_errors=True)

    reuse_resources = m.args.reuse_resources

    # Always create a filesystem package before ZIP or Excel, so we can use it as a source for
    # data for the other packages. This means that Transform processes and programs only need
    # to be run once.

    _, url, created = make_filesystem_package(m.mt_file, m.package_root, m.cache, env, m.args.force, False,
                                              nv_link, reuse_resources=reuse_resources)
    create_list.append(('fs', url, created))

    lb_path = Path(m.package_root.fspath, 'last_build')

    if created or not lb_path.exists():
        Path(m.package_root.fspath, 'last_build').touch()

    m.mt_file = url

    env = {}  # Don't need it anymore, since no more programs will be run.

    if m.args.excel is not False:
        _, url, created = make_excel_package(m.mt_file, package_dir, m.cache, env, m.args.force, nv_name, nv_link)
        create_list.append(('xlsx', url, created))

    if m.args.zip is not False:
        _, url, created = make_zip_package(m.mt_file, package_dir, m.cache, env, m.args.force, nv_name, nv_link)
        create_list.append(('zip', url, created))

    if m.args.csv is not False:
        _, url, created = make_csv_package(m.mt_file, package_dir, m.cache, env, m.args.force, nv_name, nv_link)
        create_list.append(('csv', url, created))

    index_packages(m)

    return create_list


def metatab_admin_handler(m):
    if m.args.clean_cache:
        clean_cache('metapack')


def classify_url(url):
    ss = parse_app_url(url)

    if ss.target_format in DATA_FORMATS:
        term_name = 'DataFile'
    elif ss.target_format in DOC_FORMATS:
        term_name = 'Documentation'
    else:
        term_name = 'Resource'

    return term_name


def add_resource(mt_file, ref, cache):
    """Add a resources entry, downloading the intuiting the file, replacing entries with
    the same reference"""

    if isinstance(mt_file, MetapackDoc):
        doc = mt_file
    else:
        doc = MetapackDoc(mt_file)

    if 'Resources' not in doc:
        doc.new_section('Resources')

    doc['Resources'].args = [e for e in set(doc['Resources'].args + ['Name', 'StartLine', 'HeaderLines', 'Encoding']) if
                             e]

    seen_names = set()

    u = parse_app_url(ref)

    # The web and file URLs don't list the same.

    if u.proto == 'file':
        entries = u.list()
    else:
        entries = [ssu for su in u.list() for ssu in su.list()]

    print(type(u), u)

    for e in entries:
        add_single_resource(doc, e, cache=cache, seen_names=seen_names)

    write_doc(doc, mt_file)


def add_single_resource(doc, ref, cache, seen_names):
    from metatab.util import slugify

    t = doc.find_first('Root.Datafile', value=ref)

    if t:
        prt("Datafile exists for '{}', deleting".format(ref))
        doc.remove_term(t)
    else:
        prt("Adding {}".format(ref))

    term_name = classify_url(ref)

    path, name = extract_path_name(ref)

    # If the name already exists, try to create a new one.
    # 20 attempts ought to be enough.
    if name in seen_names:
        base_name = re.sub(r'-?\d+$', '', name)

        for i in range(1, 20):
            name = "{}-{}".format(base_name, i)
            if name not in seen_names:
                break

    seen_names.add(name)

    encoding = start_line = None
    header_lines = []

    if not name:
        from hashlib import sha1
        name = sha1(slugify(path).encode('ascii')).hexdigest()[:12]

        # xlrd gets grouchy if the name doesn't start with a char
        try:
            int(name[0])
            name = 'a' + name[1:]
        except Exception:
            pass

    return doc['Resources'].new_term(term_name, ref, name=name,
                                     startline=start_line,
                                     headerlines=','.join(str(e) for e in header_lines),
                                     encoding=encoding)


def run_row_intuit(path, cache):
    from tableintuit import RowIntuiter
    from itertools import islice
    from rowgenerators import TextEncodingError, get_generator

    for encoding in ('ascii', 'utf8', 'latin1'):
        try:

            u = parse_app_url(path)
            u.encoding = encoding

            rows = list(islice(get_generator(url=str(u), cache=cache, ), 5000))
            return encoding, RowIntuiter().run(list(rows))
        except (TextEncodingError, UnicodeEncodeError):
            pass

    raise RowIntuitError('Failed to convert with any encoding')


def index_packages(m):
    from metapack.cli.index import walk_packages
    from metapack.index import SearchIndex, search_index_file

    idx = SearchIndex(search_index_file())

    entries = []
    for p in walk_packages(None, parse_app_url(str(m.package_root.fspath))):
        prt(p.ref)
        idx.add_package(p)
        entries.append(p.name)

    idx.write()
    prt("Indexed ", len(entries), 'entries')


DATA_FORMATS = ('xls', 'xlsx', 'tsv', 'csv')
DOC_FORMATS = ('pdf', 'doc', 'docx', 'html')
