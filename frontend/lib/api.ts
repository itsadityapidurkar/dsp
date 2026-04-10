import {
  CategoryItem,
  CompanyItem,
  CompareResponse,
  FilterMeta,
  IndustryItem,
  LocationItem,
  ResumeAnalysis,
  RoleItem,
  RoleOverview,
  SalaryOverviewItem,
  SkillItem,
} from "@/types/api";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { ...init, cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Request failed for ${path}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  getTopSkills: () => request<{ items: SkillItem[] }>("/dashboard/skills/top"),
  getCategoryDistribution: () => request<{ items: CategoryItem[] }>("/dashboard/categories/distribution"),
  getTopRoles: () => request<{ items: RoleItem[] }>("/dashboard/roles/top"),
  getTopCompanies: () => request<{ items: CompanyItem[] }>("/dashboard/companies/top"),
  getLocationDemand: () => request<{ items: LocationItem[] }>("/dashboard/locations/demand"),
  getSalaryOverview: () => request<{ items: SalaryOverviewItem[] }>("/dashboard/salary/overview"),
  getFilters: () => request<FilterMeta>("/meta/filters"),
  getTrendsSkills: (query = "") => request<{ items: SkillItem[] }>(`/trends/skills${query}`),
  getTrendsRoles: (query = "") => request<{ items: RoleItem[] }>(`/trends/roles${query}`),
  getTrendsCompanies: (query = "") => request<{ items: CompanyItem[] }>(`/trends/companies${query}`),
  getTrendsLocations: (query = "") => request<{ items: LocationItem[] }>(`/trends/locations${query}`),
  getTrendsSalaries: (query = "") => request<{ items: SalaryOverviewItem[] }>(`/trends/salaries${query}`),
  getTrendsIndustries: (query = "") => request<{ items: IndustryItem[] }>(`/trends/industries${query}`),
  getRoleOptions: () => request<{ items: string[] }>("/roles"),
  getRoleOverview: (role: string) => request<RoleOverview>(`/roles/${encodeURIComponent(role)}/overview`),
  getRoleSkills: (role: string) => request<{ items: { skill: string; value: number }[] }>(`/roles/${encodeURIComponent(role)}/skills`),
  getRoleCompanies: (role: string) => request<{ items: { company: string; value: number }[] }>(`/roles/${encodeURIComponent(role)}/companies`),
  getRoleLocations: (role: string) => request<{ items: { location: string; value: number }[] }>(`/roles/${encodeURIComponent(role)}/locations`),
  getRoleExperience: (role: string) => request<{ items: { level: string; value: number }[] }>(`/roles/${encodeURIComponent(role)}/experience`),
  compareRoles: (role1: string, role2: string) =>
    request<CompareResponse>(`/compare/roles?role1=${encodeURIComponent(role1)}&role2=${encodeURIComponent(role2)}`),
  analyzeResume: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return request<ResumeAnalysis>("/resume/analyze", { method: "POST", body: formData });
  },
};
