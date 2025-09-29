import { Nav, Form } from "react-bootstrap";
import { useClassStore, usePathStore } from "../store";

export default function ClassListNav() {
  const { classes, default_classes } = useClassStore();
  const { class_path, setClassPath } =
    usePathStore();

  return (
    <div
      className="position-absolute top-0 end-0 h-100 bg-light border-end d-flex flex-column"
      style={{width: 240, zIndex: 10}}
    >
      {/* top area */}
      <div className="p-2 border-bottom d-flex justify-content-between align-items-center">
        <span className="ms-2 fw-bold">Classes</span>
      </div>

      {/* contents */}
        <div className="flex-grow-1 overflow-y-auto p-3">
          <Form.Group className="mb-3">
            <Form.Label>Class Path</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter the path of classes"
              defaultValue={class_path}
              onBlur={(e) => setClassPath(e.target.value)}
            />
          </Form.Group>

          <h5>Default Classes</h5>
          <Nav className="flex-column">
            {default_classes.map((item, idx) => (
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

          <h5>Classes</h5>
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
