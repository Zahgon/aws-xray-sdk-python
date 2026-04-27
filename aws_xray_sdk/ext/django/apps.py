import logging

from django.apps import AppConfig

from .conf import settings
from .db import patch_db
from .templates import patch_template
from aws_xray_sdk.core import patch, xray_recorder
from aws_xray_sdk.core.exceptions.exceptions import SegmentNameMissingException


log = logging.getLogger(__name__)


class XRayConfig(AppConfig):
    name = 'aws_xray_sdk.ext.django'

    def ready(self):
        """
        Configure global XRay recorder based on django settings
        under XRAY_RECORDER namespace.
        This method could be called twice during server startup
        because of base command and reload command.
        So this function must be idempotent
        """
        pass
