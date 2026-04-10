"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";


const COLORS = ["#0ea5e9", "#f59e0b", "#14b8a6", "#ef4444", "#8b5cf6", "#22c55e"];

export function DonutChartCard({ title, data }: { title: string; data: { name: string; value: number }[] }) {
  return (
    <Card className="h-[360px]">
      <h2 className="mb-4 text-lg font-semibold">{title}</h2>
      {data.length === 0 ? (
        <EmptyState message="No matching insights found for this selection." />
      ) : (
        <ResponsiveContainer width="100%" height="88%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" innerRadius={78} outerRadius={112} paddingAngle={3}>
              {data.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      )}
    </Card>
  );
}
