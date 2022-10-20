from google.cloud import translate
import google.auth
from pathlib import Path
import json

root_path = Path('<directory path of *.json file(s)> eg. /home/user/json')
target_path = Path('./directory to save translated json file(s) eg. /home/user/translated')
credentials, project_id = google.auth.default()
client = translate.TranslationServiceClient()
project_id = "<GCP procject_id>"

src_language = 'en-US'
target_language = 'is-IS'


def walk_json(node, translate):
    if isinstance(node, dict):
        return dict([(k, translate(v) if type(v) == str else walk_json(v, translate)) for k, v in node.items()])
    elif isinstance(node, list):
        return [translate(v) if type(v) == str else walk_json(v, translate) for v in node]
    elif type(node) == str:
        return translate(node)
    else:
        return 'null' if not node else translate(node)


def translate_txt(txt):
    translations = client.translate_text(
        request={
            "parent": f"projects/{project_id}",
            "contents": [txt],
            "mime_type": "text/plain",
            "source_language_code": src_language,
            "target_language_code": target_language
        }
    )
    return 'no translation' if not translations.translations else translations.translations[0].translated_text


for f in root_path.glob('*.json'):
    with f.open() as json_file:
        translated = walk_json(json.loads(json_file.read()), translate_txt)

        with open(target_path / f.name, 'w', encoding='utf-8') as target_file:
            target_file.write(json.dumps(translated, indent=4, ensure_ascii=False))

