import { Nav } from 'react-bootstrap';
import { useMenuClass } from './store';

export default function LeftNav() {
    const classes = useMenuClass(state => state.classes);

    return (
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
    )
}