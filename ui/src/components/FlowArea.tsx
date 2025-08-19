import {
  ReactFlow,
  useReactFlow,
} from '@xyflow/react';
import { useFlowStore } from '../store';


export default function FlowArea() {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect, setNodes } = useFlowStore();
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
      fitView
      onDrop={onDrop}
      onDragOver={onDragOver}
    />
  );
}