import { useState, useCallback, useEffect } from 'react';
import { Nav } from 'react-bootstrap';
import { ReactFlow, applyNodeChanges, applyEdgeChanges, addEdge, useReactFlow, ReactFlowProvider} from '@xyflow/react';
import type {
  Node,
  Edge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const initialNodes = [
  { id: 'n1', position: { x: 50, y: 50 }, data: { label: 'Node 1' } },
  { id: 'n2', position: { x: 250, y: 150 }, data: { label: 'Node 2' } },
];
const initialEdges = [{ id: 'e1', source: 'n1', target: 'n2' }];

type MenuClass = { class: string };

function FlowArea() {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);

  const { screenToFlowPosition  } = useReactFlow();

  const onNodesChange: OnNodesChange = useCallback(
    (changes) => setNodes((ns) => applyNodeChanges(changes, ns)),
    []
  );

  const onEdgesChange: OnEdgesChange = useCallback(
    (changes) => setEdges((es) => applyEdgeChanges(changes, es)),
    []
  );

  const onConnect: OnConnect = useCallback(
    (params) => setEdges((es) => addEdge(params, es)),
    []
  );

  
  const getId = () => `node_${+new Date()}`;

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const onDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();

    const name = event.dataTransfer.getData("application/reactflow");
    if (!name) return;

    // 计算鼠标在画布上的位置
    const position = screenToFlowPosition({ x: event.clientX, y: event.clientY });

    const newNode = {
      id: getId(),
      position,
      data: { label: name },
    };

    setNodes((nds) => nds.concat(newNode));
  }, [screenToFlowPosition]);

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
  )
}

export default function App() {
  

  const [menuClasses, setMenuClasses] = useState<MenuClass[]>([]);

  useEffect(() => {
    // 模拟调用 API
    fetch(
      '/api/parse_code',
      {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({path: "D:/git/FuncTrade/tests/example_model.py"})
      }      
    )   // 这里换成你的接口地址
      .then((res) => res.json())
      .then((data) => {
          setMenuClasses(data.classes);  // data.classes 已经是 [{class: ...}]
        })
      .catch((err) => console.error('加载菜单失败', err));
  }, []);

  return (
    <div
      className="position-relative vw-100 vh-100"
    >
      {/* ReactFlow 全屏 */}
      <ReactFlowProvider>
        <FlowArea />
      </ReactFlowProvider>

      {/* 左侧浮动导航（Bootstrap 类） */}
      <div className="position-absolute top-0 start-0 h-100 bg-light border-end p-3" style={{ width: 240, zIndex: 10 }}>
        <h5>Menu</h5>
        <Nav className="flex-column">
          {menuClasses.map((item, idx) => (
            <Nav.Link
              key={idx}
              href={`#${item.class}`}
              draggable
              onDragStart={(event) => {
                event.dataTransfer.setData("application/reactflow", item.class);
                event.dataTransfer.effectAllowed = "move";
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
