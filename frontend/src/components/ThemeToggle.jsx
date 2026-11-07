import React from 'react';
import { Sun, Moon } from 'lucide-react';

export default function ThemeToggle({ dark, onToggle }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label="Toggle theme"
      className="relative flex items-center justify-between w-16 h-8 px-1.5 rounded-full cursor-pointer transition-colors duration-300 select-none
        bg-slate-200 dark:bg-[#161616] border border-slate-300 dark:border-[#2a2a2a]
        hover:border-[#fc6203] dark:hover:border-[#fc6203] hover:shadow-[0_0_12px_rgba(252,98,3,0.35)]"
    >
      {/* Light Icon */}
      <span className="flex items-center justify-center w-5 h-5 z-10 transition-colors duration-200 text-slate-600 dark:text-neutral-500">
        <Sun className="w-3.5 h-3.5" />
      </span>

      {/* Dark Icon */}
      <span className="flex items-center justify-center w-5 h-5 z-10 transition-colors duration-200 text-slate-400 dark:text-neutral-400">
        <Moon className="w-3.5 h-3.5" />
      </span>

      {/* Sliding Glowing Pill */}
      <div
        className={`absolute top-1 left-1 w-6 h-6 rounded-full transition-transform duration-300 ease-in-out flex items-center justify-center pointer-events-none
          ${dark
            ? 'translate-x-8 bg-[#fc6203] text-black shadow-[0_0_15px_rgba(252,98,3,0.7)]'
            : 'translate-x-0 bg-white text-slate-800 shadow-sm'
          }`}
      >
        {dark ? (
          <Moon className="w-3.5 h-3.5 text-black stroke-[2.5]" />
        ) : (
          <Sun className="w-3.5 h-3.5 text-amber-500 stroke-[2.5]" />
        )}
      </div>
    </button>
  );
}
