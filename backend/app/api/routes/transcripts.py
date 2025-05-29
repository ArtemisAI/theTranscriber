"""/transcripts API endpoint – fetches transcripts for a video."""

from typing import List
import logging # For logging actual errors

from fastapi import APIRouter, HTTPException, Query, Path, Response
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
# Explicitly alias NoTranscriptFound from the library
from youtube_transcript_api import NoTranscriptFound as YTNoTranscriptFound
from youtube_transcript_api.formatters import JSONFormatter, TextFormatter

# Pydantic Models
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class TranscriptSegment(BaseModel):
    text: str
    start: float
    duration: float

class TranscriptResponse(BaseModel):
    video_id: str
    transcript: List[TranscriptSegment]


router = APIRouter(prefix="/transcripts")

@router.get("/{video_id}", response_model=TranscriptResponse, responses={
    200: {
        "content": {
            "application/json": {},
            "text/plain": {}
        },
        "description": "Successfully retrieved transcript.",
    },
    404: {"description": "Transcript not found or disabled"},
    500: {"description": "Internal server error"},
})
async def get_transcript_by_video_id(
    video_id: str = Path(..., description="The YouTube video ID"),
    format: str = Query("json", pattern="^(json|text)$", description="Format of the transcript (json or text)"),
):
    """
    Retrieve transcript for a given YouTube video ID.
    """
    logger.info(f"Request for transcript: video_id='{video_id}', format='{format}'")
    try:
        # This call itself can raise TranscriptsDisabled or other specific errors for invalid video IDs.
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        transcript_to_fetch = None
        try:
            # Attempt to find a manually created transcript first
            transcript_to_fetch = transcript_list.find_manually_created_transcript()
        except YTNoTranscriptFound:
            logger.info(f"No manually created transcript found for video ID: {video_id}. Trying generated.")
            try:
                # If no manual transcript, try to find a generated one
                transcript_to_fetch = transcript_list.find_generated_transcript()
            except YTNoTranscriptFound:
                logger.warning(f"No transcript found (manual or generated) for video ID: {video_id}")
                raise HTTPException(status_code=404, detail="No transcript found for this video.")
        
        if transcript_to_fetch: # Check if a transcript object was actually found
            logger.info(f"Transcript found (type: {'manual' if transcript_to_fetch.is_manually_created else 'generated'}) for video_id='{video_id}'")
        else: # Should ideally not be reached if previous logic is correct
            logger.error(f"Transcript object (transcript_to_fetch) is None for video ID: {video_id} before fetching. This indicates a logic flaw.")
            raise HTTPException(status_code=500, detail="Internal server error: transcript object not found before fetch.")

        fetched_transcript_segments = transcript_to_fetch.fetch()

        if format == "json":
            formatter = JSONFormatter()
            # The library's JSONFormatter returns a JSON string.
            # We need to parse it to fit our Pydantic model structure.
            formatted_transcript_str = formatter.format_transcript(fetched_transcript_segments)
            import json # Ensure json is imported
            parsed_segments = json.loads(formatted_transcript_str)
            return TranscriptResponse(video_id=video_id, transcript=parsed_segments)
        
        elif format == "text":
            formatter = TextFormatter()
            formatted_transcript_text = formatter.format_transcript(fetched_transcript_segments)
            return Response(content=formatted_transcript_text, media_type="text/plain")

    except TranscriptsDisabled:
        logger.warning(f"Transcripts disabled for video ID: {video_id}")
        raise HTTPException(status_code=404, detail="Transcripts are disabled for this video.")
    except YTNoTranscriptFound: 
        logger.warning(f"A NoTranscriptFound exception was caught at an outer level for video ID: {video_id}")
        raise HTTPException(status_code=404, detail="No transcript available for this video (outer catch).")
    except HTTPException as http_exc: # Explicitly re-raise HTTPException
        raise http_exc
    except Exception as e:
        logger.exception(f"An unexpected error occurred while fetching transcript for video ID {video_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
