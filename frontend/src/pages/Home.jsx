import { useState } from "react";
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
    <>
      {!data && (
        <div className="flex justify-center mt-24">
          <div className="w-full max-w-2xl bg-gray-900 p-8 rounded-xl">
            <UploadBox onUploadReady={setFileFn} />

            <button
              disabled={!fileFn || loading}
              onClick={generateNotes}
              className={`w-full mt-6 py-3 rounded-lg text-lg font-semibold text-white transition-all
                ${
                  !fileFn
                    ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                    : "bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 shadow-lg"
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
    </>
  );
}
