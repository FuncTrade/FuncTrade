import { ReactFlowProvider } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import FlowArea from './components/FlowArea';
import LeftNav from './components/LeftNav';
import { useLoadPipeline } from './hooks/useLoadPipeline';

export default function App() {
  useLoadPipeline()

  return (
    <div className="position-relative vw-100 vh-100">
      <ReactFlowProvider>
        <FlowArea />
      </ReactFlowProvider>

      {/* 左侧导航 */}
      <LeftNav />
    </div>
  );
}
