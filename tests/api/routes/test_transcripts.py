"""Tests for the /transcripts API endpoint."""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock

# Import the actual exceptions from the library
from youtube_transcript_api import TranscriptsDisabled, NoTranscriptFound

from app.main import app  # Ensure app is imported for client

# Constants for video IDs used in tests
MOCKED_SUCCESS_VIDEO_ID = "mockedSuccessVideo"
DISABLED_VIDEO_ID = "disabledVideo"
NO_TRANSCRIPT_VIDEO_ID = "noTranscriptVideo"
GENERATED_ONLY_VIDEO_ID = "generatedOnlyVideo"
FETCH_ERROR_VIDEO_ID = "fetchErrorVideo"
UNEXPECTED_LIST_ERROR_VIDEO_ID = "unexpectedListErrorVideo"

# Sample transcript data for mocking
SAMPLE_TRANSCRIPT_SEGMENTS = [
    {"text": "Hello world", "start": 0.5, "duration": 1.5},
    {"text": "This is a test", "start": 2.0, "duration": 2.5},
]

@pytest.mark.asyncio
@patch("app.api.routes.transcripts.YouTubeTranscriptApi.list_transcripts")
async def test_get_transcript_json_success(mock_list_transcripts):
    """Test successful retrieval of transcript in JSON format (mocked)."""
    video_id = MOCKED_SUCCESS_VIDEO_ID

    mock_transcript_data = MagicMock() 
    mock_transcript_data.fetch.return_value = SAMPLE_TRANSCRIPT_SEGMENTS

    mock_transcript_list_obj = MagicMock() 
    mock_transcript_list_obj.find_manually_created_transcript = MagicMock(return_value=mock_transcript_data)
    mock_list_transcripts.return_value = mock_transcript_list_obj

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}?format=json")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert data["video_id"] == video_id
    assert data["transcript"] == SAMPLE_TRANSCRIPT_SEGMENTS
    mock_list_transcripts.assert_called_once_with(video_id)
    mock_transcript_list_obj.find_manually_created_transcript.assert_called_once()
    mock_transcript_data.fetch.assert_called_once()


@pytest.mark.asyncio
@patch("app.api.routes.transcripts.YouTubeTranscriptApi.list_transcripts")
async def test_get_transcript_text_success(mock_list_transcripts):
    """Test successful retrieval of transcript in TEXT format (mocked)."""
    video_id = MOCKED_SUCCESS_VIDEO_ID

    mock_transcript_data = MagicMock()
    mock_transcript_data.fetch.return_value = SAMPLE_TRANSCRIPT_SEGMENTS

    mock_transcript_list_obj = MagicMock()
    mock_transcript_list_obj.find_manually_created_transcript = MagicMock(return_value=mock_transcript_data)
    mock_list_transcripts.return_value = mock_transcript_list_obj
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}?format=text")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert "Hello world" in response.text 
    assert "This is a test" in response.text
    mock_list_transcripts.assert_called_once_with(video_id)
    mock_transcript_list_obj.find_manually_created_transcript.assert_called_once()
    mock_transcript_data.fetch.assert_called_once()

@pytest.mark.asyncio
@patch("app.api.routes.transcripts.YouTubeTranscriptApi.list_transcripts")
async def test_get_transcript_default_format_is_json(mock_list_transcripts):
    """Test that the default format is JSON when not specified (mocked)."""
    video_id = MOCKED_SUCCESS_VIDEO_ID
    
    mock_transcript_data = MagicMock()
    mock_transcript_data.fetch.return_value = SAMPLE_TRANSCRIPT_SEGMENTS
    mock_transcript_list_obj = MagicMock()
    mock_transcript_list_obj.find_manually_created_transcript = MagicMock(return_value=mock_transcript_data)
    mock_list_transcripts.return_value = mock_transcript_list_obj

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}") 
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert data["video_id"] == video_id
    assert data["transcript"] == SAMPLE_TRANSCRIPT_SEGMENTS
    mock_list_transcripts.assert_called_once_with(video_id)

@pytest.mark.asyncio
@patch("app.api.routes.transcripts.YouTubeTranscriptApi.list_transcripts")
async def test_get_transcript_transcripts_disabled(mock_list_transcripts):
    """Test response when transcripts are disabled for a video."""
    video_id = DISABLED_VIDEO_ID
    
    mock_list_transcripts.side_effect = TranscriptsDisabled(video_id)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}?format=json")
        
    assert response.status_code == 404
    assert response.json() == {"detail": "Transcripts are disabled for this video."}
    mock_list_transcripts.assert_called_once_with(video_id)

