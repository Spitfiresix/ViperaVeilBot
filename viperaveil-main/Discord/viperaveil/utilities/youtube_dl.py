import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})


async def ydlLookup(args):
    with ydl:
        ydltrack = ydl.extract_info(
            args,
            download=False  # We just want to extract the info
        )
    return ydltrack
