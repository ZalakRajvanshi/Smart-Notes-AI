export default function Header({ onReset }) {
  return (
    <header className="w-full bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
      <h1 className="text-xl font-semibold text-white">
        Smart Notes
      </h1>

      <div className="flex gap-3">
        <button
          onClick={onReset}
          className="px-4 py-2 bg-white text-gray-900 rounded hover:bg-gray-200 transition"
        >
          New Upload
        </button>
      </div>
    </header>
  );
}
