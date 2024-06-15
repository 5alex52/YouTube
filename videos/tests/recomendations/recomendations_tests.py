import pytest
from src.videos.service import VideoService


def test_get_relevant_videos(tag_views, videos):
    expected_result = ['2', '3', '1', '4']
    result = VideoService.get_relevant_videos(tag_views, videos)
    assert result == expected_result

def test_get_relevant_videos_top_n(tag_views, videos):
    top_n = 2
    expected_result = ['2', '3']
    result = VideoService.get_relevant_videos(tag_views, videos, top_n=top_n)
    assert result == expected_result
