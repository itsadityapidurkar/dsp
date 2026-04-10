"use client";

import { useEffect, useState } from "react";

import { BarChartCard } from "@/components/charts/bar-chart-card";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Select } from "@/components/ui/select";
import { api } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { CompareResponse } from "@/types/api";


function RolePanel({ panel }: { panel: CompareResponse["role_1"] }) {
  return (
    <Card className="h-full">
      <p className="text-sm uppercase tracking-[0.24em] text-muted-foreground">Role</p>
      <h2 className="mt-2 text-2xl font-semibold">{panel.name}</h2>
      <p className="mt-2 text-sm text-muted-foreground">{panel.summary}</p>
      <div className="mt-6 grid gap-4">
        <div className="rounded-2xl bg-secondary/50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Demand Level</p>
          <p className="mt-2 font-semibold">{panel.demand_level}</p>
        </div>
        <div className="rounded-2xl bg-secondary/50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Salary Range</p>
          <p className="mt-2 font-semibold">
            {formatCurrency(panel.salary_range.min, panel.salary_range.currency ?? "USD")} to{" "}
            {formatCurrency(panel.salary_range.max, panel.salary_range.currency ?? "USD")}
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl bg-secondary/50 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Top Industry</p>
            <p className="mt-2 font-semibold">{panel.top_industry}</p>
          </div>
          <div className="rounded-2xl bg-secondary/50 p-4">
            <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Experience Summary</p>
            <p className="mt-2 font-semibold">{panel.experience_summary}</p>
          </div>
        </div>
        <div className="rounded-2xl bg-secondary/50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Remote Availability</p>
          <p className="mt-2 font-semibold">{panel.remote_summary}</p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Top Skills</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {panel.top_skills.map((skill) => (
              <span key={skill} className="rounded-full bg-primary/10 px-3 py-1 text-sm text-primary">
                {skill}
              </span>
            ))}
          </div>
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Top Companies</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {panel.top_companies.map((company) => (
              <span key={company} className="rounded-full bg-secondary px-3 py-1 text-sm">
                {company}
              </span>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}


export default function ComparePage() {
  const [roles, setRoles] = useState<string[]>([]);
  const [role1, setRole1] = useState("");
  const [role2, setRole2] = useState("");
  const [comparison, setComparison] = useState<CompareResponse | null>(null);

  useEffect(() => {
    api.getRoleOptions().then((response) => {
      const options = response.items;
      setRoles(options);
      setRole1(options[0] ?? "");
      setRole2(options[1] ?? options[0] ?? "");
    });
  }, []);

  useEffect(() => {
    if (!role1 || !role2) return;
    api.compareRoles(role1, role2).then(setComparison);
  }, [role1, role2]);

  return (
    <div className="space-y-6">
      <section>
        <p className="text-sm uppercase tracking-[0.24em] text-muted-foreground">Compare Roles</p>
        <h1 className="mt-2 text-3xl font-semibold">Compare two career paths side by side.</h1>
      </section>
      <Card className="grid gap-4 md:grid-cols-[1fr_auto_1fr] md:items-center">
        <Select options={roles} value={role1} onChange={setRole1} placeholder="Select role 1" />
        <p className="text-center text-sm uppercase tracking-[0.26em] text-muted-foreground">vs</p>
        <Select options={roles} value={role2} onChange={setRole2} placeholder="Select role 2" />
      </Card>

      {comparison ? (
        <>
          <div className="grid gap-6 xl:grid-cols-2">
            <RolePanel panel={comparison.role_1} />
            <RolePanel panel={comparison.role_2} />
          </div>
          <Card>
            <h2 className="text-lg font-semibold">Common Skills</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {comparison.common_skills.map((skill) => (
                <span key={skill} className="rounded-full bg-primary/10 px-3 py-1 text-sm text-primary">
                  {skill}
                </span>
              ))}
            </div>
          </Card>
          <div className="grid gap-6 lg:grid-cols-2">
            <BarChartCard title="Demand Comparison" data={comparison.demand_comparison} dataKey="role" valueKey="value" />
            <BarChartCard title="Salary Comparison" data={comparison.salary_comparison} dataKey="role" valueKey="value" />
          </div>
          <Card>
            <h2 className="text-lg font-semibold">Final Comparison Insight</h2>
            <p className="mt-3 text-muted-foreground">{comparison.final_insight}</p>
          </Card>
        </>
      ) : (
        <EmptyState message="Choose two roles to compare their market positioning." />
      )}
    </div>
  );
}
