import { useState, useEffect, useRef } from 'react';
import { getJob, getDownloadUrl } from '../api/client';

export function useJob() {
  const [jobs, setJobs] = useState({});
  const timers = useRef({});

  const startPolling = (jobId, originalSize) => {
    setJobs(prev => ({ ...prev, [jobId]: { status: 'queued', progress: 0, originalSize } }));
    
    const poll = async () => {
      try {
        const { data } = await getJob(jobId);
        setJobs(prev => ({ ...prev, [jobId]: { ...data, originalSize } }));
        if (data.status === 'done' || data.status === 'error') {
          clearInterval(timers.current[jobId]);
          delete timers.current[jobId];
        }
      } catch {
        clearInterval(timers.current[jobId]);
        setJobs(prev => ({ ...prev, [jobId]: { status: 'error', error: 'Network error' } }));
      }
    };

    timers.current[jobId] = setInterval(poll, 800);
    poll();
  };

  const setJobError = (jobId, errorMsg) => {
    setJobs(prev => ({
      ...prev,
      [jobId]: { status: 'error', progress: 0, error: errorMsg }
    }));
  };

  useEffect(() => () => Object.values(timers.current).forEach(clearInterval), []);

  return { jobs, startPolling, setJobError, getDownloadUrl };
}
