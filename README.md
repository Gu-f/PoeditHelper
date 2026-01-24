<img src="app/res/logo.png" width=100 height=100 alt="LOGO"/>

# PoeditHelper

[README_EN](README_EN.md)  
基于机器学习翻译库的Poedit翻译助手.

- 机器学习模型翻译
- LLM 大模型智能翻译
- 明/暗模式

## LLM 翻译
- 目前支持的 LLM 供应商
  - Google Ai Studio
  
- 使用大模型翻译前请先配置相关Token，部分地区需要配置代理才能访问。

----

# 演示

## V2
![DemoV2](app/res/PoeditHelperV2.gif)
## V1
![Demo](app/res/PoeditHelper.gif)

# 模型下载

其他语言的翻译模型可从这里下载  
[翻译模型下载]  
https://raw.githubusercontent.com/argosopentech/argospm-index/main/index.json  
[翻译模型下载-dev]  
https://raw.githubusercontent.com/argosopentech/argospm-index-dev/main/index.json

# 经测试

- Windows11
- Python3.11
- Poedit 3.4.4

# 使用

`pip install -r requirements.txt`  
`python main.py`  
然后  
1、 打开Poedit。  
2、 打开PoeditHelper。  
3、 载入po文件。  
4、 选择翻译类型。  
5、 点击Poedit中待翻译文本，PoeditHelper会自动进行翻译。  
5、 点击PoeditHelper中翻译后的文本，会自动填入Poedit。  