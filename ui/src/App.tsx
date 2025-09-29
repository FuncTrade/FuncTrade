import { ReactFlowProvider } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import FlowArea from './components/FlowArea';
import LeftNav from './components/LeftNav';
import ClassListNav from './components/ClassListNav';
import { useLoadPipeline } from './hooks/useLoadPipeline';
import { useDefaultClass } from './hooks/useDefaultClass';
import { usePipelineDir } from './hooks/usePipelineDir';

export default function App() {
  useLoadPipeline()
  useDefaultClass()
  usePipelineDir()

  return (
    <div className="position-relative vw-100 vh-100">
      <ReactFlowProvider>
        <FlowArea />
      </ReactFlowProvider>

      <LeftNav />
      <ClassListNav />
    </div>
  );
}
