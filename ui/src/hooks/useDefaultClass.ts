// hooks/useLoadPipeline.ts
import { useEffect } from 'react';
import { useClassStore } from '../store';

export function useDefaultClass() {
  const { setDefaultClasses } = useClassStore();

  useEffect(() => {
    fetch('/api/default_classes', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
      .then((res) => res.json())
      .then((data) => {
        setDefaultClasses(data.default_classes.map((c: {class: string}) => c.class));
      })
      .catch((err) => console.error('Failed loading Default Classes', err));
  }, [setDefaultClasses]);
}
