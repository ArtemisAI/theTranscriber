interface Props {
  content: string;
}

export default function TranscriptViewer({ content }: Props) {
  return (
    <pre
      style={{
        background: "#f5f5f5",
        padding: 16,
        whiteSpace: "pre-wrap",
        borderRadius: 4,
      }}
    >
      {content}
    </pre>
  );
}
