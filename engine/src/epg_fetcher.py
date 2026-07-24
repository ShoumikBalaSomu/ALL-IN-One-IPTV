class EPGFetcher:
    @staticmethod
    async def fetch(url: str) -> str:
        # Mock XMLTV content
        return '<?xml version="1.0" encoding="UTF-8"?><tv></tv>'
