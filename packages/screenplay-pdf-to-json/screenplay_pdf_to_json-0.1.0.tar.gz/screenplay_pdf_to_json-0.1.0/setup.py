# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['screenplay_pdf_to_json',
 'screenplay_pdf_to_json.parse_pdf',
 'screenplay_pdf_to_json.utils']

package_data = \
{'': ['*']}

install_requires = \
['pdfminer.six>=20200124,<20200125', 'spacy>=2.2.4,<3.0.0']

setup_kwargs = {
    'name': 'screenplay-pdf-to-json',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Screenplay Parser\n\n> Parse PDF screenplay into rich JSON format\n\n## Install\n\n```sh\npipenv install\n\n# or\npip3 install -r requirements.txt\n```\n\n## Usage\n\n```sh\npython index.py -s path_of_screenplay.pdf --start page_number_to_start_analyzing\n```\n\n## Notes\n\n- It\'s advisable to set `--start` to the start of the screenplay. Title page, cast list, etc should be skipped. Feature to detect these pages is part of the roadmap, so stay tuned.\n- Works well for "clean" PDF screenplays, not OCR PDFs.\n- Production screenplays works pretty well.\n\n## JSON structure\n\n```js\n[{\n    // page number\n    "page": 1,\n\n    // scene info\n    "scene_info": {\n        "region": "EXT.",  //region of scene [EXT., INT., EXT./INT, INT./EXT]\n        "location": "VILLA",\n        "time": ["DAY"] // time of scene [DAY, NIGHT, DAWN, DUSK, ...]\n    },\n    "scene": [{\n        "type": "ACTION",  // type of snippet [ACTION, CHARACTER, TRANSITION, DUAL_DIALOGUE]\n        "content": {...} // content differs based on ACTION\n    }, {...}]\n\n}, {...}]\n```\n\n- It\'s really an array of dictionaries rather than a JSON object.\n\n### Type Content Structure\n\n- ACTION\n  ```js\n  "content": [{\n      "text": "an action paragraph",\n      "x": 108,\n      "y": 120 // Y-axis of last line in paragraph\n  }, {...}]\n  ```\n- CHARACTER\n  ```js\n   "content": {\n       "character": "MILES",\n       "modifier": null,  // V.O, O.S., and more. null if no modifier\n       "dialogue": [\n        "Hey good morning. How you doing?... Weekend was short, huh? ",\n        "(he turns to another kid)", //parentheticals are seperated\n        " Oh my gosh this is embarrassing, we wore the same jacket--"\n       ]\n   }\n  ```\n- DUAL_DIALOGUE\n  ```js\n   "content": {\n       "character1": {\n            "character": {\n                "character": "PETER",\n                "modifier": null\n            },\n            "dialogue": [\n                "(groggy)",\n                " Why are you trying to kill me?--"\n            ]\n        },\n        "character2": {\n            "character": {\n                "character": "MILES",\n                "modifier": "CONT\'D"\n            },\n            "dialogue": [\n                "--I’m not! I’m trying to save you!"\n            ]\n        }\n   }\n  ```\n- TRANSITION\n  ```js\n   "content": {\n       "text": "SMASH TO:",\n       "metadata": {\n           "x": 448,\n           "y": 720\n       }\n   }\n  ```\n\n## Run tests\n\n```sh\npython -m pytest tests/\n```\n\n## Todos\n\n- [x] Add unit tests\n- [x] Skip to start of screenplay\n- [ ] Add -o flag to set output path\n- [ ] More documentation\n- [ ] Add option to use as a library\n- [ ] detect end of screenplay\n\n## Author\n\n👤 **Egan Bisma**\n\n- Website: egan.dev\n- Github: [@VVNoodle](https://github.com/VVNoodle)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n\n---\n',
    'author': 'VVNoodle',
    'author_email': 'brickkace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SMASH-CUT/screenplay-pdf-to-json',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
