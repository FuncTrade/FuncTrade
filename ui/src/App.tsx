import { Nav } from 'react-bootstrap';
import { ReactFlowProvider } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useMenuClass } from './store';
import FlowArea from './FlowArea';
import { loadPipeline } from './hooks/loadPipeline';

export default function App() {
  const path = 'D:/git/FuncTrade/webserver/tests/example_model.py';

  loadPipeline(path)

  const classes = useMenuClass(state => state.classes);

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
          {classes.map((item, idx) => (
            <Nav.Link
              key={idx}
              href={`#${item}`}
              draggable
              onDragStart={(event) => {
                event.dataTransfer.setData('application/reactflow', item);
                event.dataTransfer.effectAllowed = 'move';
              }}
            >
              {item}
            </Nav.Link>
          ))}
        </Nav>
      </div>
    </div>
  );
}
