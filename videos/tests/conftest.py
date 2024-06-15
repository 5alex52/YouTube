import pytest
from typing import List, Dict
from src.videos.models import VideoModel, TagModel 


@pytest.fixture
def tag_views():
    return {
        'tag1': 100,
        'tag2': 200,
        'tag3': 300
    }

@pytest.fixture
def videos():
    return [
        VideoModel(id=1, tags=[TagModel(name='tag1'), TagModel(name='tag2')]),
        VideoModel(id=2, tags=[TagModel(name='tag2'), TagModel(name='tag3')]),
        VideoModel(id=3, tags=[TagModel(name='tag1'), TagModel(name='tag3')]),
        VideoModel(id=4, tags=[TagModel(name='tag3')])
    ]
