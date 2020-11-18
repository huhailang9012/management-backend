

class Matched_Information(object):

    def __init__(self, audio_id: str, audio_name: str, cloud_video_path: str, cloud_cover_path: str, total_time: float, fingerprint_time: float, query_time: float,
                 align_time: float, related_audios: list, date_created: str):
        self.audio_id = audio_id
        self.audio_name = audio_name
        self.cloud_video_path = cloud_video_path
        self.cloud_cover_path = cloud_cover_path
        self.total_time = total_time
        self.fingerprint_time = fingerprint_time
        self.align_time = align_time
        self.query_time = query_time
        self.related_audios = related_audios
        self.date_created = date_created
