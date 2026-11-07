import React, { useRef, useState } from 'react';

export default function LiquidSlider({
  value,
  onChange,
  min = 1,
  max = 100,
  label = 'Compression Quality',
  unit = '%',
  presets = [
    { label: 'Max 25%', value: 25 },
    { label: 'Eco 50%', value: 50 },
    { label: 'Balanced 75%', value: 75 },
    { label: 'High 90%', value: 90 },
  ]
}) {
  const [isHovered, setIsHovered] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const trackRef = useRef(null);

  const pct = Math.max(0, Math.min(100, ((value - min) / (max - min)) * 100));

  return (
    <div className="space-y-2 select-none">
      {/* Top Header with live badge */}
      <div className="flex items-center justify-between text-xs font-medium">
        <span className="text-slate-600 dark:text-neutral-400">{label}</span>
        <div
          className={`px-2 py-0.5 rounded-full text-[11px] font-mono font-bold transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]
            ${isDragging || isHovered
              ? 'bg-[#fc6203] text-black shadow-[0_0_15px_rgba(252,98,3,0.8)] scale-110 rotate-1'
              : 'bg-slate-100 dark:bg-white/10 text-[#fc6203] border border-slate-200 dark:border-white/10'
            }`}
        >
          {value}{unit}
        </div>
      </div>

      {/* Modern Liquid Track & Thumb */}
      <div
        className="relative py-2 flex items-center cursor-pointer group"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => { setIsHovered(false); setIsDragging(false); }}
      >
        {/* Track Background */}
        <div
          ref={trackRef}
          className="relative w-full h-2 rounded-full bg-slate-200 dark:bg-white/10 overflow-hidden backdrop-blur-md"
        >
          {/* Active Liquid Fill (Solid Neon Orange with glow, ZERO gradients) */}
          <div
            className="h-full bg-[#fc6203] rounded-full transition-[width] duration-75 ease-out shadow-[0_0_14px_rgba(252,98,3,0.8)]"
            style={{ width: `${pct}%` }}
          />
        </div>

        {/* Liquid Thumb (Controlled via standard range input overlay for 100% native accessibility) */}
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onMouseDown={() => setIsDragging(true)}
          onMouseUp={() => setIsDragging(false)}
          onTouchStart={() => setIsDragging(true)}
          onTouchEnd={() => setIsDragging(false)}
          onChange={e => onChange(+e.target.value)}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-20"
          aria-label={label}
        />

        {/* Visual Glowing Thumb with Spring Wobble */}
        <div
          className={`absolute pointer-events-none top-1/2 -translate-y-1/2 w-4 h-4 sm:w-5 sm:h-5 rounded-full bg-[#fc6203] border-2 border-white dark:border-black shadow-[0_0_16px_rgba(252,98,3,0.9)] transition-transform duration-200 ease-[cubic-bezier(0.34,1.56,0.64,1)]
            ${isDragging ? 'scale-125 shadow-[0_0_24px_rgba(252,98,3,1)]' : isHovered ? 'scale-120' : 'scale-100'}
          `}
          style={{ left: `calc(${pct}% - ${pct * 0.16}px)` }}
        />
      </div>

      {/* ReactBits Tactile Preset Pills */}
      {presets && presets.length > 0 && (
        <div className="grid grid-cols-4 gap-1.5 pt-0.5">
          {presets.map(p => {
            const isSelected = value === p.value;
            return (
              <button
                key={p.value}
                type="button"
                onClick={() => onChange(p.value)}
                className={`py-1 rounded-lg text-[10px] font-mono font-medium transition-all duration-200 cursor-pointer text-center select-none hover-wobble active:scale-95
                  ${isSelected
                    ? 'bg-[#fc6203] text-black font-bold shadow-[0_0_12px_rgba(252,98,3,0.5)] scale-[1.03]'
                    : 'bg-slate-100 dark:bg-white/5 text-slate-500 dark:text-neutral-400 hover:text-slate-800 dark:hover:text-white border border-slate-200/60 dark:border-white/5'
                  }`}
              >
                {p.label}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
