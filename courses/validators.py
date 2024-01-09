''' Field validators to be used for models '''

from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
import pypdf

@deconstructible
class PDFFileValidator():
    ''' Validates file size and if it is a pdf  '''
    error_messages = {
        'max_size': ("Ensure this file size is not greater than %(max_size)s."
                     " Your file size is %(size)s."),
        'content_type': "You can only upload pdf files.",
    }

    def __init__(self, max_size=None):
        self.max_size = max_size

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                  'max_size', params)

        try:
            pypdf.PdfReader(data)
        except Exception as exc:
            raise ValidationError(self.error_messages['content_type'],
                                  'content_type') from exc

    def __eq__(self, other):
        return (
            isinstance(other, PDFFileValidator) and
            self.max_size == other.max_size
        )
