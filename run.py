import os

start_orig = 25.014; end_orig = 3 * 60 + 21.852
start_mint = 31.463; end_mint = 3 * 60 + 28.406
dur_orig = end_orig - start_orig
dur_mint = end_mint - start_mint
print(dur_orig, dur_mint)
seam = 60 + 18.567

def mod_orig():
    os.system('ffmpeg -y -i orig_hd.mpg -c:v libx264 -preset ultrafast -crf 0 orig_hd.mp4')
    os.system('ffmpeg -y -ss 0 -i orig_hd.mp4 -an -c:v libx264 -c:a aac -preset ultrafast -crf 0 -t {} orig_hd_start.mp4'.format(seam))
    os.system('ffmpeg -y -ss {} -i orig.mp4 -an -c:v libx264 -c:a aac -preset ultrafast -crf 0 orig_end.mp4'.format(seam))
    os.system('ffmpeg -y -i orig_hd_start.mp4 -c:v libx264 -preset ultrafast -crf 0 -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts')
    os.system('ffmpeg -y -i orig_end.mp4 -c:v libx264 -preset ultrafast -crf 0 -bsf:v h264_mp4toannexb -f mpegts intermediate2.ts')
    os.system('ffmpeg -y -i "concat:intermediate1.ts|intermediate2.ts" -c:v libx264 -preset ultrafast -crf 0 -bsf:a aac_adtstoasc origm.mp4')

def run():
    os.system('ffmpeg -y -ss 0 -i origm.mp4 -an -c:v libx264 -c:a aac -preset ultrafast -crf 0 -t {} orig_intro.mp4'.format(start_orig))
    os.system('ffmpeg -y -ss {} -i origm.mp4 -an -c:v libx264 -c:a aac -preset ultrafast -crf 0 -t {} orig_mid.mp4'.format(start_orig, end_orig))
    os.system('ffmpeg -y -i orig_intro.mp4 -an -filter:v "setpts={}*PTS" -preset ultrafast -crf 0 orig_introm.mp4'.format(start_mint / start_orig))
    os.system('ffmpeg -y -i orig_mid.mp4 -an -filter:v "setpts={}*PTS" -preset ultrafast -crf 0 orig_midm.mp4'.format(dur_mint / dur_orig))
    os.system('ffmpeg -y -loop 1 -i filler.jpg -c:v libx264 -t 10 -pix_fmt yuv420p filler.mp4')
    os.system('ffmpeg -y -i orig_introm.mp4 -c:v libx264 -c:a aac -preset ultrafast -crf 0 -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts')
    os.system('ffmpeg -y -i orig_midm.mp4 -c:v libx264 -c:a aac -preset ultrafast -crf 0 -bsf:v h264_mp4toannexb -f mpegts intermediate2.ts')
    os.system('ffmpeg -y -i filler.mp4 -c:v libx264 -c:a aac -preset ultrafast -crf 0 -bsf:v h264_mp4toannexb -f mpegts intermediate3.ts')
    os.system('ffmpeg -y -i "concat:intermediate1.ts|intermediate2.ts|intermediate3.ts" -c:v libx264 -c:a aac -preset ultrafast -crf 0 -bsf:a aac_adtstoasc mintm.mp4')
    os.system('ffmpeg -y -i mintm.mp4 -i mint.mp3 -c:v libx264 -c:a aac -preset ultrafast -crf 0 -map 0:0 -map 1:0 mint.mp4')
    os.system('ffmpeg -y -i mint.mp4 -vcodec ffv1 -acodec pcm_s16le mint.mkv')

mod_orig()
run()

os.system('ffmpeg -i mint_final.mkv -vf scale=960:720 -c:v libx264 -c:a aac -preset ultrafast -crf 0 mint_final_720p.mkv')
os.system('python -m aeneas.tools.execute_task {} {} "task_language=eng|os_task_file_format=srt|is_text_type=plain" {}'.format('mint.mp3', 'mint.txt', 'subtitle.srt'))
