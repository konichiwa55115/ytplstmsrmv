from yt_dlp import YoutubeDL
from pyrogram import Client, filters
import os 
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton , ReplyKeyboardMarkup , CallbackQuery , ForceReply,Message
from os import system as cmd
import audioread
import shutil

bot = Client(
    "audiobot",
    api_id=17983098,
    api_hash="ee28199396e0925f1f44d945ac174f64",
    bot_token="5782497998:AAFdx2dX3yeiyDIcoJwPa_ghY2h_dozEh_E"
)
temptxt = "res.txt"
audioexs = [".mp3",".ogg",".m4a"]
videoexs = [".mp4",".mkv",".wmv"]


def musicrmv(x,y):
  
  file_path = x
  user_id = y
  filename = os.path.basename(file_path)
  nom,ex = os.path.splitext(filename)
  mp4file = f"msrmvd{nom}.mp4"
  mp3file = f"{nom}.mp3"
  finalsound = f"{nom}.wav"
  cmd(f'mkdir workdir')
  cmd(f'''ffmpeg -i "{file_path}" -q:a 0 -map a "{mp3file}" -y''')
  def duration_detector(length):
        seconds = length
        return seconds
  with audioread.audio_open(mp3file) as f:
            totalsec = f.duration
  if totalsec<= 100 :
         cmd(f'''spleeter separate -p spleeter:2stems -o workdir "{mp3file}"''')
         if ex in audioexs :
            cmd(f'''ffmpeg -i "./workdir/{nom}/vocals.wav" -q:a 0 -map a "{mp3file}" -y''')
            bot.send_audio(user_id,mp3file,caption=nom)
         elif ex in videoexs :
          cmd(f'''ffmpeg -i "{file_path}" -i "./workdir/{nom}/vocals.wav" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "{mp4file}" -y''')
          bot.send_video(user_id, mp4file,caption=nom)
          os.remove(mp4file)
  else :
        cmd(f'mkdir parts')
        cmd(f'''ffmpeg -i "{mp3file}" -f segment -segment_time 100 -c copy "./parts/rmvd%09d.wav" -y''')
        dir_path = "./parts/"
        numbofitems = len(os.listdir(dir_path))
        for x in range(0,numbofitems):
             myzfillvar = str(x).zfill(9)
             pathy=f"./parts/rmvd{myzfillvar}.wav"
             cmd(f'''spleeter separate -p spleeter:2stems -o workdir "{pathy}"''')
             rmvdvoice = f"./workdir/rmvd{myzfillvar}/vocals.wav"
             with open('list.txt', 'a') as f:
                f.write(f'''file {rmvdvoice} \n''')   
        cmd(f'''ffmpeg -f concat -safe 0 -i list.txt "{finalsound}" -y''')
        if ex in audioexs : 
           cmd(f'''ffmpeg -i "{finalsound}" -q:a 0 -map a "{mp3file}" -y''')
           bot.send_audio(user_id, mp3file,caption=nom)
        elif ex in videoexs : 
             cmd(f'''ffmpeg -i "{file_path}" -i "{finalsound}" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "{mp4file}" -y''')
             bot.send_video(y, mp4file,caption=nom)
             os.remove(mp4file)
        shutil.rmtree('./parts/') 
        os.remove("list.txt")
  shutil.rmtree('./workdir/')
  if os.path.isfile(file_path):
   os.remove(file_path)
  else :
     print("pass anyway !")
  os.remove(mp3file)

@bot.on_message(filters.command('ytplst') & filters.text & filters.private)
def command4(bot,message):
     x = message.text.split(" ")[1]
     url = x.split(" ")[0]
     dlmode = message.text.split(" ")[-1] 
     global ytplstid
     ytplstid = message.from_user.id
     cmd(f'''yt-dlp --flat-playlist -i --print-to-file url ytplst.txt {url}''')
     cmd(f'''wc -l < ytplst.txt > "{temptxt}"''')
     with open(temptxt, 'r') as file:
      temp = file.read().rstrip('\n') 
     global plstnumbofvid
     plstnumbofvid = int(temp) + 1
     os.remove(temptxt)
     if dlmode == "vid" : 
       for i in range(1,plstnumbofvid):
         cmd(f'sed -n {i}p ytplst.txt > "{temptxt}"')
         with open(temptxt, 'r') as file:
           link = file.read().rstrip('\n')  
         with YoutubeDL() as ydl: 
          info_dict = ydl.extract_info(f'{link}', download=False)
          video_url = info_dict.get("url", None)
          video_id = info_dict.get("id", None)
          video_title = info_dict.get('title', None).replace('＂', '').replace('"', '').replace("'", "").replace("｜", "").replace("|", "") 
          mp32file =   f"{video_title}.mp3"
          txtresfile = f"{video_title}.txt"
          mp42file =   f"{video_title}.mp4"
         cmd(f'''yt-dlp -f 18 -ciw  -o "{mp42file}" "{link}"''')
         bot.send_video(ytplstid, mp42file,caption=video_title)
         os.remove(mp42file)
         os.remove(temptxt)
     elif dlmode == "vid720":
      for i in range(1,plstnumbofvid):
         cmd(f'sed -n {i}p ytplst.txt > "{temptxt}"')
         with open(temptxt, 'r') as file:
           link = file.read().rstrip('\n')  
         with YoutubeDL() as ydl: 
          info_dict = ydl.extract_info(f'{link}', download=False)
          video_url = info_dict.get("url", None)
          video_id = info_dict.get("id", None)
          video_title = info_dict.get('title', None).replace('＂', '').replace('"', '').replace("'", "").replace("｜", "").replace("|", "") 
          mp32file =   f"{video_title}.mp3"
          txtresfile = f"{video_title}.txt"
          mp42file =   f"{video_title}.mp4"
         cmd(f'''yt-dlp -f 22 -ciw  -o "{mp42file}" "{link}"''')
         musicrmv(mp42file,ytplstid)
         os.remove(temptxt)
     else : 
      for i in range(1,plstnumbofvid):
         cmd(f'sed -n {i}p ytplst.txt > "{temptxt}"')
         with open(temptxt, 'r') as file:
           link = file.read().rstrip('\n')  
         with YoutubeDL() as ydl: 
          info_dict = ydl.extract_info(f'{link}', download=False)
          video_url = info_dict.get("url", None)
          video_id = info_dict.get("id", None)
          video_title = info_dict.get('title', None).replace('＂', '').replace('"', '').replace("'", "").replace("｜", "").replace("|", "") 
          mp32file =   f"{video_title}.mp3"
          txtresfile = f"{video_title}.txt"
          mp42file =   f"{video_title}.mp4"
         cmd(f'''yt-dlp -ciw  --extract-audio --audio-format mp3  -o "{video_title}"  "{link}"''')
         bot.send_audio(ytplstid, mp32file,caption=video_title)
         os.remove(mp32file)
         os.remove(temptxt)
     os.remove("ytplst.txt")


bot.run()
