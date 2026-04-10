import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { formatCompactNumber } from "@/lib/utils";


export function RankedListCard({
  title,
  items,
  labelKey,
  valueKey,
}: {
  title: string;
  items: Record<string, string | number>[];
  labelKey: string;
  valueKey: string;
}) {
  return (
    <Card>
      <h2 className="mb-4 text-lg font-semibold">{title}</h2>
      {items.length === 0 ? (
        <EmptyState message="No matching insights found for this selection." />
      ) : (
        <div className="space-y-3">
          {items.map((item, index) => (
            <div key={`${item[labelKey]}-${index}`} className="flex items-center justify-between rounded-2xl bg-secondary/60 px-4 py-3">
              <div>
                <p className="text-sm text-muted-foreground">#{index + 1}</p>
                <p className="font-medium">{String(item[labelKey])}</p>
              </div>
              <p className="text-sm font-semibold text-primary">{formatCompactNumber(Number(item[valueKey]))}</p>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
