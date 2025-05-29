import React, { useState, FormEvent } from 'react';

interface VideoIdFormProps {
  onSubmitVideoId: (videoId: string) => void;
  isLoading: boolean;
}

const VideoIdForm: React.FC<VideoIdFormProps> = ({ onSubmitVideoId, isLoading }) => {
  const [videoId, setVideoId] = useState<string>('');

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (videoId.trim()) {
      onSubmitVideoId(videoId.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="video-id-form">
      <div>
        <label htmlFor="videoIdInput">
          YouTube Video ID:
        </label>
        <input
          id="videoIdInput"
          type="text"
          value={videoId}
          onChange={(e) => setVideoId(e.target.value)}
          placeholder="e.g., zFMgNw3N-m0"
          disabled={isLoading}
        />
      </div>
      <button 
        type="submit" 
        disabled={isLoading || !videoId.trim()}
      >
        {isLoading ? 'Loading...' : 'Get Transcript'}
      </button>
    </form>
  );
};

export default VideoIdForm;
