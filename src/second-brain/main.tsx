import "./main.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { AppsSDKUIProvider } from "@openai/apps-sdk-ui/components/AppsSDKUIProvider";
import { App } from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AppsSDKUIProvider>
      <App />
    </AppsSDKUIProvider>
  </StrictMode>
);

