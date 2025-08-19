// hooks/useLoadPipeline.ts
import { useEffect } from 'react';
import { useFlowStore, useClassStore, usePathStore } from '../store';

export function useLoadPipeline() {
  const { pipeline_path } = usePathStore();

  const { setNodes, setEdges } = useFlowStore();
  const { setClasses } = useClassStore();

  useEffect(() => {
    const path = pipeline_path;

    if (path == undefined || path.trim() == "") return

    fetch('/api/parse_code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path }),
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
  }, [pipeline_path, setNodes, setEdges, setClasses]);
}
