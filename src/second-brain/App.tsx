import { useState, useEffect } from "react";
import { Badge } from "@openai/apps-sdk-ui/components/Badge";
import { Button } from "@openai/apps-sdk-ui/components/Button";
import { Calendar, Circle } from "@openai/apps-sdk-ui/components/Icon";

interface Note {
  id: string;
  title: string;
  description?: string;
  createdAt?: string;
  category: "general" | "technology" | "learning" | "ideas";
  tags?: string[];
}

// Extender el tipo Window para incluir openai
declare global {
  interface Window {
    __NOTES_DATA__?: Note[];
    openai?: {
      toolOutput?: {
        notes?: Note[];
      };
      callTool?: (name: string, args: any) => Promise<any>;
    };
  }
}

const categoryColors = {
  technology: "info" as const,
  learning: "success" as const,
  ideas: "warning" as const,
  general: "secondary" as const,
};

const categoryLabels = {
  technology: "Tecnología",
  learning: "Aprendizaje",
  ideas: "Ideas",
  general: "General",
};

const defaultNotes: Note[] = [
  {
    id: "1",
    title: "Ideas sobre arquitectura de software",
    description: "Reflexiones sobre patrones de diseño y arquitectura limpia",
    createdAt: "2025-01-23",
    category: "technology",
    tags: ["arquitectura", "patrones"],
  },
  {
    id: "2",
    title: "Notas de lectura: Clean Code",
    description: "Principios clave sobre escribir código limpio y mantenible",
    createdAt: "2025-01-24",
    category: "learning",
    tags: ["programación", "libros"],
  },
  {
    id: "3",
    title: "Ideas para proyecto personal",
    description: "Brainstorming de características para nueva aplicación",
    createdAt: "2025-01-25",
    category: "ideas",
    tags: ["proyecto", "innovación"],
  },
];

export function App() {
  // Inicializar desde window.openai.toolOutput o __NOTES_DATA__ o defaults
  const [notes, setNotes] = useState<Note[]>(() => {
    if (typeof window !== "undefined") {
      const data = window.openai?.toolOutput?.notes ||
        window.__NOTES_DATA__ ||
        defaultNotes;
      console.log('Second Brain App: Initializing with notes', data);
      return data;
    }
    return defaultNotes;
  });

  // Escuchar eventos de actualización desde ChatGPT
  useEffect(() => {
    const handleSetGlobals = (event: any) => {
      const globals = event.detail?.globals;
      if (globals?.toolOutput?.notes) {
        setNotes(globals.toolOutput.notes);
      }
    };

    window.addEventListener("openai:set_globals", handleSetGlobals);

    return () => {
      window.removeEventListener("openai:set_globals", handleSetGlobals);
    };
  }, []);

  return (
    <div className="w-full max-w-2xl">
      <div className="rounded-2xl border border-default bg-surface shadow-lg p-6">
        {/* Header */}
        <div className="flex items-start justify-between gap-3">
          <div>
            <h1 className="heading-xl">🧠 Second Brain</h1>
            <p className="mt-1 text-secondary text-sm">
              {notes.length} nota(s) en tu conocimiento personal
            </p>
          </div>
          <Button color="primary" size="sm">
            Nueva Nota
          </Button>
        </div>

        {/* Lista de notas */}
        {notes.length > 0 && (
          <div className="mt-6">
            <h2 className="heading-sm mb-3">Mis Notas</h2>
            <div className="space-y-3">
              {notes.map((note) => (
                <NoteCard
                  key={note.id}
                  note={note}
                />
              ))}
            </div>
          </div>
        )}

        {notes.length === 0 && (
          <div className="mt-8 text-center py-8">
            <Circle className="mx-auto size-12 text-tertiary" />
            <p className="mt-3 text-secondary">No hay notas</p>
            <p className="mt-1 text-tertiary text-sm">
              Crea tu primera nota para comenzar a construir tu Second Brain
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

function NoteCard({
  note,
}: {
  note: Note;
}) {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("es-ES", {
      day: "numeric",
      month: "short",
    });
  };

  return (
    <div className="rounded-xl border border-subtle bg-default p-4 transition-all hover:shadow-md">
      <div className="flex items-start gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <h3 className="font-medium">
              {note.title}
            </h3>
            <Badge color={categoryColors[note.category]} size="sm">
              {categoryLabels[note.category]}
            </Badge>
          </div>

          {note.description && (
            <p className="mt-1 text-sm text-secondary">{note.description}</p>
          )}

          {note.createdAt && (
            <div className="mt-2 flex items-center gap-1.5 text-xs text-tertiary">
              <Calendar className="size-3.5" />
              <span>{formatDate(note.createdAt)}</span>
            </div>
          )}

          {note.tags && note.tags.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {note.tags.map((tag, index) => (
                <span
                  key={index}
                  className="text-xs px-2 py-0.5 bg-subtle text-tertiary rounded"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

