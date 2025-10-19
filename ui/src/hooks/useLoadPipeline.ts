// hooks/useLoadPipeline.ts
import { useCallback } from 'react';
import { useFlowStore, useClassStore } from '../store';

export function useLoadPipeline() {
  const { setNodes, setEdges, setCurrentPipeline } = useFlowStore();
  const { setClasses } = useClassStore();

  const loadPipeline = useCallback(async (dir_path: string, file_path: string) => {
      const path = dir_path + '\\' + file_path + '.py';
      setCurrentPipeline(file_path);

      if (path == undefined || path.trim() == "") return

      fetch('/api/parse_code_new', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: path }),
    })
      .then((res) => res.json())
      .then((data) => {
        const newNodes = data.classes.map((item: { class: string }, idx: number) => ({
          id: item.class,
          data: { label: item.class },
          position: { x: 100, y: idx * 100 + 50 },
        }));
        const newEdges = data.edges.map((e: [string, string]) => ({
          id: `${e[0]}-${e[1]}`,
          source: e[0],
          target: e[1],
          markerEnd: { type: 'arrowclosed', width: 20, height: 20, color: '#222' },
        }));
        setNodes(newNodes);
        setEdges(newEdges);

        setClasses(data.classes.map((c: {class: string}) => c.class));
      })
      .catch((err) => console.error('Failed loading pipeline', err));
    }, [])

  return {loadPipeline}
}
