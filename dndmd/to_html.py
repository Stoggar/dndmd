#!/usr/bin/env python3
from jinja2 import Environment, PackageLoader, FileSystemLoader
import markdown
import sys
import pathlib
import argparse

THIS_DIR = pathlib.Path(__file__).parent
BLOCK_NAME = 'content'
ITEM_PARENT_TEMPLATE = 'item/item.html'

def main(mark_path, parent_path):
    # prepare environment:
    env_dir = THIS_DIR / 'item'
    env = load_environment(env_dir)

    # get html from markdown:
    html = get_html(mark_path, parent_path, BLOCK_NAME, env)
    
    # write to file:
    html_filename = get_html_filename(mark_path)
    write_to_file(html_filename, html)
    print(f'wrote to file {html_filename}')


def get_html(mark_path, parent_path, block_name, env):
    raw_html = markdown2html(mark_path)
    html_as_template = get_html_as_template(raw_html, parent_path, block_name)
    final_html = env.from_string(html_as_template).render()
    return final_html


def read_file(filename):
    f = open(filename, 'r')
    content_markdown = f.read()
    f.close()
    return content_markdown


def markdown2html(mark_path):
    content = read_file(mark_path)
    html = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    return html


def get_html_as_template(html, parent_path, block_name):
    parent_path = pathlib.PurePath(parent_path)
    pre = '{% extends "' + parent_path.name + '" %}\r\n'
    pre += '\r\n{% block ' + block_name + ' %}'
    post = '\r\n{% endblock %}'
    html = pre + html + post 
    return html


def load_environment(path):
    file_loader = FileSystemLoader(str(path))
    env = Environment(loader=file_loader)
    return env


def write_to_file(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()


def get_html_filename(mark_path):
    path = pathlib.Path(mark_path)
    if path.suffix != '.md':
        print('unexpected filename ending')
        return
    html_base = path.stem
    html_final = html_base + '.html'
    return html_final


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('markdown_filename')
arg_parser.add_argument('-f', '--format', default='item',
        help='format of html output')
args = arg_parser.parse_args()

if args.format == 'item':
    main(args.markdown_filename, THIS_DIR / ITEM_PARENT_TEMPLATE)


