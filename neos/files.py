import os
import time

def get_localtime(etime: int | None = None, tzone: int = 9):
    ''' ローカルタイムを取得する '''
    if etime is None:
        etime = time.time()
    return time.gmtime(etime + tzone * 3600)


def str_ftime(timestamp_seconds):
    t = get_localtime(timestamp_seconds, tzone=9)
    # 年/月/日 時:分:秒 の形式でフォーマット
    return f"{t[0]:04d}/{t[1]:02d}/{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

def show_files(path='/', indent=0):
    """
    指定されたパス以下のファイルとディレクトリを再帰的にリスト表示します。
    ファイル名、サイズ、最終更新日時を表示します。
    """
    try:
        contents = os.listdir(path)
        
        # ディレクトリ一覧
        directories = sorted([c for c in contents if (os.stat(f"{path}/{c}")[0] & 0o170000) == 0o040000])
        # ファイル一覧
        files = sorted([c for c in contents if (os.stat(f"{path}/{c}")[0] & 0o170000) == 0o100000])

        current_indent = "  " * indent

        for item in directories:
            full_path = f"{path}/{item}"
            print(f"{current_indent}{item}/")
            show_files(full_path, indent + 1)
        
        for item in files:
            full_path = f"{path}/{item}"
            try:
                stats = os.stat(full_path)
                file_size = stats[6]
                m_time = str_ftime(stats[8])     # last modified timeのつもり
            

                print(f"{current_indent}{item:<16} {file_size:>10,} bytes  {m_time}")
            except OSError as e:
                print(f"{current_indent}{item:<16} Error getting info: {e}")

    except OSError as e:
        print(f"Error accessing path '{path}': {e}")


# ルートディレクトリから探索を開始
show_files()
