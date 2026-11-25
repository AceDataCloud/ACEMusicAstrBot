"""ACE Music tools for AstrBot."""

import asyncio
import json

from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

from .client import invoke


class AceMusicPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def _call(self, operation, values):
        result = await asyncio.to_thread(
            invoke, self.config.get("api_key"), operation, values
        )
        return json.dumps(result, ensure_ascii=False)

    @filter.llm_tool(name="acemusic_generate")
    async def acemusic_generate(
        self, event: AstrMessageEvent, prompt: str, model: str = "acemusic-v1.1"
    ) -> str:
        """Submit one paid song generation. Save its task ID.

        Args:
            prompt(string): Music or lyrics idea.
            model(string): Model.
        """
        return await self._call("generate", {"prompt": prompt, "model": model})

    @filter.llm_tool(name="acemusic_custom")
    async def acemusic_custom(
        self,
        event: AstrMessageEvent,
        lyric: str,
        style: str,
        title: str,
        model: str = "acemusic-v1.1",
    ) -> str:
        """Submit one paid song generation with your own lyrics, style and title.

        Args:
            lyric(string): Lyrics.
            style(string): Musical style.
            title(string): Title.
            model(string): Model.
        """
        return await self._call(
            "custom", {"lyric": lyric, "style": style, "title": title, "model": model}
        )

    @filter.llm_tool(name="acemusic_upload")
    async def acemusic_upload(
        self,
        event: AstrMessageEvent,
        audio_url: str,
        name: str = "",
        audio_id: str = "",
    ) -> str:
        """Import one publicly accessible HTTPS MP3 as a separately priced reference.

        Args:
            audio_url(string): Public HTTPS MP3 URL.
            name(string): Display name.
            audio_id(string): Owned track ID.
        """
        return await self._call(
            "upload", {"audio_url": audio_url, "name": name, "audio_id": audio_id}
        )

    @filter.llm_tool(name="acemusic_cover")
    async def acemusic_cover(
        self,
        event: AstrMessageEvent,
        audio_id: str,
        lyric: str,
        style: str,
        title: str = "",
        audio_influence: float = 60,
    ) -> str:
        """Submit one paid cover using a caller-owned track ID and new lyrics and style.

        Args:
            audio_id(string): Owned track ID.
            lyric(string): Lyrics.
            style(string): Musical style.
            title(string): Title.
            audio_influence(number): Audio influence (1–100).
        """
        return await self._call(
            "cover",
            {
                "audio_id": audio_id,
                "lyric": lyric,
                "style": style,
                "title": title,
                "audio_influence": audio_influence,
            },
        )

    @filter.llm_tool(name="acemusic_mashup")
    async def acemusic_mashup(
        self,
        event: AstrMessageEvent,
        first_audio_id: str,
        second_audio_id: str,
        lyric: str,
        style: str,
        title: str = "",
        audio_influence: float = 60,
    ) -> str:
        """Submit one paid mashup with two distinct, compatible caller-owned track IDs.

        Args:
            first_audio_id(string): First owned track ID.
            second_audio_id(string): Second owned track ID.
            lyric(string): Lyrics.
            style(string): Musical style.
            title(string): Title.
            audio_influence(number): Audio influence (1–100).
        """
        return await self._call(
            "mashup",
            {
                "first_audio_id": first_audio_id,
                "second_audio_id": second_audio_id,
                "lyric": lyric,
                "style": style,
                "title": title,
                "audio_influence": audio_influence,
            },
        )

    @filter.llm_tool(name="acemusic_lyrics")
    async def acemusic_lyrics(
        self, event: AstrMessageEvent, prompt: str, style: str = ""
    ) -> str:
        """Request paid lyrics independently. The reply may contain lyrics or a pending task ID.

        Args:
            prompt(string): Music or lyrics idea.
            style(string): Musical style.
        """
        return await self._call("lyrics", {"prompt": prompt, "style": style})

    @filter.llm_tool(name="acemusic_retrieve")
    async def acemusic_retrieve(self, event: AstrMessageEvent, task_id: str) -> str:
        """Read the same task ID. Inspect its state and response for tracks or lyrics.

        Args:
            task_id(string): Task ID.
        """
        return await self._call("retrieve", {"task_id": task_id})

    @filter.llm_tool(name="acemusic_batch")
    async def acemusic_batch(self, event: AstrMessageEvent, task_ids: str) -> str:
        """Read 1 to 100 existing task IDs, one per line.

        Args:
            task_ids(string): Task IDs (one per line).
        """
        return await self._call("batch", {"task_ids": task_ids})

    @filter.llm_tool(name="acemusic_history")
    async def acemusic_history(
        self, event: AstrMessageEvent, page: int = 1, page_size: int = 20
    ) -> str:
        """Read one page of the authenticated application’s task history.

        Args:
            page(number): Page (1–10001).
            page_size(number): Items per page (1–100).
        """
        return await self._call("history", {"page": page, "page_size": page_size})