@pytest.mark.asyncio
@patch("app.api.routes.transcripts.YouTubeTranscriptApi.list_transcripts")
async def test_get_transcript_no_transcript_found(mock_list_transcripts):
    """Test response when no transcript is found (manual or generated)."""
    video_id = NO_TRANSCRIPT_VIDEO_ID
    
    mock_actual_transcript_list = MagicMock()
    
    mock_find_manual = MagicMock()
    # Use full constructor for NoTranscriptFound
    mock_find_manual.side_effect = NoTranscriptFound(
        video_id=video_id, requested_language_codes=['en'], transcript_data={}
    )
    mock_actual_transcript_list.find_manually_created_transcript = mock_find_manual

    mock_find_generated = MagicMock()
    mock_find_generated.side_effect = NoTranscriptFound(
        video_id=video_id, requested_language_codes=['en'], transcript_data={}
    )
    mock_actual_transcript_list.find_generated_transcript = mock_find_generated
    
    mock_list_transcripts.return_value = mock_actual_transcript_list
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}?format=json")
        
    assert response.status_code == 404
    assert response.json() == {"detail": "No transcript found for this video."}
    mock_list_transcripts.assert_called_once_with(video_id)
    mock_actual_transcript_list.find_manually_created_transcript.assert_called_once()
    mock_actual_transcript_list.find_generated_transcript.assert_called_once()


@pytest.mark.asyncio
async def test_get_transcript_invalid_format_parameter():
    """Test response when an invalid 'format' query parameter is provided."""
    video_id = "any_video_id" 
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}?format=invalid_format")
        
    assert response.status_code == 422 
    assert response.json()["detail"][0]["type"] == "string_pattern_mismatch"
    assert response.json()["detail"][0]["loc"] == ["query", "format"]

@pytest.mark.asyncio
@patch("app.api.routes.transcripts.YouTubeTranscriptApi.list_transcripts")
async def test_get_transcript_only_generated_exists(mock_list_transcripts):
    """Test fetching a transcript when only a generated one exists."""
    video_id = GENERATED_ONLY_VIDEO_ID
    
    mock_generated_transcript_data = MagicMock() 
    mock_generated_transcript_data.fetch.return_value = SAMPLE_TRANSCRIPT_SEGMENTS
    
    mock_actual_transcript_list = MagicMock() 

    mock_find_manual = MagicMock()
    # Use full constructor for NoTranscriptFound
    mock_find_manual.side_effect = NoTranscriptFound(
        video_id=video_id, requested_language_codes=['en'], transcript_data={}
    )
    mock_actual_transcript_list.find_manually_created_transcript = mock_find_manual
    
    mock_find_generated = MagicMock(return_value=mock_generated_transcript_data)
    mock_actual_transcript_list.find_generated_transcript = mock_find_generated
    
    mock_list_transcripts.return_value = mock_actual_transcript_list
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}?format=json")
        
    assert response.status_code == 200
    data = response.json()
    assert data["video_id"] == video_id
    assert data["transcript"] == SAMPLE_TRANSCRIPT_SEGMENTS
    mock_list_transcripts.assert_called_once_with(video_id)
    mock_actual_transcript_list.find_manually_created_transcript.assert_called_once()
    mock_actual_transcript_list.find_generated_transcript.assert_called_once()
    mock_generated_transcript_data.fetch.assert_called_once()


@pytest.mark.asyncio
@patch("app.api.routes.transcripts.YouTubeTranscriptApi.list_transcripts")
async def test_get_transcript_list_transcripts_raises_unexpected_error(mock_list_transcripts):
    """Test response for an unexpected error from list_transcripts itself."""
    video_id = UNEXPECTED_LIST_ERROR_VIDEO_ID
    
    mock_list_transcripts.side_effect = Exception("Some internal list_transcripts error")
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}?format=json")
        
    assert response.status_code == 500
    assert "An unexpected error occurred: Some internal list_transcripts error" in response.json()["detail"]
    mock_list_transcripts.assert_called_once_with(video_id)

@pytest.mark.asyncio
@patch("app.api.routes.transcripts.YouTubeTranscriptApi.list_transcripts")
async def test_get_transcript_fetch_raises_unexpected_error(mock_list_transcripts):
    """Test an unexpected error during the .fetch() call."""
    video_id = FETCH_ERROR_VIDEO_ID

    mock_transcript_data = MagicMock() 
    mock_transcript_data.fetch.side_effect = Exception("Unexpected fetch error")

    mock_transcript_list_obj = MagicMock() 
    mock_transcript_list_obj.find_manually_created_transcript = MagicMock(return_value=mock_transcript_data)
    mock_list_transcripts.return_value = mock_transcript_list_obj

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/transcripts/{video_id}?format=json")

    assert response.status_code == 500
    assert "An unexpected error occurred: Unexpected fetch error" in response.json()["detail"]
    mock_list_transcripts.assert_called_once_with(video_id)
    mock_transcript_list_obj.find_manually_created_transcript.assert_called_once()
    mock_transcript_data.fetch.assert_called_once()
