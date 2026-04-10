"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { formatCompactNumber } from "@/lib/utils";


export function BarChartCard({
  title,
  data,
  dataKey,
  valueKey,
  horizontal = false,
}: {
  title: string;
  data: Record<string, string | number>[];
  dataKey: string;
  valueKey: string;
  horizontal?: boolean;
}) {
  return (
    <Card className="h-[360px]">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold">{title}</h2>
      </div>
      {data.length === 0 ? (
        <EmptyState message="No matching insights found for this selection." />
      ) : (
        <ResponsiveContainer width="100%" height="88%">
          <BarChart data={data} layout={horizontal ? "vertical" : "horizontal"}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
            <XAxis
              type={horizontal ? "number" : "category"}
              dataKey={horizontal ? undefined : dataKey}
              tickFormatter={(value) => (horizontal ? formatCompactNumber(Number(value)) : String(value))}
            />
            <YAxis type={horizontal ? "category" : "number"} dataKey={horizontal ? dataKey : undefined} width={120} />
            <Tooltip />
            <Bar dataKey={valueKey} fill="hsl(var(--primary))" radius={[10, 10, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </Card>
  );
}
