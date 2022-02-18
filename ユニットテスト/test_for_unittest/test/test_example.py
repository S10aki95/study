"""
pytestのフィクスチャについての確認を行う。
"myproject\example.py"にある、ファイルのテスト実行用のスクリプト

# 注意事項：
1. ファイル名の頭に"test_"を付ける。
2. 

"""

# 定義した関数をインポート
import pytest
from src.example import load_numbers_sorted, load_numbers_sorted_error


# フィクスチャを作成
@pytest.fixture
def txt(tmpdir):# -> str:
    with open('numbers.txt', 'w') as f:
        for n in [2, 5, 4, 3, 1]:
            f.write('{}\n'.format(n))
    
    yield 'numbers.txt'



# 正解用の関数を実行：
# エラーは出力されない
def test_load_numbers_sorted(txt):
    assert load_numbers_sorted(txt) == [1, 2, 3, 4, 5]

# 正解用の関数を実行：
# エラーが出力される(すべてのエラー出力を確認するにはコマンド入力時に -vを付けるか、)
def test_load_numbers_sorted_2(txt):
    assert load_numbers_sorted_error(txt) == [1, 2, 3, 4, 5]
