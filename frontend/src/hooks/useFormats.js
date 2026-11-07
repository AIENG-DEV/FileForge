import { useState, useEffect } from 'react';
import { getFormats } from '../api/client';

export function useFormats() {
  const [formats, setFormats] = useState({});
  const [loading, setLoading] = useState(true);
  const [isWakingUp, setIsWakingUp] = useState(false);

  useEffect(() => {
    // Show cold-start message if request takes longer than 3 seconds
    const timer = setTimeout(() => {
      setIsWakingUp(true);
    }, 3000);

    const fetchFormats = async (retries = 3) => {
      try {
        const res = await getFormats();
        setFormats(res.data);
      } catch {
        if (retries > 0) {
          setTimeout(() => fetchFormats(retries - 1), 3000);
          return;
        }
        setFormats({});
      } finally {
        clearTimeout(timer);
        setLoading(false);
        setIsWakingUp(false);
      }
    };

    fetchFormats();

    return () => clearTimeout(timer);
  }, []);

  return { formats, loading, isWakingUp };
}
