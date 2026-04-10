"use client";

import { useState } from "react";

import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { api } from "@/lib/api";
import { ResumeAnalysis } from "@/types/api";


export default function ResumePage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<ResumeAnalysis | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    if (!file) return;
    setError("");
    setLoading(true);
    try {
      const next = await api.analyzeResume(file);
      setResult(next);
    } catch {
      setError("Unable to read this resume. Please upload a valid PDF or DOCX file.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <section>
        <p className="text-sm uppercase tracking-[0.24em] text-muted-foreground">Resume Analyzer</p>
        <h1 className="mt-2 text-3xl font-semibold">Analyze your resume against current market expectations.</h1>
      </section>

      <Card>
        <div className="rounded-[2rem] border border-dashed border-border bg-secondary/40 p-8 text-center">
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            className="mx-auto block"
          />
          <p className="mt-4 text-sm text-muted-foreground">{file ? `Selected: ${file.name}` : "Upload a PDF or DOCX resume"}</p>
          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className="mt-6 rounded-2xl bg-primary px-5 py-3 text-sm font-medium text-primary-foreground disabled:opacity-60"
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
          {error ? <p className="mt-3 text-sm text-red-500">{error}</p> : null}
        </div>
      </Card>

      {result ? (
        <div className="space-y-6">
          <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
            <Card>
              <p className="text-sm uppercase tracking-[0.24em] text-muted-foreground">Match Score</p>
              <h2 className="mt-3 text-5xl font-semibold">{result.match_score}%</h2>
              <p className="mt-4 text-muted-foreground">{result.profile_summary}</p>
            </Card>
            <Card>
              <h2 className="text-lg font-semibold">Recommended Roles</h2>
              <div className="mt-4 space-y-3">
                {result.recommended_roles.map((role) => (
                  <div key={role.role} className="flex items-center justify-between rounded-2xl bg-secondary/50 px-4 py-3">
                    <span className="font-medium">{role.role}</span>
                    <span className="text-sm text-primary">{role.score}% match</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <h2 className="text-lg font-semibold">Your Skills</h2>
              <div className="mt-4 flex flex-wrap gap-2">
                {result.your_skills.map((skill) => (
                  <span key={skill} className="rounded-full bg-secondary px-3 py-1 text-sm">
                    {skill}
                  </span>
                ))}
              </div>
            </Card>
            <Card>
              <h2 className="text-lg font-semibold">Missing Skills</h2>
              <div className="mt-4 flex flex-wrap gap-2">
                {result.missing_skills.map((skill) => (
                  <span key={skill} className="rounded-full bg-primary/10 px-3 py-1 text-sm text-primary">
                    {skill}
                  </span>
                ))}
              </div>
            </Card>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <h2 className="text-lg font-semibold">Improvement Suggestions</h2>
              <ul className="mt-4 space-y-3 text-sm text-muted-foreground">
                {result.suggestions.map((suggestion) => (
                  <li key={suggestion}>• {suggestion}</li>
                ))}
              </ul>
            </Card>
            <Card>
              <h2 className="text-lg font-semibold">Learning Resources</h2>
              <div className="mt-4 space-y-3">
                {result.learning_resources.map((resource) => (
                  <a key={resource.skill} href={resource.url} target="_blank" rel="noreferrer" className="block rounded-2xl bg-secondary/50 px-4 py-3">
                    <p className="font-medium">{resource.skill}</p>
                    <p className="text-sm text-muted-foreground">{resource.title}</p>
                  </a>
                ))}
              </div>
            </Card>
          </div>

          <Card>
            <h2 className="text-lg font-semibold">Gemini Insights</h2>
            <p className="mt-4 text-muted-foreground">{result.insight}</p>
          </Card>
        </div>
      ) : (
        <EmptyState message="Upload a resume to see role alignment, skill gaps, and learning recommendations." />
      )}
    </div>
  );
}
