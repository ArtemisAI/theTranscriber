import { useState } from "react";
import SearchForm from "./components/SearchForm";
import TranscriptViewer from "./components/TranscriptViewer";

export default function App() {
  const [transcript, setTranscript] = useState<string | null>(null);

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: 20 }}>
      <h1>YouTube Transcript Retrieval (Demo)</h1>

      <SearchForm onTranscriptFetched={setTranscript} />

      {transcript && (
        <>
          <h2>Transcript</h2>
          <TranscriptViewer content={transcript} />
        </>
      )}
    </main>
  );
}
