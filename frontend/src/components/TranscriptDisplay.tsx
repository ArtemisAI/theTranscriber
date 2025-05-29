import React from 'react';

interface TranscriptSegment {
  text: string;
  start: number;
  duration: number;
}

interface TranscriptDisplayProps {
  transcriptData: string | TranscriptSegment[] | null;
  isLoading: boolean;
  error: string | null;
  // format?: 'json' | 'text'; // Kept for potential future use, but not actively used for rendering logic now
}

const TranscriptDisplay: React.FC<TranscriptDisplayProps> = ({
  transcriptData,
  isLoading,
  error,
  // format = 'json', 
}) => {
  if (isLoading) {
    return <div className="transcript-display-container"><p>Loading transcript...</p></div>;
  }

  if (error) {
    return <div className="transcript-display-container"><p className="error-message">Error: {error}</p></div>;
  }

  if (!transcriptData) {
    return <div className="transcript-display-container"><p>Submit a video ID to see the transcript.</p></div>;
  }

  return (
    <div className="transcript-display-container">
      {typeof transcriptData === 'string' ? (
        <>
          <h3>Transcript (Text)</h3>
          <pre>{transcriptData}</pre>
        </>
      ) : (
        <>
          <h3>Transcript (Segments)</h3>
          <pre>
            {JSON.stringify(transcriptData, null, 2)}
          </pre>
        </>
      )}
    </div>
  );
};

export default TranscriptDisplay;
