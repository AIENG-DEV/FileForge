import React from 'react';
import {
  Image as FileImage,
  Video as FileVideo,
  Music as FileAudio,
  FileText,
  FileSpreadsheet,
  Archive,
  Code2,
  Sparkles
} from 'lucide-react';

const SECTIONS = [
  { id: 'image',    label: 'Images',    icon: FileImage },
  { id: 'video',    label: 'Video',     icon: FileVideo },
  { id: 'audio',    label: 'Audio',     icon: FileAudio },
  { id: 'pdf',      label: 'PDF',       icon: FileText },
  { id: 'document', label: 'Documents', icon: FileSpreadsheet },
  { id: 'archive',  label: 'Archives',  icon: Archive },
  { id: 'code',     label: 'Code/Data', icon: Code2 },
];

export default function SectionNav({ active, onSelect }) {
  return (
    <nav className="flex flex-row md:flex-col gap-1.5 p-1.5 overflow-x-auto no-scrollbar scroll-smooth">
      <div className="hidden md:flex px-3 py-2 text-[11px] font-semibold tracking-wider uppercase text-neutral-400 dark:text-neutral-500 items-center justify-between">
        <span>Categories</span>
        <Sparkles className="w-3 h-3 text-[#fc6203]" />
      </div>
      {SECTIONS.map(s => {
        const Icon = s.icon;
        const isActive = active === s.id;
        return (
          <button
            key={s.id}
            type="button"
            onClick={() => onSelect(s.id)}
            className={`flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-left text-xs sm:text-sm font-medium transition-all duration-200 cursor-pointer flex-shrink-0 whitespace-nowrap
              ${isActive
                ? 'bg-[#fc6203] text-white dark:text-black dark:font-semibold shadow-[0_0_18px_rgba(252,98,3,0.45)]'
                : 'text-slate-600 dark:text-neutral-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-[#171717]'
              }`}
          >
            <Icon className={`w-4 h-4 transition-transform duration-200 ${isActive ? 'scale-110' : ''}`} />
            <span>{s.label}</span>
          </button>
        );
      })}
    </nav>
  );
}
