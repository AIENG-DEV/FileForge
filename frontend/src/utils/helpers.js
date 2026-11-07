export const fmtBytes = (b) => {
  if (!b || b === 0) return '0 B';
  if (b < 1024) return b + ' B';
  if (b < 1048576) return (b / 1024).toFixed(1) + ' KB';
  return (b / 1048576).toFixed(2) + ' MB';
};

export const extOf = (name) => name?.split('.').pop().toLowerCase() || '';

export const getCategory = (filename) => {
  const ext = extOf(filename);
  const map = {
    image: ['jpg','jpeg','png','webp','gif','bmp','tiff','avif','heic','heif','ico','svg','psd','jfif','jpe','exr','hdr','raw'],
    video: ['mp4','mov','avi','mkv','webm','flv','wmv','m4v','3gp','ogv','ts'],
    audio: ['mp3','wav','flac','ogg','aac','m4a','wma','opus','aiff','au'],
    pdf: ['pdf'],
    document: ['doc','docx','ppt','pptx','xls','xlsx','odt','odp','ods','rtf','txt','csv','md','epub','mobi'],
    archive: ['zip','tar','gz','bz2','xz','7z','rar'],
    code: ['json','xml','yaml','yml','html','css','js','ts'],
  };
  for (const [cat, exts] of Object.entries(map)) {
    if (exts.includes(ext)) return cat;
  }
  return 'unknown';
};

export const categoryAccept = (cat) => {
  const accepts = {
    image: '.jpg,.jpeg,.png,.webp,.gif,.bmp,.tiff,.avif,.heic,.heif,.ico,.svg,.psd,.jfif,.jpe,.exr,.hdr,.raw',
    video: '.mp4,.mov,.avi,.mkv,.webm,.flv,.wmv,.m4v,.3gp,.ogv,.ts',
    audio: '.mp3,.wav,.flac,.ogg,.aac,.m4a,.wma,.opus,.aiff,.au',
    pdf: '.pdf',
    document: '.doc,.docx,.ppt,.pptx,.xls,.xlsx,.odt,.odp,.ods,.rtf,.txt,.csv,.md,.epub,.mobi',
    archive: '.zip,.tar,.gz,.bz2,.xz,.7z',
    code: '.json,.xml,.yaml,.yml,.html,.css,.js,.ts',
  };
  return accepts[cat] || '*';
};

export const downloadBlob = (blob, filename) => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
};

export const downloadFromUrl = (url, filename) => {
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click();
};

export const pct = (orig, result) => {
  if (!orig || !result) return null;
  return Math.round((1 - result / orig) * 100);
};
