import { Command } from "@tauri-apps/plugin-shell";

type LabelsResponse = Record<string, string>;

let backendStarted = false;

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function setStatus(message: string) {
  const statusEl = document.querySelector<HTMLElement>("#status-msg");
  if (statusEl) {
    statusEl.textContent = message;
  }
}

function renderLabels(labels: LabelsResponse) {
  const tableBody = document.querySelector<HTMLElement>("#labels-table-body");
  const emptyState = document.querySelector<HTMLElement>("#labels-empty");
  if (!tableBody || !emptyState) {
    return;
  }

  const rows = Object.entries(labels).sort(
    ([left], [right]) => Number(left) - Number(right),
  );

  if (rows.length === 0) {
    tableBody.innerHTML = "";
    emptyState.hidden = false;
    return;
  }

  emptyState.hidden = true;
  tableBody.innerHTML = rows
    .map(
      ([inputId, label], index) => `
        <tr class="${index === 0 ? "bg-base-200" : ""}">
          <th>${escapeHtml(inputId)}</th>
          <td>Input ${escapeHtml(inputId)}</td>
          <td class="label-cell">${escapeHtml(label || "(empty)")}</td>
        </tr>
      `,
    )
    .join("");
}

async function loadLabels() {
  try {
    setStatus("Loading labels...");
    const response = await fetch("http://127.0.0.1:8765/labels", {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Request failed with ${response.status}`);
    }

    const labels = (await response.json()) as LabelsResponse;
    renderLabels(labels);
    setStatus(`Loaded ${Object.keys(labels).length} labels from /labels`);
  } catch (error) {
    setStatus(`Failed to load labels: ${String(error)}`);
  }
}

async function startBackend() {
  if (backendStarted) {
    return;
  }

  try {
    const command = Command.sidecar("binaries/atemconnector");

    command.stdout.on("data", (line) => {
      console.log("[atemconnector stdout]", line);
    });

    command.stderr.on("data", (line) => {
      console.error("[atemconnector stderr]", line);
    });

    command.on("close", ({ code, signal }) => {
      backendStarted = false;
      console.log("[atemconnector closed]", { code, signal });
      setStatus(`atemconnector exited with code ${code ?? "null"}`);
    });

    command.on("error", (error) => {
      backendStarted = false;
      console.error("[atemconnector error]", error);
      setStatus(`Failed to start atemconnector: ${error}`);
    });

    const child = await command.spawn();
    backendStarted = true;
    console.log("[atemconnector pid]", child.pid);
    setStatus(`atemconnector started with pid ${child.pid}`);

    window.setTimeout(() => {
      void loadLabels();
    }, 800);
  } catch (error) {
    backendStarted = false;
    console.error("[atemconnector spawn failed]", error);
    setStatus(`Spawn failed: ${String(error)}`);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#reload-labels")?.addEventListener("click", () => {
    void loadLabels();
  });

  void startBackend();
});
