import { useState } from "react";
import Header from "../components/Header";
import UploadBox from "../components/UploadBox";
import NotesView from "../components/NotesView";

export default function Home() {
  const [fileFn, setFileFn] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  async function generateNotes() {
    setLoading(true);
    const res = await fileFn();
    setData(res);
    setLoading(false);
  }

  function reset() {
    setData(null);
    setFileFn(null);
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Header onReset={reset} />

      {!data && (
        <div className="flex justify-center mt-24">
          <div className="w-full max-w-2xl bg-gray-900 p-8 rounded-xl">
            <UploadBox onUploadReady={setFileFn} />

            <button
              disabled={!fileFn || loading}
              onClick={generateNotes}
              className={`w-full mt-6 py-3 rounded-lg text-lg
                ${
                  !fileFn
                    ? "bg-gray-700"
                    : "bg-blue-600 hover:bg-blue-700"
                }`}
            >
              {loading ? "Processing…" : "Generate Notes"}
            </button>
          </div>
        </div>
      )}

      {data && (
        <div className="flex justify-center mt-10 pb-20">
          <NotesView structure={data.structure} />
        </div>
      )}
    </div>
  );
}
