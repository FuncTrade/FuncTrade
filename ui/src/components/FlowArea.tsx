import React from 'react';
import { Background, ReactFlow, useReactFlow, BackgroundVariant } from '@xyflow/react';
import { useFlowStore } from '../store';

export default function FlowArea() {
  const {
    nodes, edges, onNodesChange, onEdgesChange, onConnect, onConnectStart, setNodes,
  } = useFlowStore(s => s);

  const { screenToFlowPosition } = useReactFlow();

  const getId = () => `node_${+new Date()}`;

  const onDragOver = (event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };

  const onDrop = (event: React.DragEvent) => {
    event.preventDefault();
    const name = event.dataTransfer.getData('application/reactflow');
    if (!name) return;

    const position = screenToFlowPosition({ x: event.clientX, y: event.clientY });
    const newNode = { id: getId(), position, data: { label: name } };

    setNodes([...nodes, newNode]);
  };

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnect={onConnect}
      onConnectStart={onConnectStart}
      onDrop={onDrop}
      onDragOver={onDragOver}
      fitView deleteKeyCode={['Delete','Backspace']}
    >
        <Background
            variant={BackgroundVariant.Dots}
            gap={15}
            size={1}
        />
    </ReactFlow>
  );
}
