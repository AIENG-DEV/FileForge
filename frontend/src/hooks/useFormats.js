import { useState, useEffect } from 'react';
import { getFormats } from '../api/client';

export function useFormats() {
  const [formats, setFormats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getFormats()
      .then(r => setFormats(r.data))
      .catch(() => setFormats({}))
      .finally(() => setLoading(false));
  }, []);

  return { formats, loading };
}
