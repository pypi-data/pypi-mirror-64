# -*- coding: UTF-8 -*-
import logging
<<<<<<< HEAD

import click

from miio.click_common import (
    ExceptionHandlerGroup, DeviceGroupMeta, GlobalContextObject,
    json_output,
=======
import click
from miio.click_common import (
    ExceptionHandlerGroup, DeviceGroupMeta, GlobalContextObject
>>>>>>> Framework for device class based cli configuration
)

_LOGGER = logging.getLogger(__name__)


@click.group(cls=ExceptionHandlerGroup)
@click.option('-d', '--debug', default=False, count=True)
<<<<<<< HEAD
@click.option('-o', '--output', type=click.Choice([
    'default', 'json', 'json_pretty',
]), default='default')
@click.pass_context
def cli(ctx, debug: int, output: str):
=======
@click.pass_context
def cli(ctx, debug: int):
>>>>>>> Framework for device class based cli configuration
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        _LOGGER.info("Debug mode active")
    else:
        logging.basicConfig(level=logging.INFO)

<<<<<<< HEAD
    if output in ('json', 'json_pretty'):
        output_func = json_output(pretty=output == 'json_pretty')
    else:
        output_func = None

    ctx.obj = GlobalContextObject(
        debug=debug,
        output=output_func,
=======
    ctx.obj = GlobalContextObject(
        debug=debug
>>>>>>> Framework for device class based cli configuration
    )


for device_class in DeviceGroupMeta.device_classes:
    cli.add_command(device_class.get_device_group())


def create_cli():
    return cli(auto_envvar_prefix="MIIO")


if __name__ == '__main__':
    create_cli()
