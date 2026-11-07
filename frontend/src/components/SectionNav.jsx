import React from 'react';
import {
  Image as FileImage,
  Video as FileVideo,
  Music as FileAudio,
  FileText,
  FileSpreadsheet,
  Archive,
  Code2
} from 'lucide-react';

const SECTIONS = [
  { id: 'image',    label: 'Images',    icon: FileImage },
  { id: 'video',    label: 'Video',     icon: FileVideo },
  { id: 'audio',    label: 'Audio',     icon: FileAudio },
  { id: 'pdf',      label: 'PDF',       icon: FileText },
  { id: 'document', label: 'Docs',      icon: FileSpreadsheet },
  { id: 'archive',  label: 'Archives',  icon: Archive },
  { id: 'code',     label: 'Code',      icon: Code2 },
];

export default function SectionNav({ active, onSelect }) {
  return (
    <div className="w-full flex justify-center py-1">
      <nav className="inline-flex items-center gap-1 sm:gap-1.5 p-1.5 rounded-2xl bg-slate-100/90 dark:bg-[#111111]/90 backdrop-blur-md border border-slate-200/80 dark:border-[#222222] shadow-sm max-w-full overflow-x-auto no-scrollbar scroll-smooth">
        {SECTIONS.map(s => {
          const Icon = s.icon;
          const isActive = active === s.id;
          return (
            <button
              key={s.id}
              type="button"
              onClick={() => onSelect(s.id)}
              className={`flex items-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl text-xs sm:text-sm font-medium transition-all duration-200 cursor-pointer flex-shrink-0 whitespace-nowrap select-none
                ${isActive
                  ? 'bg-[#fc6203] text-white dark:text-black dark:font-semibold shadow-[0_0_15px_rgba(252,98,3,0.45)]'
                  : 'text-slate-600 dark:text-neutral-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/60 dark:hover:bg-[#1a1a1a]'
                }`}
            >
              <Icon className={`w-3.5 h-3.5 sm:w-4 sm:h-4 transition-transform duration-200 ${isActive ? 'scale-110' : ''}`} />
              <span>{s.label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}
