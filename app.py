import json
import time
from os.path import isdir
from pathlib import Path

from google.cloud import translate

from config import settings

client = translate.TranslationServiceClient()


def walk_strs(node, translate):
    if isinstance(node, dict):
        return dict([(k, translate(v) if type(v) == str else walk_strs(v, translate)) for k, v in node.items()])
    elif isinstance(node, list):
        return [translate(v) if type(v) == str else walk_strs(v, translate) for v in node]
    elif type(node) == str:
        return translate(node)
    else:
        return node


def translate_txt(txt):
    translations = client.translate_text(
        request={
            "parent": f"projects/{settings.gcp_project}",
            "contents": [txt],
            "mime_type": "text/plain",
            "source_language_code": settings.from_lang,
            "target_language_code": settings.to_lang
        }
    )
    return 'no translation' if not translations.translations else translations.translations[0].translated_text


def process_file(src_path, target_path):
    with src_path.open('r', encoding='utf-8') as json_file:
        translated = walk_strs(json.load(json_file), translate_txt)
        translated_path = target_path / src_path.name if isdir(src_path) else src_path.name

        if translated_path.exists():
            existing = translated_path.name
            rename = translated_path.stem + str(time.time_ns())
            translated_path = translated_path.with_stem(rename)
            print(f'translated file {existing} already exists, saving to {translated_path}')


        with open(translated_path, 'w', encoding='utf-8') as target_file:
            print(f'writing translation to {target_file}')
            json.dump(translated, target_file, indent=4, ensure_ascii=False)


def run():
    src = Path(settings.from_path)
    dst = Path(settings.to_path)
    if src.is_dir():
        files = list(src.glob('*.json'))
        print(f'translating {len(files)} .json files from {src}')
        for f in files:
            print(f'translating file: {f}')
            process_file(f, dst)
    else:
        print(f'translating 1 file: {src}')
        process_file(src, dst)


if __name__ == "__main__":
    run()
