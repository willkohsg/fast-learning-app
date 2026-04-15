/**
 * Lightweight localStorage wrapper for "welcome back" recovery.
 * Stores the most recent active sessionId so the landing page can
 * offer to resume an in-progress diagnostic.
 */

const KEY = "fast-diagnostic:lastSessionId";

export function rememberSession(id: string) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(KEY, id);
  } catch {
    // Quota exceeded / private mode — silently ignore
  }
}

export function recallSession(): string | null {
  if (typeof window === "undefined") return null;
  try {
    return window.localStorage.getItem(KEY);
  } catch {
    return null;
  }
}

export function forgetSession() {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.removeItem(KEY);
  } catch {
    // ignore
  }
}
