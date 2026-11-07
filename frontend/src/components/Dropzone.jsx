import React, { useRef, useState } from 'react';
import { UploadCloud, FolderUp, FileCheck2 } from 'lucide-react';

export default function Dropzone({ onFiles, accept = '*', category = 'any' }) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef();

  const handle = (files) => {
    const arr = Array.from(files).filter(f => f.size > 0);
    if (arr.length) onFiles(arr);
  };

  return (
    <div
      onDragOver={e => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={e => { e.preventDefault(); setDragging(false); handle(e.dataTransfer.files); }}
      onClick={() => inputRef.current.click()}
      className={`relative border-2 border-dashed rounded-2xl sm:rounded-3xl p-6 sm:p-10 text-center cursor-pointer transition-all duration-300 select-none
        ${dragging
          ? 'border-[#fc6203] bg-orange-50/20 dark:bg-[#150a04] shadow-[0_0_30px_rgba(252,98,3,0.35)] scale-[1.01]'
          : 'border-slate-300 dark:border-[#222222] bg-white dark:bg-[#0a0a0a] hover:border-[#fc6203] hover:shadow-[0_0_20px_rgba(252,98,3,0.2)]'
        }`}
    >
      <input
        ref={inputRef}
        type="file"
        multiple
        accept={accept}
        className="hidden"
        onChange={e => handle(e.target.files)}
      />

      {/* Modern Icon with Glowing Ring */}
      <div className="flex justify-center mb-4">
        <div className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-300
          ${dragging
            ? 'bg-[#fc6203] text-black shadow-[0_0_25px_rgba(252,98,3,0.8)]'
            : 'bg-slate-100 dark:bg-[#141414] text-[#fc6203] border border-slate-200 dark:border-[#222222]'
          }`}
        >
          {dragging ? (
            <FolderUp className="w-8 h-8 animate-bounce" />
          ) : (
            <UploadCloud className="w-8 h-8 transition-transform duration-200" />
          )}
        </div>
      </div>

      <p className="text-lg font-semibold text-slate-800 dark:text-neutral-100">
        {dragging ? 'Drop your files now!' : `Upload ${category} files`}
      </p>

      <p className="text-xs text-slate-500 dark:text-neutral-400 mt-1.5 flex items-center justify-center gap-1.5">
        <FileCheck2 className="w-3.5 h-3.5 text-[#fc6203]" />
        Drag and drop files here, or click to browse
      </p>

      {accept && accept !== '*' && (
        <div className="mt-4 inline-flex items-center gap-1 px-3 py-1 rounded-full text-[11px] font-mono
          bg-slate-100 dark:bg-[#141414] text-slate-600 dark:text-neutral-400 border border-slate-200 dark:border-[#222222]">
          <span className="text-[#fc6203] font-bold">Formats:</span> {accept.replace(/\./g, ' ').toUpperCase()}
        </div>
      )}
    </div>
  );
}
