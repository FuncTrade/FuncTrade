import { Form, Nav } from "react-bootstrap";
import { usePathStore } from "../store";
import { useState } from "react";
import { List } from "react-bootstrap-icons"; // Bootstrap Icons
import { useLoadPipeline } from "../hooks/useLoadPipeline";

export default function LeftNav() {
  const { pipeline_dir, setPipelineDir, pipeline_paths } =
    usePathStore();

  const { loadPipeline } = useLoadPipeline();
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
      {/* top area */}
      <div className="p-2 border-bottom d-flex justify-content-between align-items-center">
        <button
          className="btn btn-sm btn-outline-secondary"
          onClick={() => setCollapsed(!collapsed)}
        >
          <List /> {/* icon button */}
        </button>
        {!collapsed && <span className="ms-2 fw-bold">Pipeline</span>}
      </div>

      {/* contents */}
      {!collapsed && (
        <div className="flex-grow-1 overflow-y-auto p-3">
          <Form.Group className="mb-3">
            <Form.Label>Pipeline Path</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter the path of pipelines"
              defaultValue={pipeline_dir}
              onBlur={(e) => setPipelineDir(e.target.value)}
            />
          </Form.Group>

          <h5>Pipeline Files</h5>
          <Nav className="flex-column">
            {pipeline_paths.map((name) => (
                <Nav.Link
                    key={name}
                    href={`#${name}`}
                    onClick={() => loadPipeline(pipeline_dir, name)}
                    >
                    {name}
                </Nav.Link>
            ))}
          </Nav>
        </div>
      )}
    </div>
  );
}
