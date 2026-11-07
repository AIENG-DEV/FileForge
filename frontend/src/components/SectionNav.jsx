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
    <div className="w-full flex justify-center px-1">
      {/* ReactBits Liquid Glass Floating Dock (Zero Scrollbar) */}
      <nav
        className="inline-flex items-center gap-1 sm:gap-1.5 p-1.5 rounded-2xl sm:rounded-full glass-panel max-w-full overflow-x-auto no-scrollbar scroll-smooth"
        aria-label="Format Categories"
      >
        {SECTIONS.map(s => {
          const Icon = s.icon;
          const isActive = active === s.id;
          return (
            <button
              key={s.id}
              type="button"
              onClick={() => onSelect(s.id)}
              className={`relative flex items-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-xl sm:rounded-full text-xs sm:text-sm font-medium cursor-pointer flex-shrink-0 whitespace-nowrap select-none spring-pill
                ${isActive
                  ? 'bg-[#fc6203] text-black font-bold shadow-[0_0_20px_rgba(252,98,3,0.65)] scale-[1.03]'
                  : 'text-slate-600 dark:text-neutral-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/50 dark:hover:bg-white/10'
                }`}
            >
              <Icon className={`w-3.5 h-3.5 sm:w-4 sm:h-4 ${isActive ? 'stroke-[2.5]' : ''}`} />
              <span>{s.label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}
