import React from 'react';
import { fmtBytes } from '../utils/helpers';
import { ArrowDownRight, ArrowUpRight } from 'lucide-react';

export default function ResultBadge({ originalSize, newSize }) {
  const smaller = newSize <= originalSize;
  const pct = originalSize > 0
    ? Math.abs(((newSize - originalSize) / originalSize) * 100).toFixed(1)
    : '0.0';

  return (
    <span
      className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2 py-0.5 rounded-lg border font-mono
        ${smaller
          ? 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20'
          : 'text-[#fc6203] bg-[#fc6203]/10 border-[#fc6203]/25 shadow-[0_0_8px_rgba(252,98,3,0.3)]'
        }`}
    >
      <span>{fmtBytes(originalSize)}</span>
      {smaller ? (
        <ArrowDownRight className="w-3.5 h-3.5" />
      ) : (
        <ArrowUpRight className="w-3.5 h-3.5" />
      )}
      <span>{fmtBytes(newSize)}</span>
      <span className="opacity-70">({pct}%)</span>
    </span>
  );
}
