import { BarChartCard } from "@/components/charts/bar-chart-card";
import { DonutChartCard } from "@/components/charts/donut-chart-card";
import { RankedListCard } from "@/components/charts/ranked-list-card";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { api } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";


export default async function DashboardPage() {
  const [skills, categories, roles, companies, locations, salary] = await Promise.all([
    api.getTopSkills(),
    api.getCategoryDistribution(),
    api.getTopRoles(),
    api.getTopCompanies(),
    api.getLocationDemand(),
    api.getSalaryOverview(),
  ]);

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] bg-gradient-to-br from-primary/15 via-secondary to-transparent p-8">
        <p className="text-sm uppercase tracking-[0.26em] text-muted-foreground">Market Pulse</p>
        <h1 className="mt-3 max-w-3xl text-4xl font-semibold tracking-tight">See where hiring momentum, skill demand, and career opportunities are moving.</h1>
      </section>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <BarChartCard title="Most In-Demand Skills" data={skills.items} dataKey="skill" valueKey="demand_score" horizontal />
        <DonutChartCard title="Job Market Distribution by Domain" data={categories.items.map((item) => ({ name: item.category, value: item.value }))} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <BarChartCard title="Roles with Highest Demand" data={roles.items} dataKey="role" valueKey="value" horizontal />
        <RankedListCard title="Companies Hiring the Most" items={companies.items} labelKey="company" valueKey="activity_score" />
        <BarChartCard title="Where Opportunities Are Growing" data={locations.items} dataKey="location" valueKey="value" />
        <Card>
          <h2 className="mb-4 text-lg font-semibold">Salary Trends by Role</h2>
          {salary.items.length === 0 ? (
            <EmptyState message="Limited salary information available for this view." />
          ) : (
            <div className="space-y-3">
              {salary.items.slice(0, 6).map((item) => (
                <div key={item.role} className="rounded-2xl bg-secondary/50 px-4 py-3">
                  <div className="flex items-center justify-between gap-3">
                    <p className="font-medium">{item.role}</p>
                    <p className="text-sm text-muted-foreground">
                      {formatCurrency(item.salary_range.min, item.salary_range.currency ?? "USD")} to{" "}
                      {formatCurrency(item.salary_range.max, item.salary_range.currency ?? "USD")}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
