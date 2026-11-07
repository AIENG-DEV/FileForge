import axios from 'axios';

const BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

const api = axios.create({ baseURL: BASE });

// New job-based flow
export const uploadFile = (file, operation, options, onProgress) => {
  const fd = new FormData();
  fd.append('file', file);
  fd.append('operation', operation);
  Object.entries(options).forEach(([k, v]) => v != null && fd.append(k, String(v)));
  return api.post('/upload', fd, {
    onUploadProgress: e => onProgress?.(Math.round(e.loaded * 100 / e.total))
  });
};

export const getJob = (jobId) => api.get(`/job/${jobId}`);
export const getDownloadUrl = (jobId) => `${BASE}/download/${jobId}`;
export const getFormats = () => api.get('/formats');
export const downloadBundle = (jobIds) =>
  api.post('/download-bundle', { job_ids: jobIds }, { responseType: 'blob' });

// Legacy sync endpoints
export const compressFile = (file, options, onProgress) => {
  const fd = new FormData();
  fd.append('file', file);
  Object.entries(options).forEach(([k, v]) => v != null && fd.append(k, String(v)));
  return api.post('/compress', fd, { responseType: 'blob', onUploadProgress: e => onProgress?.(Math.round(e.loaded * 100 / e.total)) });
};

export const convertFile = (file, target_format, onProgress) => {
  const fd = new FormData();
  fd.append('file', file);
  fd.append('target_format', target_format);
  return api.post('/convert', fd, { responseType: 'blob', onUploadProgress: e => onProgress?.(Math.round(e.loaded * 100 / e.total)) });
};

export const upscaleFile = (file, scale, onProgress) => {
  const fd = new FormData();
  fd.append('file', file);
  fd.append('scale', String(scale));
  return api.post('/upscale', fd, { responseType: 'blob', onUploadProgress: e => onProgress?.(Math.round(e.loaded * 100 / e.total)) });
};
