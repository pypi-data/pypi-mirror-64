"""yamlip - A yaml interpolation tool"""

__version__ = '0.0.1'
__author__ = 'Jan Murre <jan.murre@catalyz.nl>'
__all__ = []

import functools
from string import Template
from attrdict import AttrDict
import yaml
import click


class DotTemplate(Template):
    idpattern = r"[a-z][\.\-_a-z0-9]*"


def rgetattr(obj, initial_attr, *args):
    def _getattr(obj, attr):
        try:
            return getattr(obj, attr, *args)
        except AttributeError:
            return f"<<no substitute: {initial_attr}>>"
    return functools.reduce(_getattr, [obj] + initial_attr.split('.'))


def fetch_interpolated_yaml(src_yaml_fn):

    with open(src_yaml_fn) as sf:
        src_yaml = sf.read()
    yaml_tmpl = DotTemplate(src_yaml)
    ip_vars = AttrDict(yaml.safe_load(src_yaml))

    placeholders = ["".join(hit) for hit in yaml_tmpl.pattern.findall(yaml_tmpl.template)]
    substitutions = {p: rgetattr(ip_vars, p) for p in placeholders}
    return yaml_tmpl.safe_substitute(substitutions)


@click.command()
@click.argument("source_yaml_file")
@click.option("-o", "--output")
def yamlip(source_yaml_file, output):
    result = fetch_interpolated_yaml(source_yaml_file)
    if output:
        with open(output, 'w') as tf:
            tf.write(result)
    else:
        click.echo(result)
