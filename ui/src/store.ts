// store.ts
import { create } from 'zustand';
import { persist, createJSONStorage  } from "zustand/middleware";
import { applyNodeChanges, applyEdgeChanges, addEdge, MarkerType} from '@xyflow/react';
import type {
    Node, Edge, OnNodesChange, OnEdgesChange, OnConnect, Connection, OnConnectStartParams
} from '@xyflow/react'

type StartType = 'source' | 'target' | null;

type FlowStore = {
  nodes: Node[];
  edges: Edge[];
  setNodes: (nodes: Node[]) => void;
  setEdges: (edges: Edge[]) => void;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  connectStartType: StartType;
  onConnectStart: (e: MouseEvent | TouchEvent, p: OnConnectStartParams) => void;
  onConnect: (params: Connection) => void;
};

const withArrow = (edges: Edge[]): Edge[] => 
    edges.map((e) => ({
        ...e,
        markerEnd: e.markerEnd ?? { type: MarkerType.ArrowClosed}
    }));

export const useFlowStore = create<FlowStore>((set, get) => ({
  nodes: [],
  edges: [],
  setNodes: (nodes) => set({ nodes }),
  setEdges: (edges) => set({ edges: withArrow(edges) }),
  onNodesChange: (changes) => {
    set({ nodes: applyNodeChanges(changes, get().nodes) });
  },
  onEdgesChange: (changes) => {
    const next = applyEdgeChanges(changes, get().edges);
    set({ edges: withArrow(next)});
  },

  connectStartType: null,

  onConnectStart: (_e, { handleType }) => {
    set({ connectStartType: handleType ?? null });
  },
  onConnect: (params) => {
    const startedAt = get().connectStartType;
    const fixed =
      startedAt === 'target'
        ? { ...params, source: params.target!, target: params.source! }
        : params;

    set({
      edges: withArrow(
        addEdge({ ...fixed, markerEnd: { type: MarkerType.ArrowClosed } }, get().edges)
      ),
      connectStartType: null,
    });
  },
}));

type ClassStore = { 
  classes: string[]; 
  default_classes: string[];
  setClasses: (classes: string[]) => void
  setDefaultClasses: (default_classes: string[]) => void
};

export const useClassStore = create<ClassStore>((set) => ({
  classes: [],
  default_classes: [],
  setClasses: (classes) => set({ classes }),
  setDefaultClasses: (default_classes) => set({ default_classes }),
}))

type PathStore = {
  default_class_path: string;
  class_path: string;
  pipeline_path: string;
  pipeline_dir: string;
  pipeline_paths: string[];
  setDefaultClassPath: (path: string) => void;
  setClassPath: (path: string) => void;
  setPipelinePath: (path: string) => void;
  setPipelineDir: (path: string) => void;
  setPipelinePaths: (list: string[]) => void;
}

export const usePathStore = create<PathStore>()(
  persist(
  (set) => ({
    default_class_path: "",
    class_path: "",
    pipeline_path: "",
    pipeline_dir: "",
    pipeline_paths: [],
    setClassPath: (path) => {set({class_path: path})},
    setPipelinePath: (path) => {set({pipeline_path: path})},
    setPipelinePaths: (list) => {set({pipeline_paths: list})},
    setPipelineDir: (path) => {set({pipeline_dir: path})},
    setDefaultClassPath: (path) => {set({default_class_path: path})},
  }),
  {
    name: "path-storage",
    storage: createJSONStorage(() => sessionStorage),
  }
))
