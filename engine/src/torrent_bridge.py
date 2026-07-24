class TorrentBridge:
    @staticmethod
    def acestream_to_http(acestream_id: str) -> str:
        return f"http://127.0.0.1:6878/ace/getstream?id={acestream_id}"
        
    @staticmethod
    def magnet_to_http(magnet_link: str) -> str:
        return f"http://127.0.0.1:8080/magnet?link={magnet_link}"
