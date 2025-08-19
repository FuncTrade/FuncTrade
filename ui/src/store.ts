// store.ts
import { create } from 'zustand';
import { persist, createJSONStorage  } from "zustand/middleware";
import { applyNodeChanges, applyEdgeChanges, addEdge} from '@xyflow/react';
import type {
    Node, Edge, OnNodesChange, OnEdgesChange, OnConnect 
} from '@xyflow/react'

type FlowStore = {
  nodes: Node[];
  edges: Edge[];
  setNodes: (nodes: Node[]) => void;
  setEdges: (edges: Edge[]) => void;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
};

export const useFlowStore = create<FlowStore>((set, get) => ({
  nodes: [],
  edges: [],
  setNodes: (nodes) => set({ nodes }),
  setEdges: (edges) => set({ edges }),
  onNodesChange: (changes) => {
    set({ nodes: applyNodeChanges(changes, get().nodes) });
  },
  onEdgesChange: (changes) => {
    set({ edges: applyEdgeChanges(changes, get().edges) });
  },
  onConnect: (params) => {
    set({ edges: addEdge(params, get().edges) });
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
  setDefaultClassPath: (path: string) => void;
  setClassPath: (path: string) => void;
  setPipelinePath: (path: string) => void;
}

export const usePathStore = create<PathStore>()(
  persist(
  (set) => ({
    default_class_path: "",
    class_path: "",
    pipeline_path: "",
    setClassPath: (path) => {set({class_path: path})},
    setPipelinePath: (path) => {set({pipeline_path: path})},
    setDefaultClassPath: (path) => {set({default_class_path: path})},
  }),
  {
    name: "path-storage",
    storage: createJSONStorage(() => sessionStorage),
  }
))
