import os
from classes.document_class import Document

ALLOWED_FILETYPES = {"png", "jpeg", "jpg", "gif"}


def get_upload_directory() -> str:
    parent_dir = os.getcwd()
    return os.path.join(parent_dir, 'uploads')


def check_logging_directory() -> None:
    current_logging_dir = get_upload_directory()
    if not os.path.exists(current_logging_dir):
        os.mkdir(current_logging_dir)
        print("CREATED DIR: {}".format(current_logging_dir))


def check_filetype_valid(filename: str) -> bool:
    filename_split = filename.split(".")
    if filename_split[-1].lower() in ALLOWED_FILETYPES:
        return True
    else:
        return False


def return_filetype(filename: str) -> str:
    filename_split = filename.split(".")
    return ".{}".format(filename_split[-1].lower())


def return_filename(doc: Document, filename: str) -> str:
    return str(doc.user_id) + "_" + str(doc.document_id) + return_filetype(filename)