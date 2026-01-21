import { useState } from "react";
import axios from "axios";

export default function UploadBox({ onUploadReady }) {
  const [fileName, setFileName] = useState("");
  const [preview, setPreview] = useState(null);

  async function handleFile(e) {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setPreview(URL.createObjectURL(file));

    onUploadReady(async () => {
      const form = new FormData();
      form.append("file", file);

      const res = await axios.post(
        "http://127.0.0.1:8000/process",
        form
      );

      return res.data;
    });
  }

  return (
    <div className="border-2 border-dashed border-gray-600 p-8 rounded-lg text-center">
      {!preview && (
        <>
          <p className="text-gray-400 mb-4">
            Upload handwritten notes (JPG / PNG)
          </p>

          <label className="cursor-pointer bg-white text-gray-900 px-5 py-2 rounded hover:bg-gray-700">
            Select File
            <input type="file" hidden onChange={handleFile} />
          </label>
        </>
      )}

      {preview && (
        <div className="flex flex-col items-center gap-4">
          <img
            src={preview}
            alt="preview"
            className="max-h-48 rounded border"
          />

          <p className="text-sm text-gray-300">
            Uploaded: <span className="font-medium">{fileName}</span>
          </p>

          <label className="cursor-pointer text-blue-400 underline">
            Change file
            <input type="file" hidden onChange={handleFile} />
          </label>
        </div>
      )}
    </div>
  );
}
