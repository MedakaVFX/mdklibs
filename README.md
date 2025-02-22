# mdklibs
---
VFX用Pythonライブラリ
- Linux、Mac、Windowsクロスプラットフォーム

## v0.0.1 2024/12/03
- added : 基本構造作成
  - added : mdklibs.date モジュール
  - added : mdklibs.file モジュール
  - added : mdklibs.path モジュール
  - added : mdklibs.qt モジュール


## Recommended 
| Name | Version | Description |
| ---- | ---- | ---- |
| Python | 3.12.x |
| PySide | 6 (Qt 6.8.0.1) |


## Environment Variables
- 環境変数は`大文字` (UNIX系は大文字、小文字が指定出来るが、Windowsが大文字、小文字の概念が無い場合があるため)

| Vars | Description |
| ---- | ---- |
| MDK_DEBUG | デバッグモード 0 or 1 |

## Comment
- added : test module #1
- changed : test #1
- updated : test #1
- fixed : test #1

## Examples
基本
``` python
import mdklibs as mdk

mdk.version()
# v0.0.1

mdk.name()
# mdklibs

# ---------------------
# mdk.libs
mdk.path.get_versions('c:/t-yamagishi/v01/asset_v0002.mb')
# ['v01', 'v0002']

mdk.path.version_up('c:/t-yamagishi/v01/asset_v0002.mb')
# 'c:/t-yamagishi/v02/asset_v0003.mb'

mdk.path.open_in_explorer('c:/t-yamagishi/v01/asset_v0002.mb')

# ---------------------
# mdk.file
mdk.file.open_file('C:\Users\ta_yamagishi\temp\pic001.png')
mdk.file.save_text(<filepath>, 'test')
mdk.file.save_json(<filepath>, <dict>)
mdk.file.save_csv(<filepath>, <list[list[str]]>)
```

## パス式の評価
| Vars | Description |
| ---- | ---- |
| {} | {}で囲むことでエクスプレッション評価をします |
| {`str`} | {}内に文字を書くと変数名になります。 |
| %expr% | %name% 関数名 |
| {`int`} | {1} 引数の番号 |
| {&`str`} | {} 内で&から始まる文字はexpr名 |


``` python
import mdklibs as mdk

ROOT = r'C:\Users\ta_yamagishi\temp\show'

VARS = {
    'ASSET':'CharaA',
    'TASK': 'Modeling',
}

EXPRS = {
    'asset_scene': r'{ASSET}_{TASK}_{ELEMENT}',
    'shot_code': r'{EPI}_{SEQ}_{SHOT}',
    'shot_scene': r'{EPI}_{SEQ}_{SHOT}_{TASK}_{ELEMENT}',
}


# エクスプレッションをセット
_path.set_exprs(EXPRS)

# 変数をセット
_path.set_vars(VARS)

# 変数をセット
_path.set_var('ASSET', 'CreatureA')

# エクスプレッションを評価
_expr = r'_expr = r'{ROOT}/assets/{ASSET}/publish/{TASK}/%new_version%/{&asset_scene}_%new_version%{EXT}'
_result = mdk.Path.eval(_expr, '.ma')
print(_result)
# C:/Users/ta_yamagishi/temp/show/assets/CharaA/publish/modeling/v0001/CharaA_modeling_head_v0001.mb

_expr = r'{ROOT}/{SHOW}/dailies/dailies_{DEP}_{YYYY}{MM}{DD}'
_result = _path.eval(_expr)
print(_result)
# C:\Users\ta_yamagishi\temp\show/PRJ/dailies/dailies_3d_20241108
```