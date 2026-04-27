import logging

from django.template import Template
from django.utils.safestring import SafeString

from aws_xray_sdk.core import xray_recorder

log = logging.getLogger(__name__)


def patch_template():

    attr = '_xray_original_render'

    if getattr(Template, attr, None):
        log.debug("already patched")
        return

    setattr(Template, attr, Template.render)

    @xray_recorder.capture('template_render')
    def xray_render(self, context):
        pass

    Template.render = xray_render
