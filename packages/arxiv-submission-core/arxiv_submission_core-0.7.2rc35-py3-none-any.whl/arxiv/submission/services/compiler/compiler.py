"""
Integration with the compiler service API.

The compiler is responsible for building PDF, DVI, and other goodies from
LaTeX sources. In the submission UI, we specifically want to build a PDF so
that the user can preview their submission. Additionally, we want to show the
submitter the TeX log so that they can identify any potential problems with
their sources.
"""
import io
import json
import re
from collections import defaultdict
from enum import Enum
from functools import wraps
from typing import Tuple, Optional, List, Union, NamedTuple, Mapping, Any
from urllib.parse import urlparse, urlunparse, urlencode

import dateutil.parser
import requests
from werkzeug.datastructures import FileStorage

from arxiv.base import logging
from arxiv.integration.api import status, service

from ...domain.compilation import Compilation, CompilationProduct, \
    CompilationLog


logger = logging.getLogger(__name__)

PDF = Compilation.Format.PDF


class CompilationFailed(RuntimeError):
    """The compilation service failed to compile the source package."""


class Compiler(service.HTTPIntegration):
    """Encapsulates a connection with the compiler service."""

    SERVICE = 'compiler'

    VERSION = "30c84dd5b5381e2f2f69ed58298bd87c10bad5c8"
    """Verison of the compiler service with which we are integrating."""

    NAME = "arxiv-compiler"
    """Name of the compiler service with which we are integrating."""

    class Meta:
        """Configuration for :class:`Classifier`."""

        service_name = "compiler"

    def is_available(self, **kwargs: Any) -> bool:
        """Check our connection to the compiler service."""
        timeout: float = kwargs.get('timeout', 0.2)
        try:
            self.get_service_status(timeout=timeout)
        except Exception as e:
            logger.error('Encountered error calling compiler: %s', e)
            return False
        return True

    def _parse_status_response(self, data: dict, headers: dict) -> Compilation:
        return Compilation(
            source_id=data['source_id'],
            checksum=data['checksum'],
            output_format=Compilation.Format(data['output_format']),
            status=Compilation.Status(data['status']),
            reason=Compilation.Reason(data.get('reason', None)),
            description=data.get('description', None),
            size_bytes=data.get('size_bytes', 0),
            product_checksum=headers.get('ETag')
        )

    def _parse_loc(self, headers: Mapping) -> str:
        return str(urlparse(headers['Location']).path)

    def get_service_status(self, timeout: float = 0.2) -> dict:
        """Get the status of the compiler service."""
        data: dict = self.json('get', 'status', timeout=timeout)[0]
        return data

    def compile(self, source_id: str, checksum: str, token: str,
                stamp_label: str, stamp_link: str,
                compiler: Optional[Compilation.SupportedCompiler] = None,
                output_format: Compilation.Format = PDF,
                force: bool = False) -> Compilation:
        """
        Request compilation for an upload workspace.

        Unless ``force`` is ``True``, the compiler service will only attempt
        to compile a source ID + checksum + format combo once. If there is
        already a compilation underway or complete for the parameters in this
        request, the service will redirect to the corresponding status URI.
        Hence the data returned by this function may be from the response to
        the initial POST request, or from the status endpoint after being
        redirected.

        Parameters
        ----------
        source_id : int
            Unique identifier for the upload workspace.
        checksum : str
            State up of the upload workspace.
        token : str
            The original (encrypted) auth token on the request. Used to perform
            subrequests to the file management service.
        stamp_label : str
            Label to use in PS/PDF stamp/watermark. Form is
              'Identifier  [Category Date]'
            Category and Date are optional. By default Date will be added
            by compiler.
        stamp_link : str
            Link (URI) to use in PS/PDF stamp/watermark.
        compiler : :class:`.Compiler` or None
            Name of the preferred compiler.
        output_format : :class:`.Format`
            Defaults to :attr:`.Format.PDF`.
        force : bool
            If True, compilation will be forced even if it has been attempted
            with these parameters previously. Default is ``False``.

        Returns
        -------
        :class:`Compilation`
            The current state of the compilation.

        """
        logger.debug("Requesting compilation for %s @ %s: %s",
                     source_id, checksum, output_format)
        payload = {'source_id': source_id, 'checksum': checksum,
                   'stamp_label': stamp_label, 'stamp_link': stamp_link,
                   'format': output_format.value, 'force': force}
        endpoint = '/'
        expected_codes = [status.OK, status.ACCEPTED,
                          status.SEE_OTHER, status.FOUND]
        data, _, headers = self.json('post', endpoint, token, json=payload,
                                     expected_code=expected_codes)
        return self._parse_status_response(data, headers)

    def get_status(self, source_id: str, checksum: str, token: str,
                   output_format: Compilation.Format = PDF) -> Compilation:
        """
        Get the status of a compilation.

        Parameters
        ----------
        source_id : int
            Unique identifier for the upload workspace.
        checksum : str
            State up of the upload workspace.
        output_format : :class:`.Format`
            Defaults to :attr:`.Format.PDF`.

        Returns
        -------
        :class:`Compilation`
            The current state of the compilation.

        """
        endpoint = f'/{source_id}/{checksum}/{output_format.value}'
        data, _, headers = self.json('get', endpoint, token)
        return self._parse_status_response(data, headers)

    def compilation_is_complete(self, source_id: str, checksum: str,
                                token: str,
                                output_format: Compilation.Format) -> bool:
        """Check whether compilation has completed successfully."""
        stat = self.get_status(source_id, checksum, token, output_format)
        if stat.status is Compilation.Status.SUCCEEDED:
            return True
        elif stat.status is Compilation.Status.FAILED:
            raise CompilationFailed('Compilation failed')
        return False

    def get_product(self, source_id: str, checksum: str, token: str,
                    output_format: Compilation.Format = PDF) \
            -> CompilationProduct:
        """
        Get the compilation product for an upload workspace, if it exists.

        Parameters
        ----------
        source_id : int
            Unique identifier for the upload workspace.
        checksum : str
            State up of the upload workspace.
        output_format : :class:`.Format`
            Defaults to :attr:`.Format.PDF`.

        Returns
        -------
        :class:`CompilationProduct`
            The compilation product itself.

        """
        endpoint = f'/{source_id}/{checksum}/{output_format.value}/product'
        response = self.request('get', endpoint, token, stream=True)
        return CompilationProduct(content_type=output_format.content_type,
                                  stream=io.BytesIO(response.content))

    def get_log(self, source_id: str, checksum: str, token: str,
                output_format: Compilation.Format = PDF) -> CompilationLog:
        """
        Get the compilation log for an upload workspace, if it exists.

        Parameters
        ----------
        source_id : int
            Unique identifier for the upload workspace.
        checksum : str
            State up of the upload workspace.
        output_format : :class:`.Format`
            Defaults to :attr:`.Format.PDF`.

        Returns
        -------
        :class:`CompilationProduct`
            The compilation product itself.

        """
        endpoint = f'/{source_id}/{checksum}/{output_format.value}/log'
        response = self.request('get', endpoint, token, stream=True)
        return CompilationLog(stream=io.BytesIO(response.content))


def get_task_id(source_id: str, checksum: str,
                output_format: Compilation.Format) -> str:
    """Generate a key for a /checksum/format combination."""
    return f"{source_id}/{checksum}/{output_format.value}"


def split_task_id(task_id: str) -> Tuple[str, str, Compilation.Format]:
    source_id, checksum, format_value = task_id.split("/")
    return source_id, checksum, Compilation.Format(format_value)


class Download(object):
    """Wrapper around response content."""

    def __init__(self, response: requests.Response) -> None:
        """Initialize with a :class:`requests.Response` object."""
        self._response = response

    def read(self, *args: Any, **kwargs: Any) -> bytes:
        """Read response content."""
        return self._response.content
