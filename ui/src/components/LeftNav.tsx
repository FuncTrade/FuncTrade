import { Nav, Form } from "react-bootstrap";
import { useClassStore, usePathStore } from "../store";
import { useState } from "react";
import { List } from "react-bootstrap-icons"; // Bootstrap Icons

export default function LeftNav() {
  const { classes, default_classes } = useClassStore();
  const { class_path, pipeline_path, setClassPath, setPipelinePath } =
    usePathStore();

  const [collapsed, setCollapsed] = useState(false);

  return (
    <div
      className="position-absolute top-0 start-0 h-100 bg-light border-end d-flex flex-column"
      style={{
        width: collapsed ? 60 : 240,
        transition: "width 0.3s",
        zIndex: 10,
      }}
    >
      {/* 顶部区域 */}
      <div className="p-2 border-bottom d-flex justify-content-between align-items-center">
        <button
          className="btn btn-sm btn-outline-secondary"
          onClick={() => setCollapsed(!collapsed)}
        >
          <List /> {/* 小图标按钮 */}
        </button>
        {!collapsed && <span className="ms-2 fw-bold">Menu</span>}
      </div>

      {/* 内容区 */}
      {!collapsed && (
        <div className="flex-grow-1 overflow-y-auto p-3">
          <Form.Group className="mb-3">
            <Form.Label>Class Path</Form.Label>
            <Form.Control
              type="text"
              placeholder="输入 class 路径"
              defaultValue={class_path}
              onBlur={(e) => setClassPath(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Pipeline Path</Form.Label>
            <Form.Control
              type="text"
              placeholder="输入 pipeline 路径"
              defaultValue={pipeline_path}
              onBlur={(e) => setPipelinePath(e.target.value)}
            />
          </Form.Group>

          <h5>Default Classes</h5>
          <Nav className="flex-column">
            {default_classes.map((item, idx) => (
              <Nav.Link key={idx} href={`#${item}`} draggable>
                {item}
              </Nav.Link>
            ))}
          </Nav>

          <h5>Classes</h5>
          <Nav className="flex-column">
            {classes.map((item, idx) => (
              <Nav.Link key={idx} href={`#${item}`} draggable>
                {item}
              </Nav.Link>
            ))}
          </Nav>
        </div>
      )}
    </div>
  );
}
