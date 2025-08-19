// hooks/useLoadPipeline.ts
import { useEffect } from 'react';
import { useFlowStore, useMenuClass } from '../store';

export function loadPipeline(path: string) {
  const { setNodes, setEdges } = useFlowStore();
  const { setClasses } = useMenuClass();

  useEffect(() => {
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
      .catch((err) => console.error('加载菜单失败', err));
  }, [path, setNodes, setEdges, setClasses]);
}
