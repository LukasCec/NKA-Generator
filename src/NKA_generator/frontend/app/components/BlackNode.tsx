import React from "react";
import { Handle, NodeProps, Position } from "reactflow";

export default function BlackNode({ data }: NodeProps) {
    return (
        <div
            style={{
                background: "black",
                color: "white",
                border: "2px solid white",
                borderRadius: 8,
                padding: "16px 24px",
                minWidth: 80,
                textAlign: "center",
            }}
        >
            {data.label}

            <Handle type="target" position={Position.Top} style={{ background: "white", border: "none" }} />
            <Handle type="source" position={Position.Bottom} style={{ background: "white", border: "none" }} />
        </div>
    );
}
