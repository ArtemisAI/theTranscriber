import React, { useState } from 'react';
import VideoIdForm from './components/VideoIdForm';
import TranscriptDisplay from './components/TranscriptDisplay';
import './App.css'; // Import the CSS file

interface BackendTranscriptResponse {
  video_id: string;
  transcript: any[]; // Replace 'any' with a more specific TranscriptSegment[] if defined
}

const App: React.FC = () => {
  const [transcriptData, setTranscriptData] = useState<string | BackendTranscriptResponse['transcript'] | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [currentVideoId, setCurrentVideoId] = useState<string | null>(null);
  // const [format, setFormat] = useState<'json' | 'text'>('json'); // For future format selection

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

  const handleFetchTranscript = async (videoId: string) => {
    setIsLoading(true);
    setError(null);
    setTranscriptData(null);
    setCurrentVideoId(videoId);

    const currentFormat = 'json'; 

    try {
      const response = await fetch(`${API_BASE_URL}/transcripts/${videoId}?format=${currentFormat}`);
      
      if (!response.ok) {
        let errorDetail = `Failed to fetch transcript. Status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorDetail = errorData.detail || errorDetail;
        } catch (e) {
          errorDetail = response.statusText || errorDetail;
        }
        throw new Error(errorDetail);
      }

      if (currentFormat === 'text') {
        const textData = await response.text();
        setTranscriptData(textData);
      } else { 
        const jsonData: BackendTranscriptResponse = await response.json();
        setTranscriptData(jsonData.transcript); 
      }

    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="app-main">
      <header className="app-header">
        <h1>YouTube Transcript Fetcher</h1>
      </header>
      
      <VideoIdForm onSubmitVideoId={handleFetchTranscript} isLoading={isLoading} />
      
      {currentVideoId && !isLoading && !error && transcriptData && (
        <h2 style={{ marginTop: '30px', textAlign: 'center' }}>Transcript for Video ID: {currentVideoId}</h2>
      )}
      
      <TranscriptDisplay
        transcriptData={transcriptData}
        isLoading={isLoading}
        error={error}
        // format={format} 
      />
    </main>
  );
};

export default App;
