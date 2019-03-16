#!/usr/bin/env python3
"""Segment images
"""
from inselect.lib.fix_frozen import fix_frozen

fix_frozen()

import argparse
import sys
import traceback

from pathlib import Path

import inselect.lib.utils

from inselect.lib.document import InselectDocument
from inselect.lib.segment_document import SegmentDocument
from inselect.lib.utils import debug_print

# for function new_document
from inselect.lib.ingest import ingest_image
from pathlib import Path
from inselect.lib.inselect_error import InselectError

# for function safe_crops
from inselect.lib.document_export import DocumentExport
from inselect.lib.templates.dwc import DWC
from inselect.lib.user_template import UserTemplate
from inselect.lib.validate_document import format_validation_problems


def new_document(path, default_metadata_items=None):
        """Creates and opens a new inselect document for the scanned image
        given in path
        """

        path = Path(path)
        if not path.is_file():
            raise InselectError('Image file [{0}] does not exist'.format(path))
        else:
            # Callable for worker thread
            #thumbnail_width = user_template_choice().current.thumbnail_width_pixels

            doc = ingest_image(path, path.parent)
            return doc

def save_crops(inselect_doc, path_to_img, overwrite_existing, template):
    """ Save crops from inselect document to folder in same directory
    """
    doc = inselect_doc
    p = path_to_img
    export = DocumentExport(UserTemplate.load(template) if template else DWC)
    try:
        debug_print('Loading [{0}]'.format(p))
        #doc = InselectDocument.load(p)
        validation = export.validation_problems(doc)
        if validation.any_problems:
            print(
                'Not saving crops for [{0}] because there are validation '
                'problems'.format(p)
            )
            for msg in format_validation_problems(validation):
                print(msg)
        elif not overwrite_existing and doc.crops_dir.is_dir():
            print('Crops dir [{0}] exists - skipping'.format(doc.crops_dir))
        else:
            print('Will save crops for [{0}] to [{1}]'.format(p, doc.crops_dir))

            debug_print('Loading full-resolution scanned image')
            doc.scanned.array

            debug_print('Saving crops')
            export.save_crops(doc)
    except KeyboardInterrupt:
        raise
    except Exception:
        print('Error saving crops from [{0}]'.format(p))
        traceback.print_exc()

def segment(img, sort_by_columns):
    """ Create inselect document with segmentations given path to img file.
    Supported types are .bmp .jpeg .jpg .png .tif .tiff
    Returns: inselect document
    """
    p = img
    doc = new_document(img)
    segment_doc = SegmentDocument(sort_by_columns)
    if not doc.items:
        print('Segmenting [{0}]'.format(p))
        try:
            debug_print('Will segment [{0}]'.format(p))
            doc, display_image = segment_doc.segment(doc)
            del display_image    # We don't use this
            doc.save()
        except KeyboardInterrupt:
            raise
        except Exception:
            print('Error segmenting [{0}]'.format(p))
            traceback.print_exc()
        else:
            print('Segmented [{0}]'.format(doc))
    else:
        print('Skipping [{0}] as it already contains items'.format(p))

    return doc

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Segments Inselect documents')
    parser.add_argument("img", help='Path to image file *.bmp, *.jpeg, *.jpg, *.png, *.tif *.tiff')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument(
        '--sort-by-columns', action='store_true', default=False,
        help='Sort boxes by columns; default is to sort boxes by rows')
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + inselect.__version__
    )
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='Overwrite existing crops directories')
    parser.add_argument(
        '-t', '--template', type=Path, help="Path to a '{0}' file that will be "
        'used to format the crop filenames'.format(UserTemplate.EXTENSION))

    args = parser.parse_args(args)

    inselect.lib.utils.DEBUG_PRINT = args.debug

    doc = segment(args.img, args.sort_by_columns)
    save_crops(doc, args.img, args.overwrite, args.template)


if __name__ in ('__main__', 'segment__main__'):
    main()
