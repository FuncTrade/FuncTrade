import { Nav, Form } from 'react-bootstrap';
import { useClassStore, usePathStore } from '../store';

export default function LeftNav() {
    const classes = useClassStore(state => state.classes);
    const { class_path, pipeline_path, setClassPath, setPipelinePath } = usePathStore();

    return (
        <div
            className="position-absolute top-0 start-0 h-100 bg-light border-end p-3"
            style={{ width: 240, zIndex: 10 }}
        >
            {/* 路径输入框 */}
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

            <h5>Pipelines</h5>
            <Nav className="flex-column">
            </Nav>
        </div>
    )
}