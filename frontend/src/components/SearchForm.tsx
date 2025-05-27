import { FormEvent, useState } from "react";
import axios from "axios";

interface Props {
  onTranscriptFetched: (content: string) => void;
}

export default function SearchForm({ onTranscriptFetched }: Props) {
  const [videoId, setVideoId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!videoId) return;
    setLoading(true);
    setError(null);

    try {
      // Simple call to backend (format=json). Adjust path if changed.
      const response = await axios.get(`/transcripts?id=${videoId}&format=text`);
      onTranscriptFetched(response.data);
    } catch (err) {
      setError("Failed to fetch transcript. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
      <label>
        Video ID (e.g. dQw4w9WgXcQ):
        <input
          type="text"
          value={videoId}
          onChange={(e) => setVideoId(e.target.value)}
          style={{ marginLeft: 8, width: 300 }}
        />
      </label>
      <button type="submit" style={{ marginLeft: 12 }} disabled={loading}>
        {loading ? "Fetching…" : "Get Transcript"}
      </button>
      {error && (
        <p style={{ color: "red", marginTop: 8 }}>
          {error}
        </p>
      )}
    </form>
  );
}
