// comments in English
import React, { useEffect, useCallback } from 'react';
import { ReactFlow, useReactFlow } from '@xyflow/react';
import dagre from '@dagrejs/dagre';
import { useFlowStore } from '../store';

const W = 180, H = 40;

function layoutLR(nodes: any[], edges: any[]) {
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

export default function FlowArea() {
  const {
    nodes, edges, onNodesChange, onEdgesChange, onConnect, onConnectStart, setNodes,
    currentPipeline, layoutRanFor, markLayoutRan,
  } = useFlowStore(s => s);

  const { fitView } = useReactFlow();

  const runOnce = useCallback(() => {
    if (!currentPipeline) return;
    if (!nodes?.length) return;
    if (layoutRanFor[currentPipeline]) return;
    const laid = layoutLR(nodes, edges);
    setNodes(laid);
    markLayoutRan(currentPipeline);
    queueMicrotask(() => fitView({ padding: 0.2 }));
  }, [currentPipeline, nodes, edges, layoutRanFor, setNodes, markLayoutRan, fitView]);

  useEffect(() => { runOnce(); }, [runOnce]);

  return (
    <ReactFlow
      nodes={nodes} edges={edges}
      onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
      onConnect={onConnect} onConnectStart={onConnectStart}
      fitView deleteKeyCode={['Delete','Backspace']}
    />
  );
}
