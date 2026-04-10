"use client";

import { useEffect, useState } from "react";

import { BarChartCard } from "@/components/charts/bar-chart-card";
import { RankedListCard } from "@/components/charts/ranked-list-card";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Select } from "@/components/ui/select";
import { api } from "@/lib/api";
import { CompanyItem, FilterMeta, IndustryItem, LocationItem, RoleItem, SalaryOverviewItem, SkillItem } from "@/types/api";


export default function TrendsPage() {
  const [filters, setFilters] = useState<FilterMeta | null>(null);
  const [selectedRole, setSelectedRole] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedCountry, setSelectedCountry] = useState("");
  const [selectedExperience, setSelectedExperience] = useState("");
  const [selectedIndustry, setSelectedIndustry] = useState("");
  const [selectedRemoteType, setSelectedRemoteType] = useState("");
  const [skills, setSkills] = useState<SkillItem[]>([]);
  const [roles, setRoles] = useState<RoleItem[]>([]);
  const [companies, setCompanies] = useState<CompanyItem[]>([]);
  const [locations, setLocations] = useState<LocationItem[]>([]);
  const [industries, setIndustries] = useState<IndustryItem[]>([]);
  const [salaries, setSalaries] = useState<SalaryOverviewItem[]>([]);

  const query = new URLSearchParams(
    Object.entries({
      role: selectedRole,
      category: selectedCategory,
      country: selectedCountry,
      experience_level: selectedExperience,
      industry: selectedIndustry,
      remote_type: selectedRemoteType,
    }).filter(([, value]) => value),
  ).toString();
  const suffix = query ? `?${query}` : "";

  useEffect(() => {
    api.getFilters().then(setFilters);
  }, []);

  useEffect(() => {
    Promise.all([
      api.getTrendsSkills(suffix),
      api.getTrendsRoles(suffix),
      api.getTrendsCompanies(suffix),
      api.getTrendsLocations(suffix),
      api.getTrendsSalaries(suffix),
      api.getTrendsIndustries(suffix),
    ]).then(([nextSkills, nextRoles, nextCompanies, nextLocations, nextSalaries, nextIndustries]) => {
      setSkills(nextSkills.items);
      setRoles(nextRoles.items);
      setCompanies(nextCompanies.items);
      setLocations(nextLocations.items);
      setSalaries(nextSalaries.items);
      setIndustries(nextIndustries.items);
    });
  }, [suffix]);

  return (
    <div className="space-y-6">
      <section>
        <p className="text-sm uppercase tracking-[0.24em] text-muted-foreground">Explore Trends</p>
        <h1 className="mt-2 text-3xl font-semibold">Slice the market by role, domain, location, and experience.</h1>
      </section>

      <Card className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <Select options={filters?.categories ?? []} value={selectedCategory} onChange={setSelectedCategory} placeholder="Category" />
        <Select options={filters?.roles ?? []} value={selectedRole} onChange={setSelectedRole} placeholder="Role" />
        <Select options={filters?.countries ?? []} value={selectedCountry} onChange={setSelectedCountry} placeholder="Country" />
        <Select
          options={filters?.experience_levels ?? []}
          value={selectedExperience}
          onChange={setSelectedExperience}
          placeholder="Experience level"
        />
        <Select options={filters?.industries ?? []} value={selectedIndustry} onChange={setSelectedIndustry} placeholder="Industry" />
        <Select options={filters?.remote_types ?? []} value={selectedRemoteType} onChange={setSelectedRemoteType} placeholder="Remote type" />
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <BarChartCard title="Skill Demand Trends" data={skills} dataKey="skill" valueKey="demand_score" horizontal />
        <BarChartCard title="Role Demand Trends" data={roles} dataKey="role" valueKey="value" horizontal />
        <RankedListCard title="Hiring Activity by Company" items={companies} labelKey="company" valueKey="activity_score" />
        <BarChartCard title="Location Demand" data={locations} dataKey="location" valueKey="value" />
        <BarChartCard title="Industry Insights" data={industries} dataKey="industry" valueKey="value" horizontal />
        <Card className="lg:col-span-2">
          <h2 className="mb-4 text-lg font-semibold">Salary Insights</h2>
          {salaries.length === 0 ? (
            <EmptyState message="Limited salary information available for this view." />
          ) : (
            <div className="grid gap-3 md:grid-cols-2">
              {salaries.slice(0, 8).map((salary) => (
                <div key={salary.role} className="rounded-2xl bg-secondary/50 px-4 py-3">
                  <p className="font-medium">{salary.role}</p>
                  <p className="text-sm text-muted-foreground">
                    {salary.salary_range.currency ?? "USD"} {Math.round(salary.salary_range.min ?? 0)} to {Math.round(salary.salary_range.max ?? 0)}
                  </p>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
