import os
import subprocess
from pydub import AudioSegment

# ==========================================
# 步驟 1: 修改這裡！請輸入你 ffmpeg 的 bin 資料夾路徑
# ==========================================
FFMPEG_DIR = r"C:\ffmpeg-8.0.1-essentials_build\bin"  # <--- 請確保這裡面有 ffmpeg.exe 和 ffprobe.exe

# 自動設定路徑
ffmpeg_exe = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
ffprobe_exe = os.path.join(FFMPEG_DIR, "ffprobe.exe")

# 設定給 pydub 使用
AudioSegment.converter = ffmpeg_exe
AudioSegment.ffprobe = ffprobe_exe
os.environ["PATH"] += os.pathsep + FFMPEG_DIR


def convert():
    # 檢查工具是否存在
    if not os.path.exists(ffmpeg_exe):
        print(f"【嚴重錯誤】找不到 ffmpeg.exe！目前設定路徑為: {ffmpeg_exe}")
        print("請確認你的 FFMPEG_DIR 設定是否正確。")
        return

    # 設定檔案路徑
    folder = r"C:\Users\Yun-Tse Kao\Desktop\AIOT\class014"
    filename = "螢幕錄製 2026-01-04 105507.mp4"
    input_path = os.path.join(folder, filename)
    output_path = os.path.join(folder, "01.wav")

    print(f"--- 轉檔檢查 ---")
    print(f"影片路徑: {input_path}")

    if not os.path.exists(input_path):
        print("【錯誤】找不到影片檔，請檢查檔案名稱。")
        return

    try:
        print("正在轉換中... 請稍候...")
        # 讀取並匯出
        audio = AudioSegment.from_file(input_path, format="mp4")
        audio.export(output_path, format="wav")
        print(f"【成功】轉換完成！")
        print(f"存檔位置: {output_path}")
    except Exception as e:
        print(f"【轉換失敗】: {e}")


if __name__ == "__main__":
    convert()
