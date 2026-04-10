export type SkillItem = { skill: string; demand_score: number };
export type CategoryItem = { category: string; value: number };
export type RoleItem = { role: string; value: number };
export type CompanyItem = { company: string; activity_score: number };
export type LocationItem = { location: string; value: number };
export type IndustryItem = { industry: string; value: number };
export type SalaryOverviewItem = {
  role: string;
  salary_range: { min?: number | null; max?: number | null; currency?: string | null };
};

export type RoleOverview = {
  role: string;
  overview: string;
  demand_level: string;
  salary_range: { min?: number | null; max?: number | null; currency?: string | null };
  top_industry: string;
  experience_summary: string;
  remote_summary: string;
};

export type ComparePanel = {
  name: string;
  summary: string;
  demand_level: string;
  salary_range: { min?: number | null; max?: number | null; currency?: string | null };
  top_industry: string;
  experience_summary: string;
  remote_summary: string;
  top_skills: string[];
  top_companies: string[];
  experience_distribution: { level: string; value: number }[];
};

export type CompareResponse = {
  role_1: ComparePanel;
  role_2: ComparePanel;
  common_skills: string[];
  demand_comparison: { role: string; value: number }[];
  salary_comparison: { role: string; value: number }[];
  final_insight: string;
};

export type ResumeAnalysis = {
  match_score: number;
  recommended_roles: { role: string; score: number }[];
  your_skills: string[];
  missing_skills: string[];
  suggestions: string[];
  learning_resources: { skill: string; title: string; url: string }[];
  insight: string;
  profile_summary: string;
};

export type FilterMeta = {
  categories: string[];
  roles: string[];
  countries: string[];
  cities: string[];
  industries: string[];
  experience_levels: string[];
  remote_types: string[];
};
