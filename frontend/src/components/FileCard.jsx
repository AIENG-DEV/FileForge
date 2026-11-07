import React, { useState, useEffect } from 'react';
import { fmtBytes, getCategory, pct } from '../utils/helpers';
import CategoryIcon from './CategoryIcon';
import {
  X,
  Download,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  ArrowDownRight,
  ArrowUpRight
} from 'lucide-react';

const TABS = ['Compress', 'Convert', 'Upscale'];

export default function FileCard({ file, formats, jobInfo, onProcess, onRemove }) {
  const [tab, setTab] = useState('Compress');
  const [quality, setQuality] = useState(75);
  const [maxWidth, setMaxWidth] = useState('');
  const [bitrate, setBitrate] = useState('128k');
  const [crf, setCrf] = useState(28);
  const [targetFmt, setTargetFmt] = useState('');
  const [scale, setScale] = useState(2.0);
  const cat = getCategory(file.name);
  const catFormats = formats[cat] || {};
  const outputFormats = catFormats.output || [];

  const [previewUrl] = useState(() => {
    if (file && file.type?.startsWith('image/')) {
      try {
        return URL.createObjectURL(file);
      } catch {
        return null;
      }
    }
    return null;
  });

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleProcess = () => {
    if (tab === 'Compress') {
      onProcess(file, 'compress', {
        quality,
        max_width: maxWidth || null,
        bitrate,
        crf
      });
    } else if (tab === 'Convert') {
      onProcess(file, 'convert', { target_format: targetFmt || outputFormats[0] });
    } else if (tab === 'Upscale') {
      onProcess(file, 'upscale', { scale });
    }
  };

  const status = jobInfo?.status;
  const progress = jobInfo?.progress || 0;
  const saving = jobInfo?.status === 'done' ? pct(jobInfo.original_size || file.size, jobInfo.result_size) : null;

  return (
    <div className="bg-white dark:bg-[#0c0c0c] rounded-2xl border border-slate-200 dark:border-[#1f1f1f] p-4 flex flex-col gap-3.5 transition-all duration-200 hover:border-slate-300 dark:hover:border-[#2f2f2f] hover:shadow-lg dark:hover:shadow-[0_0_20px_rgba(252,98,3,0.1)]">
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 overflow-hidden
            bg-slate-100 dark:bg-[#161616] text-[#fc6203] border border-slate-200 dark:border-[#262626]">
            {previewUrl ? (
              <img src={previewUrl} alt={file.name} className="w-full h-full object-cover" />
            ) : (
              <CategoryIcon category={cat} className="w-5 h-5" />
            )}
          </div>
          <div className="min-w-0">
            <p className="font-semibold text-sm truncate text-slate-900 dark:text-neutral-100" title={file.name}>
              {file.name}
            </p>
            <p className="text-xs text-slate-500 dark:text-neutral-400">
              {fmtBytes(file.size)} <span className="opacity-40">|</span> <span className="capitalize">{cat}</span>
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={onRemove}
          className="text-slate-400 hover:text-red-500 dark:text-neutral-500 dark:hover:text-red-400 transition-colors p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-[#1a1a1a]"
          title="Remove file"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Status Progress */}
      {status && (
        <div className="space-y-1.5 p-2.5 rounded-xl bg-slate-50 dark:bg-[#141414] border border-slate-200 dark:border-[#222222]">
          <div className="flex justify-between text-xs font-medium text-slate-600 dark:text-neutral-400">
            <span className="capitalize flex items-center gap-1.5">
              {status === 'done' ? (
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
              ) : status === 'error' ? (
                <AlertCircle className="w-3.5 h-3.5 text-red-500" />
              ) : (
                <span className="w-2 h-2 rounded-full bg-[#fc6203] animate-ping inline-block" />
              )}
              {status}
            </span>
            <span>{progress}%</span>
          </div>

          <div className="h-1.5 bg-slate-200 dark:bg-[#202020] rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-300 ${
                status === 'error'
                  ? 'bg-red-500'
                  : status === 'done'
                  ? 'bg-emerald-500'
                  : 'bg-[#fc6203] shadow-[0_0_10px_rgba(252,98,3,0.8)]'
              }`}
              style={{ width: `${progress}%` }}
            />
          </div>

          {status === 'done' && saving !== null && (
            <div className={`flex items-center gap-1 text-xs font-semibold ${saving > 0 ? 'text-emerald-500' : 'text-[#fc6203]'}`}>
              {saving > 0 ? (
                <ArrowDownRight className="w-3.5 h-3.5" />
              ) : (
                <ArrowUpRight className="w-3.5 h-3.5" />
              )}
              <span>{saving > 0 ? `${saving}% smaller` : `${Math.abs(saving)}% larger`}</span>
              <span className="text-slate-400 dark:text-neutral-500 ml-auto font-mono text-[11px]">
                {fmtBytes(jobInfo.result_size)}
              </span>
            </div>
          )}

          {status === 'error' && (
            <p className="text-xs text-red-400 leading-tight">{jobInfo.error}</p>
          )}
        </div>
      )}

      {/* Controls */}
      {!status || status === 'error' ? (
        <>
          {/* Mode Tabs */}
          <div className="grid grid-cols-3 gap-1 p-1 bg-slate-100 dark:bg-[#141414] rounded-xl border border-slate-200 dark:border-[#222222] text-xs">
            {TABS.map(t => (
              <button
                key={t}
                type="button"
                onClick={() => setTab(t)}
                className={`py-1.5 rounded-lg font-medium transition-all duration-200 cursor-pointer text-center
                  ${tab === t
                    ? 'bg-[#fc6203] text-white dark:text-black dark:font-semibold shadow-[0_0_12px_rgba(252,98,3,0.45)]'
                    : 'text-slate-600 dark:text-neutral-400 hover:text-slate-900 dark:hover:text-white'
                  }`}
              >
                {t}
              </button>
            ))}
          </div>

          {tab === 'Compress' && (
            <div className="space-y-2.5">
              {cat === 'audio' ? (
                <div>
                  <label className="text-[11px] font-medium text-slate-500 dark:text-neutral-400">Target Bitrate</label>
                  <select
                    value={bitrate}
                    onChange={e => setBitrate(e.target.value)}
                    className="w-full bg-slate-50 dark:bg-[#141414] border border-slate-200 dark:border-[#262626] dark:text-white rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:border-[#fc6203]"
                  >
                    <option value="64k">64 kbps (Max Compression)</option>
                    <option value="96k">96 kbps (Voice / Podcast)</option>
                    <option value="128k">128 kbps (Standard Quality)</option>
                    <option value="192k">192 kbps (High Quality)</option>
                    <option value="256k">256 kbps (Studio Quality)</option>
                    <option value="320k">320 kbps (Maximum Fidelity)</option>
                  </select>
                </div>
              ) : cat === 'video' ? (
                <div>
                  <div className="flex justify-between text-xs text-slate-600 dark:text-neutral-400 mb-1 font-medium">
                    <span>Compression Level (CRF)</span>
                    <span className="text-[#fc6203] font-mono font-bold">{crf}</span>
                  </div>
                  <select
                    value={crf}
                    onChange={e => setCrf(+e.target.value)}
                    className="w-full bg-slate-50 dark:bg-[#141414] border border-slate-200 dark:border-[#262626] dark:text-white rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:border-[#fc6203]"
                  >
                    <option value={23}>CRF 23 — High Quality (Minor compression)</option>
                    <option value={28}>CRF 28 — Balanced (Recommended for Web)</option>
                    <option value={32}>CRF 32 — Smaller File Size</option>
                    <option value={36}>CRF 36 — Maximum Compression</option>
                  </select>
                </div>
              ) : (
                <>
                  <div>
                    <div className="flex justify-between text-xs text-slate-600 dark:text-neutral-400 mb-1.5 font-medium">
                      <span>Compression Quality</span>
                      <span className="text-[#fc6203] font-mono font-bold">{quality}%</span>
                    </div>
                    <input
                      type="range"
                      min="1"
                      max="100"
                      value={quality}
                      onChange={e => setQuality(+e.target.value)}
                      className="w-full accent-[#fc6203] cursor-pointer"
                    />
                  </div>
                  {cat === 'image' && (
                    <input
                      type="number"
                      placeholder="Max width px (optional resize)"
                      value={maxWidth}
                      onChange={e => setMaxWidth(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-[#141414] border border-slate-200 dark:border-[#262626] dark:text-white rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:border-[#fc6203] focus:ring-1 focus:ring-[#fc6203]"
                    />
                  )}
                </>
              )}
            </div>
          )}

          {tab === 'Convert' && (
            <div className="space-y-1">
              <label className="text-[11px] font-medium text-slate-500 dark:text-neutral-400">Target Format</label>
              <select
                value={targetFmt}
                onChange={e => setTargetFmt(e.target.value)}
                className="w-full bg-slate-50 dark:bg-[#141414] border border-slate-200 dark:border-[#262626] dark:text-white rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-[#fc6203] focus:ring-1 focus:ring-[#fc6203]"
              >
                {outputFormats.length === 0 ? (
                  <option>No formats available</option>
                ) : (
                  outputFormats.map(f => (
                    <option key={f} value={f}>
                      .{f.toUpperCase()}
                    </option>
                  ))
                )}
              </select>
            </div>
          )}

          {tab === 'Upscale' && (
            <div className="space-y-1">
              <label className="text-[11px] font-medium text-slate-500 dark:text-neutral-400">Scale Factor</label>
              <select
                value={scale}
                onChange={e => setScale(+e.target.value)}
                className="w-full bg-slate-50 dark:bg-[#141414] border border-slate-200 dark:border-[#262626] dark:text-white rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-[#fc6203] focus:ring-1 focus:ring-[#fc6203]"
              >
                {[1.5, 2, 3, 4].map(s => (
                  <option key={s} value={s}>
                    {s}x Resolution Upscale
                  </option>
                ))}
              </select>
            </div>
          )}

          <button
            type="button"
            onClick={handleProcess}
            disabled={tab === 'Convert' && outputFormats.length === 0}
            className="w-full bg-[#fc6203] hover:bg-[#e05400] disabled:bg-slate-200 dark:disabled:bg-[#1f1f1f] disabled:text-slate-400 dark:disabled:text-neutral-600 text-white dark:text-black font-semibold text-xs py-2.5 rounded-xl transition-all duration-200 cursor-pointer shadow-[0_0_15px_rgba(252,98,3,0.35)] hover:shadow-[0_0_22px_rgba(252,98,3,0.6)] flex items-center justify-center gap-1.5"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Process File</span>
          </button>
        </>
      ) : status === 'done' ? (
        <a
          href={jobInfo.downloadUrl}
          download={jobInfo.result_filename}
          className="w-full bg-[#fc6203] hover:bg-[#e05400] text-white dark:text-black font-semibold text-xs py-2.5 rounded-xl transition-all duration-200 text-center flex items-center justify-center gap-2 shadow-[0_0_18px_rgba(252,98,3,0.5)] hover:shadow-[0_0_25px_rgba(252,98,3,0.7)]"
        >
          <Download className="w-4 h-4" />
          <span>Download Processed File</span>
        </a>
      ) : null}
    </div>
  );
}
