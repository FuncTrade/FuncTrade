// hooks/useLoadPipeline.ts
import { useEffect } from 'react';
import { useFlowStore, useClassStore, usePathStore } from '../store';

export function usePipelineDir() {
  const { pipeline_dir, setPipelinePaths } = usePathStore();
  const { setNodes, setEdges } = useFlowStore();
  const { setClasses } = useClassStore();

  useEffect(() => {
    const dir_path = pipeline_dir;

    if (dir_path == undefined || dir_path.trim() == "") return

    fetch('/api/list_pipeline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: dir_path }),
    })
      .then((res) => res.json())
      .then((data: {pipelines: { pipeline: string}[]}) => {
        const names = data.pipelines.map((item) => item.pipeline);
        setPipelinePaths(names);
      })
      .catch((err) => console.error('Failed loading pipeline', err));
  }, [pipeline_dir, setNodes, setEdges, setClasses]);
}
