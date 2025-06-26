# micropython_copy.py

def get_between(text: str, start: str, end: str):
    '''
    文字列 text から、先頭文字列 start、終了文字列 endで挟まれた文字列を抽出して返す。
    条件を満たすが内容が空の場合は空文字列を返す。
    条件を満たさない場足は Falseを返す。
    '''
    if text.startswith(start):
        text = text[len(start):]
        if text.endswith(end):
            return text[:-len(end)]
    return False

def is_between(text: str, start: str, end: str) -> bool:
    '''
    文字列 text から、先頭文字列 start、終了文字列 endで挟まれた文字列が存在するかどうかを判定する。
    条件を満たし内容が空でない場合は True を返す。
    条件を満たさない場合（デリミタがない、中身が空、など）は False を返す。
    '''
    if text.startswith(start):
        text = text[len(start):]
        if text.endswith(end):
            return bool(text[:-len(end)])
    return False

