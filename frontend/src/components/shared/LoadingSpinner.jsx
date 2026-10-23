import React from "react";

export function LoadingSpinner({ text = "Loading...", size = "md" }) {
  const sizeMap = {
    sm: { outer: "w-5 h-5", borderWidth: "2px" },
    md: { outer: "w-8 h-8", borderWidth: "3px" },
    lg: { outer: "w-12 h-12", borderWidth: "4px" },
  };

  const { outer, borderWidth } = sizeMap[size] || sizeMap.md;

  return (
    <div className="flex flex-col items-center justify-center p-8 gap-3" style={{ color: "var(--text-muted)" }}>
      <div
        className={`${outer} rounded-full animate-spin`}
        style={{
          borderStyle: "solid",
          borderWidth,
          borderColor: "var(--primary-subtle)",
          borderTopColor: "var(--primary)",
        }}
      />
      {text && (
        <p className="text-sm tracking-wide font-medium">{text}</p>
      )}
    </div>
  );
}
