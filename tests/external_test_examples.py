import os

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOKS_TO_TEST = [
    'minimal.ipynb',
]


def run_notebook(notebook_path):
    nb_name, _ = os.path.splitext(os.path.basename(notebook_path))
    dirname = os.path.dirname(notebook_path)

    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    nb['cells'] = [cell for cell in nb['cells'] if not cell['source'].startswith('!')]

    proc = ExecutePreprocessor(timeout=600, kernel_name='python3')
    proc.allow_errors = True

    proc.preprocess(nb, {'metadata': {'path': 'examples/'}})
    output_path = os.path.join(dirname, '_test_{}.ipynb'.format(nb_name))

    with open(output_path, mode='wt') as f:
        nbformat.write(nb, f)
    errors = []
    for cell in nb.cells:
        if 'outputs' in cell:
            for output in cell['outputs']:
                if output.output_type == 'error':
                    errors.append(output)
    return nb, errors


def test_examples():
    localdir = './examples'
    for file in NOTEBOOKS_TO_TEST:
        nb, errors = run_notebook(os.path.join(localdir, file))
        assert len(errors) == 0
