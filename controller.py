from fastapi import FastAPI
import requests
import json
from fastapi.middleware.cors import CORSMiddleware
from matched_information import Matched_Information

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://audios.gz2vip.idcfengye.com/#/",
    'http://10.170.213.242:8080',
    'http://audios.gz2vip.idcfengye.com'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
),


@app.get("/app/execute")
def app_execute(related_key: str):
    url = 'http://spider:8000/app/execute/'+related_key
    r = requests.post(url)
    return r.text


@app.get("/spider/callback")
def mainline(video_id: str, local_video_path: str, related_key: str):
    url = 'http://extractor:8000/audio/extract'
    payload = {'video_id': video_id, 'local_video_path': local_video_path}
    r = requests.get(url, params=payload)
    data = json.loads(r.text)
    arr = data['data']
    audio_id = arr['audio_id']
    local_audio_path = arr['local_audio_path']
    url = 'http://recognition:8000/target/audio/recognize'

    payload = {'audio_id': audio_id, 'local_audio_path': local_audio_path, 'related_key': related_key}
    r = requests.get(url, params=payload)
    return r.text


@app.post("/app/start")
def app_start(pkg_name: str, activity: str):
    url = 'http://extractor:8000/audio/extract'
    payload = {'video_id': 'key','local_video_path': 'local_video_path'}
    r = requests.get(url, params=payload)
    return r.text


@app.get("/matched/information/index")
def information_index(related_key: str):
    url = 'http://recognition:8000/matched/information/index'
    payload = {'related_key': related_key}
    r = requests.get(url, params=payload)
    data = json.loads(r.text)
    arr = data['data']
    matched_infos = json.loads(arr)
    if matched_infos:
        audio_ids = list()
        for matched_info in matched_infos:
            audio_id = matched_info['audio_id']
            audio_ids.append(audio_id)
        payload = {'audio_ids': audio_ids}

        ret = requests.get('http://extractor:8000/audio/batch/query', params=payload)
        data = json.loads(ret.text)
        audios = json.loads(data['data'])
        video_ids = list()
        dict = {}
        for audio in audios:
            video_id = audio['video_id']
            video_ids.append(video_id)
            dict[video_id] = audio['id']
        payload = {'video_ids': video_ids}
        ret = requests.get("http://spider:8000/video/batch/query", params=payload)
        data = json.loads(ret.text)
        videos = json.loads(data['data'])
        path_dict = {}
        cover_dict = {}
        for video in videos:
            path_dict[dict[video['id']]] = video['cloud_video_path']
            cover_dict[dict[video['id']]] = video['cloud_cover_path']
        infos = list()
        for matched_info in matched_infos:
            audio_id = matched_info['audio_id']
            audio_name = matched_info['audio_name']
            total_time = matched_info['total_time']
            fingerprint_time = matched_info['fingerprint_time']
            align_time = matched_info['align_time']
            query_time = matched_info['query_time']
            cover_path = cover_dict[audio_id]
            video_path = path_dict[audio_id]
            cover_path = cover_path.replace("minio:9000", "ae.vipgz4.idcfengye.com");
            video_path = video_path.replace("minio:9000", "ae.vipgz4.idcfengye.com");
            related_audios = matched_info['related_audios']
            date_created = matched_info['date_created']
            info = Matched_Information(audio_id, audio_name, video_path, cover_path, total_time, fingerprint_time,
                                       query_time, align_time, related_audios, date_created)
            infos.append(info)
        result = json.dumps(infos, default=lambda obj: obj.__dict__, sort_keys=False, indent=4)
        return {"success": True, "code": 0, "msg": "ok", "data": result}
    else:
        return {"success": True, "code": 0, "msg": "ok"}


@app.get("/source/audio/query")
def app_execute(name: str):
    url = 'http://recognition:8000/source/audio/query'
    payload = {'name': name}
    r = requests.get(url, params=payload)
    return r.text


if __name__ == '__main__':
    url = 'http://extractor:8000/audio/extract'
    payload = {'video_id': 'video_id', 'local_video_path': 'local_video_path'}
    r = requests.get(url, params=payload)
    print(r.text)