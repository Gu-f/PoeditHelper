import os
import zipfile
import ctranslate2
import argostranslate.package
import argostranslate.translate


class AITranslater(object):
    def __init__(self):
        path = rf"{os.getcwd()}\models\translate-zh_en.argosmodel"
        extract_path = rf"{os.getcwd()}\models\packages"
        if not zipfile.is_zipfile(path):
            raise Exception("Not a valid Argos Model (must be a zip archive)")
        with zipfile.ZipFile(path, "r") as zipf:
            zipf.extractall(path=extract_path)
        pkg = argostranslate.package.Package(package_path=extract_path+r"\translate-zh_en-1_9")
        self.translator = argostranslate.translate.PackageTranslation('zh', 'cn', pkg)
        self.translator.translator = ctranslate2.Translator(
            str(pkg.package_path / "model"),
            device='cpu'
        )  # cpu, cuda, auto

    def ai_translate(self, word):
        return self.translator.translate(word)
