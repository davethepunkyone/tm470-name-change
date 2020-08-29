import os
from classes.document_class import Document

ALLOWED_FILETYPES = {"png", "jpeg", "jpg", "gif"}


def get_upload_directory() -> str:
    """This retrieves the upload directory building up from the current working directory as a str.

    Expected path: /app/static/uploads"""
    parent_dir = os.path.join(os.getcwd(), 'app')
    parent_dir = os.path.join(parent_dir, 'static')
    parent_dir = os.path.join(parent_dir, 'uploads')
    return parent_dir


def check_upload_directory() -> None:
    """This checks that the upload directory exists and if not, creates the directory ready for use."""
    current_upload_dir = get_upload_directory()
    if not os.path.exists(current_upload_dir):
        os.mkdir(current_upload_dir)
        print("CREATED DIR: {}".format(current_upload_dir))


def check_filetype_valid(filename: str) -> bool:
    """This checks that the provided filename is valid and an accepted filetype.

    Keyword arguments:
    filename (str) -- The filename to check."""
    filename_split = filename.split(".")
    if filename_split[-1].lower() in ALLOWED_FILETYPES:
        return True
    else:
        return False


def return_filetype(filename: str) -> str:
    """This grabs the filetype from a file and returns its type with preceding full stop (e.g. .gif).

    Keyword arguments:
    filename (str) -- The filename to retrieve the filetype from."""
    filename_split = filename.split(".")
    return ".{}".format(filename_split[-1].lower())


def return_filename(doc: Document, filename: str) -> str:
    """This returns the filename to use within the system for a users uploaded document.

    Keyword arguments:
    doc (Document) -- The document object this file will belong to.
    filename (str) -- The original filename of the document being uploaded."""
    return str(doc.user_id) + "_" + str(doc.document_id) + return_filetype(filename)
