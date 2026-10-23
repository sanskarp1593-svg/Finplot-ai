import React from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";

/**
 * React Error Boundary – catches rendering errors in child components and
 * displays a clean fallback instead of a blank screen.
 */
export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error("[ErrorBoundary] Caught error:", error, info);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div
          className="flex flex-col items-center justify-center min-h-[60vh] p-8 text-center"
          style={{ color: "var(--text-primary)" }}
        >
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center mb-6"
            style={{ background: "var(--danger-subtle)" }}
          >
            <AlertTriangle className="w-8 h-8" style={{ color: "var(--danger)" }} />
          </div>

          <h2
            className="text-xl font-bold mb-2"
            style={{ fontFamily: "var(--font-display)" }}
          >
            Something went wrong
          </h2>

          <p className="text-sm mb-1 max-w-md" style={{ color: "var(--text-secondary)" }}>
            A rendering error occurred in this view. The rest of the app is unaffected.
          </p>

          {this.state.error && (
            <pre
              className="text-xs mt-3 mb-5 px-4 py-3 rounded-xl text-left max-w-lg overflow-x-auto"
              style={{
                background: "var(--bg-tertiary)",
                border: "1px solid var(--border-subtle)",
                color: "var(--danger)",
              }}
            >
              {this.state.error.message}
            </pre>
          )}

          <button onClick={this.handleReset} className="btn btn-primary">
            <RefreshCw className="w-4 h-4" />
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
