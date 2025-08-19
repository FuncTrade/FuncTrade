// store.ts
import { create } from 'zustand';
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
  setClasses: (classes: string[]) => void
};

export const useMenuClass = create<ClassStore>((set) => ({
  classes: [],
  setClasses: (classes) => set({ classes })
}))
