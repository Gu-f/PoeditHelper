import os
import zipfile
import ctranslate2
import argostranslate.package
import argostranslate.translate


class TranslateModels(object):
    def __init__(self):
        self.models = []
        self.source_items = set()
        self.target_items = set()

    def search_model_package_by_category(self, category):
        for model_name in self.models:
            if category in model_name:
                return model_name.split('.')[0]
        return None

    def add_model(self, model_name):
        self.models.append(model_name)
        lang_category = model_name.split('-')[1]
        source_lang = lang_category.split('_')[0]
        target_lang = lang_category.split('_')[1]
        self.source_items.add(source_lang)
        self.target_items.add(target_lang)


class AITranslater(object):
    def __init__(self):
        self.translator = None

        models_dir = os.path.join(os.getcwd(), "models")
        self.translate_models = TranslateModels()
        for filename in os.listdir(models_dir):
            if filename.endswith(".argosmodel") and filename.startswith("translate-"):
                self.translate_models.add_model(filename)

        self.extract_dir = os.path.join(os.getcwd(), "models", "packages")

        for model_name in self.translate_models.models:
            model_file = os.path.join(models_dir, model_name)
            if not os.path.exists(os.path.join(self.extract_dir, model_name.split('.')[0])):
                if not zipfile.is_zipfile(model_file):
                    raise Exception(f"{model_file} 不是一个有效的Argos Model")
                with zipfile.ZipFile(model_file, "r") as zipf:
                    zipf.extractall(path=self.extract_dir)

    def init_translater(self, category, device='cpu'):
        package = self.translate_models.search_model_package_by_category(category=category)
        if package:
            pkg = argostranslate.package.Package(package_path=os.path.join(self.extract_dir, package))
            self.translator = argostranslate.translate.PackageTranslation(category.split('_')[0], category.split('_')[1], pkg)
            self.translator.translator = ctranslate2.Translator(
                str(pkg.package_path / "model"),
                device=device
            )  # cpu, cuda, auto

    def ai_translate(self, word):
        if not self.translator:
            return "未检测到有效的翻译模型"
        return self.translator.translate(word)


if __name__ == '__main__':
    ai = AITranslater('zh_en')
    print(ai.ai_translate("你好"))
