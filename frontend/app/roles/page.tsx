"use client";

import { useEffect, useState } from "react";

import { BarChartCard } from "@/components/charts/bar-chart-card";
import { RankedListCard } from "@/components/charts/ranked-list-card";
import { Card } from "@/components/ui/card";
import { Select } from "@/components/ui/select";
import { api } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { RoleOverview } from "@/types/api";

type SkillBreakdownItem = { skill: string; value: number };
type CompanyBreakdownItem = { company: string; value: number };
type LocationBreakdownItem = { location: string; value: number };
type ExperienceBreakdownItem = { level: string; value: number };


export default function RolesPage() {
  const [roles, setRoles] = useState<string[]>([]);
  const [selectedRole, setSelectedRole] = useState("");
  const [overview, setOverview] = useState<RoleOverview | null>(null);
  const [skills, setSkills] = useState<SkillBreakdownItem[]>([]);
  const [companies, setCompanies] = useState<CompanyBreakdownItem[]>([]);
  const [locations, setLocations] = useState<LocationBreakdownItem[]>([]);
  const [experience, setExperience] = useState<ExperienceBreakdownItem[]>([]);

  useEffect(() => {
    api.getRoleOptions().then((response) => {
      setRoles(response.items);
      setSelectedRole(response.items[0] ?? "");
    });
  }, []);

  useEffect(() => {
    if (!selectedRole) return;
    Promise.all([
      api.getRoleOverview(selectedRole),
      api.getRoleSkills(selectedRole),
      api.getRoleCompanies(selectedRole),
      api.getRoleLocations(selectedRole),
      api.getRoleExperience(selectedRole),
    ]).then(([nextOverview, nextSkills, nextCompanies, nextLocations, nextExperience]) => {
      setOverview(nextOverview);
      setSkills(nextSkills.items);
      setCompanies(nextCompanies.items);
      setLocations(nextLocations.items);
      setExperience(nextExperience.items);
    });
  }, [selectedRole]);

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-muted-foreground">Role Explorer</p>
          <h1 className="mt-2 text-3xl font-semibold">Inspect one role in depth.</h1>
        </div>
        <div className="w-full max-w-sm">
          <Select options={roles} value={selectedRole} onChange={setSelectedRole} placeholder="Select a role" />
        </div>
      </section>

      {overview && (
        <>
          <Card className="rounded-[2rem] bg-gradient-to-br from-primary/10 via-transparent to-secondary/70">
            <p className="text-sm uppercase tracking-[0.26em] text-muted-foreground">Role Snapshot</p>
            <h2 className="mt-3 text-3xl font-semibold">{overview.role}</h2>
            <p className="mt-3 max-w-3xl text-muted-foreground">{overview.overview}</p>
            <div className="mt-6 grid gap-4 md:grid-cols-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Demand Level</p>
                <p className="mt-2 font-semibold">{overview.demand_level}</p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Salary Range</p>
                <p className="mt-2 font-semibold">
                  {formatCurrency(overview.salary_range.min, overview.salary_range.currency ?? "USD")} to{" "}
                  {formatCurrency(overview.salary_range.max, overview.salary_range.currency ?? "USD")}
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Top Industry</p>
                <p className="mt-2 font-semibold">{overview.top_industry}</p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Remote Pattern</p>
                <p className="mt-2 font-semibold">{overview.remote_summary}</p>
              </div>
            </div>
          </Card>

          <div className="grid gap-6 lg:grid-cols-2">
            <RankedListCard title="Most Important Skills" items={skills} labelKey="skill" valueKey="value" />
            <RankedListCard title="Companies Hiring for This Role" items={companies} labelKey="company" valueKey="value" />
            <BarChartCard title="Location Demand" data={locations} dataKey="location" valueKey="value" />
            <BarChartCard title="Experience Distribution" data={experience} dataKey="level" valueKey="value" />
          </div>
        </>
      )}
    </div>
  );
}
