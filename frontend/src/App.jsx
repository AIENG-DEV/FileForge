import React, { useState, useCallback, useEffect } from 'react';
import Dropzone from './components/Dropzone';
import FileCard from './components/FileCard';
import SectionNav from './components/SectionNav';
import ThemeToggle from './components/ThemeToggle';
import { useFormats } from './hooks/useFormats';
import { useJob } from './hooks/useJob';
import { uploadFile, downloadBundle } from './api/client';
import { categoryAccept, downloadBlob } from './utils/helpers';
import { Zap, FolderOpen, ShieldCheck, Sparkles, DownloadCloud, Play, Smartphone } from 'lucide-react';

export default function App() {
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem('fileforge_theme');
    return saved !== null ? saved === 'dark' : true;
  });
  const [section, setSection] = useState('image');
  const [files, setFiles] = useState([]);
  const [installPrompt, setInstallPrompt] = useState(null);
  const { formats, loading, isWakingUp } = useFormats();
  const { jobs, startPolling, setJobError, getDownloadUrl: getUrl } = useJob();

  useEffect(() => {
    const handler = (e) => {
      e.preventDefault();
      setInstallPrompt(e);
    };
    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstallClick = async () => {
    if (installPrompt) {
      installPrompt.prompt();
      const choice = await installPrompt.userChoice;
      if (choice.outcome === 'accepted') {
        setInstallPrompt(null);
      }
    } else {
      alert("To install on iOS / Safari: Tap the Share button at the bottom of the screen, then select 'Add to Home Screen'.");
    }
  };

  useEffect(() => {
    localStorage.setItem('fileforge_theme', dark ? 'dark' : 'light');
    if (dark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [dark]);

  const toggleDark = () => {
    setDark(prev => !prev);
  };

  const addFiles = useCallback((newFiles) => {
    setFiles(prev => [
      ...prev,
      ...newFiles.map(f => ({ file: f, id: `${f.name}-${Date.now()}-${Math.random()}` }))
    ]);
  }, []);

  const removeFile = (id) => setFiles(prev => prev.filter(f => f.id !== id));

  const processFile = async (fileObj, operation, options) => {
    const { file, id } = fileObj;
    try {
      setFiles(prev => prev.map(f => f.id === id ? { ...f, jobId: id } : f));
      const { data } = await uploadFile(file, operation, options, () => {});
      startPolling(data.job_id, data.original_size);
      setFiles(prev => prev.map(f => f.id === id ? { ...f, jobId: data.job_id } : f));
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Upload failed';
      setJobError(id, msg);
    }
  };

  const completedJobIds = files
    .map(f => f.jobId)
    .filter(jid => jid && jobs[jid]?.status === 'done');

  const uncompletedFiles = files.filter(f => !f.jobId || jobs[f.jobId]?.status === 'error');

  const handleProcessAll = () => {
    uncompletedFiles.forEach(f => {
      processFile(f, 'compress', { quality: 75 });
    });
  };

  const handleDownloadAll = async () => {
    if (completedJobIds.length === 0) return;
    try {
      const res = await downloadBundle(completedJobIds);
      downloadBlob(res.data, 'fileforge_bundle.zip');
    } catch (err) {
      console.error('Bundle download failed', err);
    }
  };

  const inputCount = (formats[section]?.input || []).length;
  const outputCount = (formats[section]?.output || []).length;

  return (
    <div className="min-h-screen bg-white dark:bg-black text-slate-900 dark:text-neutral-100 transition-colors duration-200">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-50 bg-white/95 dark:bg-black/95 backdrop-blur-md border-b border-slate-200 dark:border-[#1a1a1a] px-6 py-3.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo & Branding */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-black dark:bg-[#121212] flex items-center justify-center border border-slate-300 dark:border-[#262626] shadow-[0_0_15px_rgba(252,98,3,0.4)]">
              <Zap className="w-5 h-5 text-[#fc6203]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-extrabold tracking-tight font-heading">
                  FILE<span className="text-[#fc6203] drop-shadow-[0_0_10px_rgba(252,98,3,0.6)]">FORGE</span>
                </span>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider bg-slate-100 dark:bg-[#161616] text-[#fc6203] border border-slate-200 dark:border-[#262626]">
                  PRO
                </span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-neutral-400 font-medium -mt-0.5">
                Compress · Convert · Upscale · Universal Engine
              </p>
            </div>
          </div>

          {/* Right Header: Security Pill & Theme Toggle */}
          <div className="flex items-center gap-2.5 sm:gap-4">
            <button
              type="button"
              onClick={handleInstallClick}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-[#fc6203]/10 text-[#fc6203] border border-[#fc6203]/30 hover:bg-[#fc6203] hover:text-black transition-all cursor-pointer shadow-[0_0_10px_rgba(252,98,3,0.2)]"
              title="Install app to your device"
            >
              <Smartphone className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Install App</span>
              <span className="sm:hidden">Install</span>
            </button>

            <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-[#07160e] border border-emerald-200 dark:border-[#0e301d]">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Magic Bytes Protected</span>
            </div>

            <ThemeToggle dark={dark} onToggle={toggleDark} />
          </div>
        </div>
      </header>

      {/* Cloud Cold Start Indicator */}
      {isWakingUp && (
        <div className="bg-[#fc6203]/10 border-b border-[#fc6203]/25 px-4 py-2 text-center text-xs text-[#fc6203] font-medium flex items-center justify-center gap-2">
          <Zap className="w-3.5 h-3.5 animate-bounce" />
          <span>Connecting to cloud engine... (Free cloud instances may take ~30s to wake up on first load)</span>
        </div>
      )}

      {/* Main Container */}
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row gap-4 sm:gap-6 p-4 sm:p-6">
        {/* Left Sidebar Navigator */}
        <aside className="w-full md:w-56 flex-shrink-0">
          <div className="bg-slate-50 dark:bg-[#0c0c0c] rounded-2xl border border-slate-200 dark:border-[#1a1a1a] p-1.5 sticky top-16 md:top-20 z-40 shadow-sm">
            <SectionNav active={section} onSelect={(s) => { setSection(s); setFiles([]); }} />
          </div>
        </aside>

        {/* Content Workspace */}
        <main className="flex-1 min-w-0 space-y-6">
          {/* Section Heading Banner */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-200 dark:border-[#1a1a1a]">
            <div>
              <h2 className="text-2xl font-bold tracking-tight capitalize text-slate-900 dark:text-white flex items-center gap-2">
                <span>{section} Studio</span>
                <Sparkles className="w-4 h-4 text-[#fc6203]" />
              </h2>
              <p className="text-xs text-slate-500 dark:text-neutral-400 mt-0.5">
                Optimize file size, upscale quality, or switch formats seamlessly.
              </p>
            </div>

            <div className="flex items-center gap-2 text-xs">
              <span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#121212] border border-slate-200 dark:border-[#222222] font-mono text-slate-600 dark:text-neutral-300">
                {loading ? '...' : `${inputCount} Inputs`}
              </span>
              <span className="text-slate-400">→</span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#121212] border border-slate-200 dark:border-[#222222] font-mono text-[#fc6203] font-semibold">
                {loading ? '...' : `${outputCount} Outputs`}
              </span>
            </div>
          </div>

          {/* Upload Dropzone */}
          <Dropzone
            onFiles={addFiles}
            accept={categoryAccept(section)}
            category={section}
          />

          {/* Active File Cards Grid */}
          {files.length > 0 && (
            <div className="space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-semibold px-1">
                <span className="text-slate-600 dark:text-neutral-400">Active Queue ({files.length})</span>

                <div className="flex items-center gap-2">
                  {uncompletedFiles.length > 0 && (
                    <button
                      type="button"
                      onClick={handleProcessAll}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#fc6203] hover:bg-[#e05400] text-white dark:text-black font-semibold transition-all shadow-[0_0_12px_rgba(252,98,3,0.35)] cursor-pointer"
                    >
                      <Play className="w-3 h-3 fill-current" />
                      <span>Process All ({uncompletedFiles.length})</span>
                    </button>
                  )}

                  {completedJobIds.length > 1 && (
                    <button
                      type="button"
                      onClick={handleDownloadAll}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold transition-all shadow-sm cursor-pointer"
                    >
                      <DownloadCloud className="w-3.5 h-3.5" />
                      <span>Download All ZIP ({completedJobIds.length})</span>
                    </button>
                  )}

                  <button
                    type="button"
                    onClick={() => setFiles([])}
                    className="text-red-500 hover:text-red-600 dark:hover:text-red-400 cursor-pointer ml-1"
                  >
                    Clear all
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {files.map(fileObj => {
                  const jobId = fileObj.jobId;
                  const jobInfo = jobId ? { ...jobs[jobId], downloadUrl: getUrl(jobId) } : null;
                  return (
                    <FileCard
                      key={fileObj.id}
                      file={fileObj.file}
                      formats={formats}
                      jobInfo={jobInfo}
                      onProcess={(f, op, opts) => processFile(fileObj, op, opts)}
                      onRemove={() => removeFile(fileObj.id)}
                    />
                  );
                })}
              </div>
            </div>
          )}

          {/* Empty State */}
          {files.length === 0 && (
            <div className="text-center py-16 border border-dashed border-slate-200 dark:border-[#1a1a1a] rounded-3xl bg-slate-50/50 dark:bg-[#070707]">
              <div className="w-14 h-14 mx-auto rounded-2xl bg-slate-100 dark:bg-[#121212] text-slate-400 dark:text-neutral-500 border border-slate-200 dark:border-[#202020] flex items-center justify-center mb-3">
                <FolderOpen className="w-7 h-7 text-[#fc6203]" />
              </div>
              <p className="text-sm font-semibold text-slate-700 dark:text-neutral-300">
                Queue is empty
              </p>
              <p className="text-xs text-slate-400 dark:text-neutral-500 mt-1 max-w-sm mx-auto">
                Select or drop files into the zone above to begin downscaling, upscaling, or converting.
              </p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
