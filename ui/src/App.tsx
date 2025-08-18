import { useEffect, useState } from 'react';
import { Nav } from 'react-bootstrap';
import {
  ReactFlow,
  ReactFlowProvider,
  useReactFlow,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useFlowStore } from './store';

type MenuClass = { class: string };

function FlowArea() {
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

export default function App() {
  const { setNodes, setEdges } = useFlowStore();
  const [menuClasses, setMenuClasses] = useState<MenuClass[]>([]);

  useEffect(() => {
    fetch('/api/parse_code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: 'D:/git/FuncTrade/tests/example_model.py' }),
    })
      .then((res) => res.json())
      .then((data) => {
        setMenuClasses(data.classes);

        const newNodes = data.classes.map((item: { class: string }, idx: number) => ({
          id: item.class,
          data: { label: item.class },
          position: { x: 100, y: idx * 100 + 50 },
        }));

        const newEdges = data.edges.map((e: [string, string]) => ({
          id: `${e[0]}-${e[1]}`,
          source: e[0],
          target: e[1],
          markerEnd: {
            type: "arrowclosed",
            width: 20,
            height: 20,
            color: "#222",
          }
        }));

        setNodes(newNodes);
        setEdges(newEdges);
      })
      .catch((err) => console.error('加载菜单失败', err));
  }, [setNodes, setEdges]);

  return (
    <div className="position-relative vw-100 vh-100">
      <ReactFlowProvider>
        <FlowArea />
      </ReactFlowProvider>

      {/* 左侧导航 */}
      <div
        className="position-absolute top-0 start-0 h-100 bg-light border-end p-3"
        style={{ width: 240, zIndex: 10 }}
      >
        <h5>Menu</h5>
        <Nav className="flex-column">
          {menuClasses.map((item, idx) => (
            <Nav.Link
              key={idx}
              href={`#${item.class}`}
              draggable
              onDragStart={(event) => {
                event.dataTransfer.setData('application/reactflow', item.class);
                event.dataTransfer.effectAllowed = 'move';
              }}
            >
              {item.class}
            </Nav.Link>
          ))}
        </Nav>
      </div>
    </div>
  );
}
