// hooks/useLoadPipeline.ts
import { useCallback } from 'react';
import { useFlowStore, useClassStore } from '../store';
import dagre from '@dagrejs/dagre';
import type { Node, Edge } from '@xyflow/react'

const W = 180, H = 40;

function layoutLR(nodes: Node[], edges: Edge[]) {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: 'LR', nodesep: 30, ranksep: 60, marginx: 20, marginy: 20 });
  g.setDefaultEdgeLabel(() => ({}));
  nodes.forEach(n => g.setNode(n.id, { width: n.width ?? W, height: n.height ?? H }));
  edges.forEach(e => g.setEdge(e.source, e.target));
  dagre.layout(g);
  return nodes.map(n => {
    const dn = g.node(n.id); if (!dn) return n;
    const x = dn.x - dn.width / 2, y = dn.y - dn.height / 2;
    return { ...n, position: { x, y }, positionAbsolute: { x, y } };
  });
}

export function useLoadPipeline() {
  const { setNodes, setEdges } = useFlowStore();
  const { setClasses } = useClassStore();

  const loadPipeline = useCallback(async (dir_path: string, file_path: string) => {
      const path = dir_path + '\\' + file_path + '.py';

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

        const laid = layoutLR(newNodes, newEdges);
        setNodes(laid);
        setEdges(newEdges);

        setClasses(data.classes.map((c: {class: string}) => c.class));
      })
      .catch((err) => console.error('Failed loading pipeline', err));
    }, [setClasses, setEdges, setNodes])

  return {loadPipeline}
}
