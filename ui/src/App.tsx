import { useState, useCallback } from 'react';
import { Nav } from 'react-bootstrap';
import { ReactFlow, applyNodeChanges, applyEdgeChanges, addEdge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const initialNodes = [
  { id: 'n1', position: { x: 50, y: 50 }, data: { label: 'Node 1' } },
  { id: 'n2', position: { x: 250, y: 150 }, data: { label: 'Node 2' } },
];
const initialEdges = [{ id: 'e1', source: 'n1', target: 'n2' }];

export default function App() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);

  const onNodesChange = useCallback(
    (changes) => setNodes((ns) => applyNodeChanges(changes, ns)),
    []
  );
  const onEdgesChange = useCallback(
    (changes) => setEdges((es) => applyEdgeChanges(changes, es)),
    []
  );
  const onConnect = useCallback(
    (params) => setEdges((es) => addEdge(params, es)),
    []
  );

  return (
    <div className="position-relative vw-100 vh-100">
      {/* ReactFlow 全屏 */}
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
      />

      {/* 左侧浮动导航（Bootstrap 类） */}
      <div className="position-absolute top-0 start-0 h-100 bg-light border-end p-3" style={{ width: 240, zIndex: 10 }}>
        <h5>Menu</h5>
        <Nav className="flex-column">
          <Nav.Link href="#pipeline">Pipeline</Nav.Link>
          <Nav.Link href="#settings">Settings</Nav.Link>
        </Nav>
      </div>
    </div>
  );
}
