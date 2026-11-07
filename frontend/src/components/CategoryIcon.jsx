import React from 'react';
import {
  Image as FileImage,
  Video as FileVideo,
  Music as FileAudio,
  FileText,
  FileSpreadsheet,
  Archive,
  Code2,
  File
} from 'lucide-react';

export default function CategoryIcon({ category, className = 'w-5 h-5' }) {
  switch (category) {
    case 'image':
      return <FileImage className={className} />;
    case 'video':
      return <FileVideo className={className} />;
    case 'audio':
      return <FileAudio className={className} />;
    case 'pdf':
      return <FileText className={className} />;
    case 'document':
      return <FileSpreadsheet className={className} />;
    case 'archive':
      return <Archive className={className} />;
    case 'code':
      return <Code2 className={className} />;
    default:
      return <File className={className} />;
  }
}
